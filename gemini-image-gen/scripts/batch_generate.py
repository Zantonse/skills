#!/usr/bin/env python3
"""Batch generate multiple images from a JSON manifest.

Usage:
    python3 batch_generate.py --manifest assets.json --outdir ./generated

Manifest format (JSON array):
[
    {
        "prompt": "Luxury hotel lobby with golden lighting",
        "filename": "hero-bg.png",
        "aspect": "16:9",
        "size": "2K"
    },
    {
        "prompt": "Minimalist shield icon, flat design, gold on transparent",
        "filename": "icon-security.png",
        "aspect": "1:1",
        "size": "1K"
    }
]

Features:
  - Auto-retries rate-limited (429) and transient errors with exponential backoff
  - Writes a *-failed.json manifest for any remaining failures (re-run with same command)
  - Skips images that already exist in outdir (use --force to regenerate)
  - Smarter default delay: 4s for LiteLLM proxy, 2s for direct API

Environment:
    LITELLM_API_KEY + LITELLM_BASE_URL  — use LiteLLM proxy mode
    GEMINI_API_KEY                       — use direct Gemini API mode
"""

import argparse
import json
import os
import sys
import time

# Allow importing generate from sibling script
sys.path.insert(0, os.path.dirname(__file__))
from generate_image import ensure_dependencies, generate, _use_litellm, ImageGenError


def main():
    is_litellm = _use_litellm()
    default_delay = 4.0 if is_litellm else 2.0

    parser = argparse.ArgumentParser(
        description="Batch generate images from manifest. "
        "WARNING: Do not run multiple batch processes in parallel against the same LiteLLM proxy."
    )
    parser.add_argument("--manifest", "-f", required=True, help="Path to JSON manifest")
    parser.add_argument("--outdir", "-d", default="./generated", help="Output directory")
    parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="Gemini model (default: gemini-3-pro-image-preview for LiteLLM, gemini-2.5-flash-image for direct)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=default_delay,
        help=f"Delay between requests in seconds (default: {default_delay})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate images even if they already exist in outdir",
    )
    args = parser.parse_args()

    # Set default model based on mode
    if args.model is None:
        if is_litellm:
            args.model = "gemini-3-pro-image-preview"
        else:
            args.model = "gemini-2.5-flash-image"

    ensure_dependencies()

    try:
        with open(args.manifest) as f:
            items = json.load(f)
    except FileNotFoundError:
        print(f"Error: Manifest file not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in manifest {args.manifest}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(items, list):
        print(f"Error: Manifest must be a JSON array, got {type(items).__name__}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    total = len(items)
    success = 0
    skipped = 0
    failed_items: list[dict] = []

    for i, item in enumerate(items, 1):
        # Validate required fields
        if not isinstance(item, dict):
            print(f"  SKIPPED: Manifest item {i} is not an object (got {type(item).__name__})", file=sys.stderr)
            failed_items.append({"_error": f"Invalid manifest item type: {type(item).__name__}", "_index": i})
            continue
        if "prompt" not in item or "filename" not in item:
            missing = [k for k in ("prompt", "filename") if k not in item]
            print(f"  SKIPPED: Missing required fields: {', '.join(missing)}", file=sys.stderr)
            failed_items.append({**item, "_error": f"Missing required fields: {', '.join(missing)}"})
            continue

        prompt = item["prompt"]
        filename = item["filename"]
        aspect = item.get("aspect")
        size = item.get("size")
        input_img = item.get("input")
        output_path = os.path.join(args.outdir, filename)

        # Skip existing files unless --force
        if not args.force and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 100:  # Minimum viable PNG size
                print(f"\n[{i}/{total}] {filename} — already exists ({file_size:,} bytes), skipping")
                skipped += 1
                continue
            else:
                print(f"\n[{i}/{total}] {filename} — exists but appears corrupt ({file_size} bytes), regenerating")

        print(f"\n[{i}/{total}] {filename}")
        try:
            generate(
                prompt=prompt,
                output_path=output_path,
                model=args.model,
                aspect_ratio=aspect,
                image_size=size,
                input_image=input_img,
            )
            success += 1
        except Exception as e:
            error_msg = str(e)
            retryable = getattr(e, "retryable", None)
            label = "RETRYABLE" if retryable else "PERMANENT"
            print(f"  FAILED ({label}): {error_msg}", file=sys.stderr)
            failed_items.append({**item, "_error": error_msg, "_retryable": bool(retryable)})

        if i < total:
            time.sleep(args.delay)

    # Write failed manifest for easy retry
    if failed_items:
        manifest_base = os.path.splitext(os.path.basename(args.manifest))[0]
        failed_manifest = os.path.join(os.path.dirname(args.manifest) or ".", f"{manifest_base}-failed.json")
        # Strip internal error fields for the retry manifest
        retry_items = [{k: v for k, v in item.items() if not k.startswith("_")} for item in failed_items]
        with open(failed_manifest, "w") as f:
            json.dump(retry_items, f, indent=2)
        print(f"\nFailed manifest written to: {failed_manifest}")
        print(f"  Retry with: python3 {__file__} -f {failed_manifest} -d {args.outdir}")

    failed = len(failed_items)
    parts = [f"{success} succeeded"]
    if skipped:
        parts.append(f"{skipped} skipped (existing)")
    if failed:
        parts.append(f"{failed} failed")
    print(f"\nDone: {', '.join(parts)} — {total} total")

    # Exit with error code if any failures
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
