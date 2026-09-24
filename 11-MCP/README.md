# Notes MCP Server

A beginner-friendly MCP server built with [FastMCP](https://gofastmcp.com) that lets Claude (or any MCP client) save, list and delete notes stored locally in `notes.json`.

## What this covers

The three MCP building blocks:

| Building block | What it does | Example |
|---|---|---|
| **Tool** | An action the client/AI can call | `add_note`, `list_notes`, `delete_note` |
| **Resource** | Data the client/AI can read | `notes://all` |
| **Prompt** | A reusable prompt template | `summarize_notes` |

## Project structure

```
server.py       ← MCP server (FastMCP)
pyproject.toml  ← dependencies (fastmcp, mcp)
notes.json      ← notes are saved here (created on first use)
```

## Setup

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv sync
```

## Run & test with the inspector

```bash
uv run fastmcp dev inspector server.py
```

This opens a browser UI (MCP Inspector) where you can call the tools by hand before connecting Claude.

## Connect to Claude Desktop

Open **Claude Desktop → Settings → Developer → Edit Config** and add:

```json
{
  "mcpServers": {
    "notes": {
      "command": "/absolute/path/to/uv",
      "args": ["--directory", "/absolute/path/to/this/folder", "run", "server.py"]
    }
  }
}
```

- Find your uv path: `which uv` (macOS/Linux) or `where uv` (Windows)
- Use absolute paths — Claude Desktop does not inherit your terminal's PATH
- Config file locations:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - Linux: `~/.config/Claude/claude_desktop_config.json`

Fully quit Claude Desktop (not just close the window) and reopen it.

## Try it in Claude

- "Save a note titled 'Exam' saying the MCP exam is on Friday."
- "What notes do I have?"
- "Delete note 1."

## Troubleshooting

Logs:
- macOS: `~/Library/Logs/Claude/mcp-server-notes.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-notes.log`
- Linux: `~/.config/Claude/logs/mcp-server-notes.log`

Run the server manually to check for errors:
```bash
uv run fastmcp run server.py
```

## FastMCP vs official MCP SDK

This server uses the standalone **FastMCP** package (`pip install fastmcp`, docs at [gofastmcp.com](https://gofastmcp.com)).

The official SDK (`pip install mcp`) has the same decorator style but uses a different class name:

```python
# FastMCP (this project)          # Official SDK
from fastmcp import FastMCP        from mcp.server import MCPServer
mcp = FastMCP("Notes")             mcp = MCPServer("Notes")

@mcp.tool                          @mcp.tool()          # parentheses required
def add_note(...): ...             def add_note(...): ...
```

The MCP client (`client.py`) works with both — it uses the official `mcp` SDK's `Client` class, which speaks standard MCP protocol regardless of which server library you use.
