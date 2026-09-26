# UniAssist: RAG + MCP

UniAssist answers students' questions about university policies (attendance,
grading, exams, scholarships, and more) using **RAG** (Retrieval-Augmented Generation).

In this lab we go in three steps:

1. **Build a RAG application**: find the right policy text and let Gemini answer from it.
2. **Turn the retriever into an MCP server**: so *any* AI app can use our search.
3. **Write our own MCP client**: a Gemini agent that uses the MCP server's tools.

```
Step 1: RAG app          question ──► retrieve ──► Gemini ──► answer

Step 2: MCP server       [ search_policies tool ]  ◄── any MCP client can call it

Step 3: MCP client       question ──► Gemini ──► "call search_policies" ──► MCP server
                                        ▲                                    │
                                        └────────── policy text ◄────────────┘
```

---

## Project structure

```
10-RAG/
├── data/                  ← the university policy documents (.md)
├── src/
│   ├── indexing/          ← load → chunk → embed → store in Qdrant (run once)
│   ├── retrival/          ← embed query → search Qdrant → rerank
│   ├── agumentation/      ← build the context + prompt
│   ├── generation/        ← call Gemini
│   └── rag_pipeline.py    ← Step 1: the full RAG app
├── mcp_server.py          ← Step 2: the retriever as an MCP server
├── mcp_client.py          ← Step 3: our own MCP client (Gemini agent)
├── evals/ + golden/       ← (optional) evaluating the RAG with DeepEval
└── .env.example           ← the keys you need
```

---

## Setup

