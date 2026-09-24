"""Notes MCP server — built with the standalone FastMCP package (gofastmcp.com).

Same three building blocks:
  Tools     -> add_note, list_notes, delete_note
  Resource  -> notes://all
  Prompt    -> summarize_notes

Run directly:    uv run server.py
Dev inspector:   uv run fastmcp dev server.py
"""

import json
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

NOTES_FILE = Path(__file__).parent / "notes.json"

# Create the server — just the name, nothing else needed
mcp = FastMCP("Notes")


def load_notes() -> list[dict]:
    if not NOTES_FILE.exists():
        return []
    return json.loads(NOTES_FILE.read_text())


def save_notes(notes: list[dict]) -> None:
    NOTES_FILE.write_text(json.dumps(notes, indent=2))


# ── Tools ──────────────────────────────────────────────────────────────────


@mcp.tool
def add_note(title: str, content: str) -> str:
    """Save a new note with a title and content."""
    notes = load_notes()
    notes.append(
        {
            "id": len(notes) + 1,
            "title": title,
            "content": content,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    save_notes(notes)
    return f"Saved note '{title}'."


@mcp.tool
def list_notes() -> list[dict]:
    """Return all saved notes."""
    return load_notes()


@mcp.tool
def delete_note(note_id: int) -> str:
    """Delete a note by its id."""
    notes = load_notes()
    remaining = [n for n in notes if n["id"] != note_id]
    if len(remaining) == len(notes):
        return f"No note with id {note_id}."
    save_notes(remaining)
    return f"Deleted note {note_id}."


# ── Resource ───────────────────────────────────────────────────────────────


@mcp.resource("notes://all")
def all_notes() -> str:
    """All notes as plain text."""
    notes = load_notes()
    if not notes:
        return "No notes yet."
    return "\n\n".join(f"#{n['id']} {n['title']}\n{n['content']}" for n in notes)


# ── Prompt ─────────────────────────────────────────────────────────────────


@mcp.prompt
def summarize_notes() -> str:
    """Ask Claude to summarize all saved notes."""
    return "Use the list_notes tool, then give me a short bullet-point summary of my notes."


if __name__ == "__main__":
    mcp.run()
