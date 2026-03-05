#!/usr/bin/env python3
"""Generate images using Google Gemini's native image generation.

Supports two modes:
  1. LiteLLM proxy (default if LITELLM_API_KEY + LITELLM_BASE_URL are set)
  2. Direct Google GenAI SDK (if GEMINI_API_KEY is set)

Usage:
    # Via LiteLLM proxy (e.g., llm.atko.ai)
    export LITELLM_API_KEY="sk-..."
    export LITELLM_BASE_URL="https://llm.atko.ai"
    python3 generate_image.py --prompt "A luxury hotel lobby" --output lobby.png

    # Via direct Gemini API
    export GEMINI_API_KEY="..."
    python3 generate_image.py --prompt "A luxury hotel lobby" --output lobby.png

    # With options
    python3 generate_image.py --prompt "Minimalist shield icon" --output icon.png --aspect 1:1 --size 1K
    python3 generate_image.py --prompt "Add golden lighting" --input photo.png --output edited.png
"""

import argparse
import base64
import os
import random
import sys
import subprocess
import time
from typing import Optional


def ensure_dependencies():
    """Install required packages if not already available."""
    # Always need Pillow
    for pkg, import_name in [("Pillow", "PIL")]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {pkg}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pkg, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to install {pkg}: {e.stderr.decode() if e.stderr else 'unknown error'}", file=sys.stderr)
                raise

    # Install SDK based on mode
    if _use_litellm():
        for pkg, import_name in [("openai", "openai")]:
            try:
                __import__(import_name)
            except ImportError:
                print(f"Installing {pkg}...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pkg, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE,
                    )
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to install {pkg}: {e.stderr.decode() if e.stderr else 'unknown error'}", file=sys.stderr)
                    raise
    else:
        for pkg, import_name in [("google-genai", "google.genai")]:
            try:
                __import__(import_name)
            except ImportError:
                print(f"Installing {pkg}...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pkg, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE,
                    )
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to install {pkg}: {e.stderr.decode() if e.stderr else 'unknown error'}", file=sys.stderr)
                    raise


def _load_env_file():
    """Auto-load credentials from ~/.claude-litellm.env if env vars are missing."""
    if os.environ.get("LITELLM_API_KEY") or os.environ.get("GEMINI_API_KEY"):
        return  # Already have credentials
    env_file = os.path.expanduser("~/.claude-litellm.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ") and "=" in line:
                    line = line[7:]  # Remove "export "
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    # Resolve $VAR references
                    if value.startswith("$"):
                        ref_var = value[1:]
                        value = os.environ.get(ref_var, "")
                    if key and value:
                        os.environ[key] = value


_load_env_file()


def _use_litellm() -> bool:
    """Check if LiteLLM proxy credentials are available."""
    return bool(os.environ.get("LITELLM_API_KEY") and os.environ.get("LITELLM_BASE_URL"))


class ImageGenError(Exception):
    """Base exception for image generation failures."""

    def __init__(self, message: str, retryable: bool = False):
        super().__init__(message)
        self.retryable = retryable