**1. Install [uv](https://docs.astral.sh/uv/)**, then install the dependencies from inside this folder:

```bash
cd 10-RAG
uv sync
```

**2. Create your `.env` file** from the example and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Where to get it |
|---|---|
| `QDRANT_URL`, `QDRANT_API_KEY` | Create a free cluster at [cloud.qdrant.io](https://cloud.qdrant.io) |
| `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |
| `SSL_CERT_FILE` | **Only** if you see `CERTIFICATE_VERIFY_FAILED` (see [Troubleshooting](#troubleshooting)) |

Never commit your `.env` file. It is already in `.gitignore`.

**3. Put the documents into Qdrant** (you only need to do this once):

```bash
uv run python -m src.indexing.load_data_to_vector_store
```

This reads every file in `data/`, splits it into chunks, turns each chunk into a
vector and saves it in a Qdrant collection called `uniassist`.

> **First run is slow:** the embedding and reranker models are downloaded from
> Hugging Face. After that they are cached.

---

## Step 1: The RAG application

```bash
uv run python -m src.rag_pipeline
```

What happens inside `RagPipeline.invoke()`:

| # | Step | File |
|---|---|---|
| 1 | Turn the question into a vector | `src/retrival/query_embedder.py` |
| 2 | Find the 10 closest chunks in Qdrant | `src/retrival/retriver.py` |
| 3 | Rerank them and keep the best ones | `src/retrival/reranker.py` |
| 4 | Build the context + prompt | `src/agumentation/` |
| 5 | Gemini writes the answer from the context | `src/generation/` |

---

## Step 2: The MCP server

**Idea:** we don't rewrite the RAG. We take the retrieval part (steps 1–3) and
expose it as an MCP **tool** called `search_policies`. The tool returns the
policy text; the *client's* LLM writes the answer.

Look at `mcp_server.py`. It's just our existing functions wrapped with `@mcp.tool`:

```python
@mcp.tool
def search_policies(query: str) -> str:
    """Search the university policy documents ..."""   # ← the AI reads this!
    query_vector = embed_query(query)
    candidates = retrieve(query_vector=query_vector, top_k=10)
    best_chunks = reranker(query=query, results=candidates, top_k=3)
    ...
```

### Test it in the MCP Inspector

```bash
uv run fastmcp dev inspector mcp_server.py
```

A browser page opens. Click **Connect** → **Tools** → `search_policies`, type a
question and run it. You are calling the tool by hand, with no LLM involved.

> The server takes **~20 seconds** to start because it loads two ML models.
> Wait for it; it's not broken.

### Use it from Claude Desktop

Open **Claude Desktop → Settings → Developer → Edit Config** and add:

```json
{
  "mcpServers": {
    "uniassist": {
      "command": "/absolute/path/to/uv",
      "args": ["--directory", "/absolute/path/to/10-RAG", "run", "mcp_server.py"]
    }
  }
}
```

- Find your uv path with `which uv` (macOS/Linux) or `where uv` (Windows).
- Use **absolute paths**.
- No `env` block needed: the server reads your `.env` by itself.
- Fully quit and reopen Claude Desktop, then ask: *"How many credits do I need to graduate?"*

---

## Step 3: Our own MCP client

Claude Desktop is an MCP client someone else wrote. Now we write our own with Gemini.

```bash
uv run mcp_client.py
```

**Before running:** open `mcp_client.py` and change the paths in `SERVERS`
to where the folders are on *your* computer. The `notes` server comes from
[`11-MCP`](../11-MCP); remove it if you don't have that lab set up.

### What a client does

An LLM can only *reply with text*. It cannot call tools by itself.
The client is the messenger between the LLM and the MCP servers:

| Job | In the code |
|---|---|
| 1. **Connect** to the servers | `client = Client(SERVERS)` |
| 2. **List** their tools | `await client.list_tools()` |
| 3. **Translate** MCP tools into Gemini's format | the `types.FunctionDeclaration` loop |
| 4. **Ask** Gemini (question + tools) | `gemini.models.generate_content(...)` |
| 5. **Call** the tool Gemini picked | `await client.call_tool(name, args)` |
| 6. **Send the result back**; Gemini writes the answer | `Part.from_function_response(...)` |

**Why translate?** Gemini doesn't know about MCP. It has its own tool format.
Luckily both use the same three things (`name`, `description`, and a JSON Schema
for the arguments), so translating is just copying fields.

### Many servers, one client?

The MCP architecture says **one client per server**. `Client(SERVERS)` still
follows that rule: FastMCP opens one connection per server behind the scenes
and gives you a single object to use. That's why tool names get the server
name in front: `uniassist_search_policies`, `notes_list_notes`, …

> ⚠️ The Notes server can **add and delete** real notes. Try read-only
> questions first, like *"What notes do I have?"*

---

## Try it yourself

1. Ask `mcp_client.py` a question that needs **no** tool (e.g. *"What is 2 + 2?"*). What happens?
2. Change `top_k=3` to `top_k=5` in `mcp_server.py`. Does the answer change?
3. Add a second tool to `mcp_server.py`, e.g. `list_policy_topics()`, and see if Gemini uses it.
4. Right now the client does only **one** round of tool calls. Wrap it in a
   `while response.function_calls:` loop so Gemini can call tools several times.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `CERTIFICATE_VERIFY_FAILED: self-signed certificate` (or `Cannot send a request, as the client has been closed`) | Your network inspects SSL traffic. Add `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt` to `.env` (Linux path; ask your IT team for macOS/Windows). |
| `Failed to spawn: fastmcp` | You are in the wrong folder. `cd 10-RAG` first. |
| `No module named 'sentence_transformers'` (or any other package) | You ran plain `python` with a *different* venv active (e.g. the repo-root `.venv`). Use `uv run python ...`, or `deactivate` and then `source .venv/bin/activate` inside `10-RAG`. |
| Inspector / client says *Connection closed* | The server crashed on start. Run `uv run mcp_server.py` on its own to see the real error. |
| Inspector times out | The models take ~20 s to load. Increase the request timeout in the Inspector's **Configuration**. |
| `No API key was provided` | Check `GOOGLE_API_KEY` in `.env`. |
