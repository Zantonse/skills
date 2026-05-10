---
name: add-litellm-mcp
version: 1.0.0
description: |
  Add a new MCP server to ~/.claude.json. Handles two cases:
  1. LiteLLM proxy MCPs (https://llm.atko.ai/<slug>/mcp) — auto-applies the
     OCM headersHelper pattern used by all existing LiteLLM MCPs.
  2. External/OAuth MCPs (custom URL) — adds a bare http entry and notes any
     auth the user needs to handle.
  Use when: "add mcp", "install mcp", "add <name> mcp", "register mcp server",
  "I want to add another MCP".
triggers:
  - add mcp
  - install mcp server
  - register mcp
  - add litellm mcp
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
---

## add-litellm-mcp skill

The user wants to add an MCP server. Follow these steps exactly.

### Step 1 — Gather info

Ask the user:
- **MCP name** — the key it will appear under in Claude (e.g. `jira`, `confluence`, `figma`)
- **LiteLLM slug or full URL** — either:
  - A slug for the LiteLLM proxy: `https://llm.atko.ai/<slug>/mcp`
  - Or a full custom URL (e.g. `https://mcp.atlassian.com/v1/mcp`)
- If the slug differs from the name (like `demo-okta` → slug is `oktademo_mcp`), confirm both

If the user provides enough info upfront, skip the question and proceed.

### Step 2 — Check for duplicates

Read `~/.claude.json` and check if the name already exists under `mcpServers`. If it does, show the existing entry and ask the user if they want to update it or pick a different name.

```bash
python3 -c "
import json
d = json.load(open('/Users/craigverzosa/.claude.json'))
servers = d.get('mcpServers', {})
print(json.dumps(servers, indent=2))
"
```

### Step 3 — Build the entry

**For LiteLLM proxy MCPs** (URL starts with `https://llm.atko.ai/` or user provides only a slug):

```json
"<name>": {
  "type": "http",
  "url": "https://llm.atko.ai/<slug>/mcp",
  "host": "llm.atko.ai",
  "headersHelper": "/Users/craigverzosa/.ocm/fetch-mcp-headers.sh"
}
```

**For external/OAuth MCPs** (custom URL like `https://mcp.atlassian.com/v1/mcp`):

```json
"<name>": {
  "type": "http",
  "url": "<full-url>"
}
```
Note: OAuth flow will trigger on first tool use in a new session.

### Step 4 — Write to ~/.claude.json

Use Python to safely update the file (never overwrite the whole thing):

```bash
python3 -c "
import json

path = '/Users/craigverzosa/.claude.json'
with open(path) as f:
    d = json.load(f)

if 'mcpServers' not in d:
    d['mcpServers'] = {}

d['mcpServers']['<NAME>'] = {
    'type': 'http',
    'url': 'https://llm.atko.ai/<SLUG>/mcp',
    'host': 'llm.atko.ai',
    'headersHelper': '/Users/craigverzosa/.ocm/fetch-mcp-headers.sh'
}

with open(path, 'w') as f:
    json.dump(d, f, indent=2)

print('Done.')
"
```

### Step 5 — Verify and inform user

Run `claude mcp list` to confirm the new server appears. Then tell the user:

> **"<name>" added.** To use it, start a **fresh Claude Code session** — MCP tools are only injected at session start, not mid-session. The server will show up in `/mcp` and its tools will be available immediately on next launch.

If it's an OAuth MCP (external URL), add:
> On first use, Claude will prompt you to authenticate via the browser OAuth flow.

### Important notes

- Always use `python3 -c "..."` to edit `~/.claude.json` — never use sed/awk on JSON
- Never hardcode Bearer tokens — the `headersHelper` script handles auth dynamically via `ocm`
- `~/.claude.json` is the canonical MCP config. `~/.claude/mcp.json` is a legacy file — do not write new entries there
- The `host` field is required for LiteLLM MCPs (used by the OCM routing layer)