def _retry_with_backoff(fn, max_retries: int = 3, base_delay: float = 4.0):
    """Retry a function with exponential backoff + jitter on retryable errors."""
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except ImageGenError as e:
            if not e.retryable or attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 2)
            print(f"  Retryable error: {e} — retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)


def _classify_error(exc: Exception) -> ImageGenError:
    """Classify an API exception into a retryable or non-retryable ImageGenError."""
    msg = str(exc).lower()
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)

    # Rate limiting — always retryable
    if status == 429 or "429" in msg or ("rate limit" in msg):
        return ImageGenError(f"Rate limited (429). {exc}", retryable=True)

    # Timeout — retryable
    if "timeout" in msg or "timed out" in msg:
        return ImageGenError(f"Request timed out. {exc}", retryable=True)

    # Transient server errors — retryable
    if status in (500, 502, 503, 504) or "server error" in msg or "internal server" in msg:
        return ImageGenError(f"Server error ({status}). {exc}", retryable=True)

    # Auth / model access — not retryable
    if status in (401, 403) or "unauthorized" in msg or "forbidden" in msg or "not allowed" in msg:
        return ImageGenError(
            f"Authorization failed. Check your API key has access to the requested model. {exc}",
            retryable=False,
        )

    # Safety filter — not retryable (prompt needs rephrasing)
    if any(kw in msg for kw in ("safety filter", "content blocked", "content policy", "content filter", "i can't", "i cannot", "not able to generate", "violates")):
        return ImageGenError(
            f"Prompt blocked by safety filter. Rephrase with concrete, photographic language. {exc}",
            retryable=False,
        )

    # Unknown — not retryable by default
    return ImageGenError(str(exc), retryable=False)


def _generate_litellm(
    prompt: str,
    output_path: str,
    model: str,
    aspect_ratio: Optional[str] = None,
    image_size: Optional[str] = None,
) -> str:
    """Generate image via LiteLLM proxy using OpenAI-compatible /v1/images/generations."""
    from openai import OpenAI

    api_key = os.environ["LITELLM_API_KEY"]
    base_url = os.environ["LITELLM_BASE_URL"].rstrip("/")

    # Ensure base_url ends with /v1 for OpenAI SDK compatibility
    if not base_url.endswith("/v1"):
        base_url = base_url + "/v1"

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=120.0)

    # Build the prompt — append aspect/size hints for the model
    full_prompt = prompt
    if aspect_ratio:
        full_prompt += f" [aspect ratio: {aspect_ratio}]"

    # Translate direct-API size formats to OpenAI format for LiteLLM
    litellm_size = image_size
    if litellm_size:
        size_map = {"512px": "512x512", "1K": "1024x1024", "2K": "2048x2048", "4K": "4096x4096"}
        litellm_size = size_map.get(litellm_size, litellm_size)

    def _call():
        print(f"Generating via LiteLLM proxy with {model}...")
        try:
            response = client.images.generate(
                model=model,
                prompt=full_prompt,
                n=1,
                size=litellm_size or "1024x1024",
                response_format="b64_json",
            )
        except Exception as e:
            raise _classify_error(e)

        if not response.data or not response.data[0].b64_json:
            raise ImageGenError(
                "No image returned. The prompt may have been blocked by safety filters. "
                "Try rephrasing with concrete, photographic descriptions.",
                retryable=False,
            )
        return response

    response = _retry_with_backoff(_call)

    b64_data = response.data[0].b64_json
    image_bytes = base64.b64decode(b64_data)
    if len(image_bytes) == 0:
        raise ImageGenError("API returned empty image data. The prompt may have been silently filtered.", retryable=False)

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    try:
        with open(output_path, "wb") as f:
            f.write(image_bytes)
    except OSError as e:
        raise ImageGenError(f"Failed to write output file {output_path}: {e}", retryable=False)

    print(f"Saved: {output_path}")
    return output_path


def _generate_direct(
    prompt: str,
    output_path: str,
    model: str,
    aspect_ratio: Optional[str] = None,
    image_size: Optional[str] = None,
    input_image: Optional[str] = None,
) -> str:
    """Generate image via direct Google GenAI SDK."""
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ImageGenError(
            "GEMINI_API_KEY environment variable is required. "
            "Get one at https://aistudio.google.com/apikey",
            retryable=False,
        )

    client = genai.Client(api_key=api_key)

    config_kwargs: dict = {"response_modalities": ["IMAGE"]}
    if aspect_ratio or image_size:
        img_cfg: dict = {}
        if aspect_ratio:
            img_cfg["aspect_ratio"] = aspect_ratio
        if image_size:
            img_cfg["image_size"] = image_size
        config_kwargs["image_config"] = types.ImageConfig(**img_cfg)

    config = types.GenerateContentConfig(**config_kwargs)

    contents: list = []
    if input_image:
        from PIL import Image

        img = Image.open(input_image)
        contents = [prompt, img]
    else:
        contents = [prompt]

    def _call():
        print(f"Generating with {model}...")
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except Exception as e:
            raise _classify_error(e)

        # Check for safety-filter text responses instead of images
        for part in response.parts:
            if part.inline_data is not None:
                return part.inline_data.data
            elif part.text is not None:
                text = part.text.lower()
                if any(kw in text for kw in ("i can't", "i cannot", "sorry", "unable", "not able", "i'm not able", "not something i can", "i don't generate", "violates", "not permitted")):
                    raise ImageGenError(
                        f"Prompt blocked by safety filter: {part.text[:120]}. "
                        "Rephrase with concrete, photographic language.",
                        retryable=False,
                    )
                print(f"Model response: {part.text}", file=sys.stderr)

        raise ImageGenError(
            "No image returned. The prompt may have been blocked by safety filters. "
            "Try rephrasing with concrete, photographic descriptions.",
            retryable=False,
        )

    image_data = _retry_with_backoff(_call)

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    try:
        with open(output_path, "wb") as f:
            f.write(image_data)
    except OSError as e:
        raise ImageGenError(f"Failed to write output file {output_path}: {e}", retryable=False)

    print(f"Saved: {output_path}")
    return output_path


def _generate_programmatic(prompt: str, output_path: str, image_size: Optional[str] = None, aspect_ratio: Optional[str] = None) -> Optional[str]:
    """Generate simple procedural images that Gemini can't handle (noise, gradients, solids).

    Returns output_path if handled, None if the prompt isn't a programmatic type.
    """
    from PIL import Image

    prompt_lower = prompt.lower()

    # Parse dimensions from size/aspect params
    width, height = 1024, 1024
    if image_size:
        size_map = {"512px": 512, "1K": 1024, "2K": 2048, "4K": 4096}
        dim = size_map.get(image_size, 1024)
        width, height = dim, dim
    if aspect_ratio:
        try:
            w, h = map(int, aspect_ratio.split(":"))
            # Scale to fit within the max dimension
            max_dim = max(width, height)
            if w > h:
                width = max_dim
                height = int(max_dim * h / w)
            else:
                height = max_dim
                width = int(max_dim * w / h)
        except (ValueError, ZeroDivisionError):
            pass  # Invalid aspect ratio, use defaults

    # Detect noise/grain texture requests
    noise_keywords = ["noise texture", "grain texture", "film grain", "noise overlay", "grain overlay",
                      "grainy", "sensor noise", "photographic grain", "digital noise"]
    if any(kw in prompt_lower for kw in noise_keywords):
        print("Generating noise texture programmatically (Gemini cannot generate pure noise)...")
        img = Image.new("RGBA", (width, height))
        pixels = img.load()
        # Compute alpha once outside the loop
        alpha = 30
        if "high opacity" in prompt_lower or "dense" in prompt_lower:
            alpha = 60
        elif "subtle" in prompt_lower or "light" in prompt_lower:
            alpha = 15

        for y in range(height):
            for x in range(width):
                v = random.randint(0, 255)
                pixels[x, y] = (v, v, v, alpha)

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        img.save(output_path)
        print(f"Saved (programmatic): {output_path}")
        return output_path

    # Detect solid color requests
    solid_keywords = ["solid color", "solid background", "flat color background",
                      "plain background", "uniform background", "monochrome fill", "single color fill"]
    if any(kw in prompt_lower for kw in solid_keywords):
        import re

        print("Generating solid color programmatically...")
        # Try to find hex color in prompt
        hex_match = re.search(r"#([0-9a-fA-F]{6})", prompt)
        color = tuple(int(hex_match.group(1)[i : i + 2], 16) for i in (0, 2, 4)) if hex_match else (26, 26, 36)
        img = Image.new("RGB", (width, height), color)
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        img.save(output_path)
        print(f"Saved (programmatic): {output_path}")
        return output_path

    # Detect simple gradient requests
    gradient_keywords = ["simple gradient", "linear gradient background", "gradient background only",
                         "color gradient", "two-color gradient", "vertical gradient", "gradient overlay"]
    if any(kw in prompt_lower for kw in gradient_keywords):
        import re

        print("Generating gradient programmatically...")
        hex_colors = re.findall(r"#([0-9a-fA-F]{6})", prompt)
        c1 = tuple(int(hex_colors[0][i : i + 2], 16) for i in (0, 2, 4)) if len(hex_colors) >= 1 else (10, 10, 26)
        c2 = tuple(int(hex_colors[1][i : i + 2], 16) for i in (0, 2, 4)) if len(hex_colors) >= 2 else (40, 30, 80)
        img = Image.new("RGB", (width, height))
        pixels = img.load()
        for y in range(height):
            t = y / height
            r = int(c1[0] * (1 - t) + c2[0] * t)
            g = int(c1[1] * (1 - t) + c2[1] * t)
            b = int(c1[2] * (1 - t) + c2[2] * t)
            for x in range(width):
                pixels[x, y] = (r, g, b)
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        img.save(output_path)
        print(f"Saved (programmatic): {output_path}")
        return output_path

    return None  # Not a programmatic type


def generate(
    prompt: str,
    output_path: str,
    model: str = "gemini-2.5-flash-image",
    aspect_ratio: Optional[str] = None,
    image_size: Optional[str] = None,
    input_image: Optional[str] = None,
) -> str:
    """Generate or edit an image and save to output_path. Returns the output path.

    Automatically selects LiteLLM proxy or direct SDK based on available env vars.
    For certain prompt types that Gemini cannot generate (noise textures, solid colors,
    simple gradients), falls back to programmatic Pillow generation automatically.
    """
    # Try programmatic generation first for known-failing categories
    if not input_image:
        result = _generate_programmatic(prompt, output_path, image_size=image_size, aspect_ratio=aspect_ratio)
        if result:
            return result

    if _use_litellm():
        if input_image:
            raise ImageGenError(
                "Image editing (--input) is only supported with direct Gemini API, not LiteLLM proxy. "
                "Set GEMINI_API_KEY instead.",
                retryable=False,
            )
        return _generate_litellm(prompt, output_path, model, aspect_ratio, image_size)
    else:
        return _generate_direct(prompt, output_path, model, aspect_ratio, image_size, input_image)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images with Gemini (via LiteLLM proxy or direct API)"
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image generation prompt")
    parser.add_argument("--output", "-o", required=True, help="Output file path (PNG)")
    parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="Model name (default: gemini-3-pro-image-preview for LiteLLM, gemini-2.5-flash-image for direct)",
    )
    parser.add_argument(
        "--aspect",
        "-a",
        default=None,
        help="Aspect ratio (e.g., 16:9, 1:1, 3:2). Only for gemini-3.x models.",
    )
    parser.add_argument(
        "--size",
        "-s",
        default=None,
        help="Image size (512px, 1K, 2K, 4K for direct; 1024x1024 etc. for LiteLLM).",
    )
    parser.add_argument(
        "--input",
        "-i",
        default=None,
        help="Input image path for editing (direct API only, not supported via LiteLLM proxy)",
    )
    args = parser.parse_args()

    # Set default model based on mode
    if args.model is None:
        if _use_litellm():
            args.model = "gemini-3-pro-image-preview"
        else:
            args.model = "gemini-2.5-flash-image"

    ensure_dependencies()
    generate(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        aspect_ratio=args.aspect,
        image_size=args.size,
        input_image=args.input,
    )


if __name__ == "__main__":
    main()
