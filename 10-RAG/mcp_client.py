"""MCP client — a Gemini agent that uses tools from our MCP servers.

Up to now we built SERVERS. Now we build the CLIENT:

    1. List the MCP servers we want to use  -> SERVERS = {...}
    2. Connect to all of them               -> Client(SERVERS)
    3. Ask them which tools they have       -> client.list_tools()
    4. Give those tools to Gemini           -> Gemini decides WHICH tool to call
    5. Call that tool on the MCP server     -> client.call_tool(...)
    6. Send the result back to Gemini       -> Gemini writes the final answer

Run:   uv run mcp_client.py
"""

import asyncio

from dotenv import load_dotenv
from fastmcp import Client
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"

# ---- The MCP servers we want to use ----
# Same format as the Claude Desktop config. Add more servers here.
SERVERS = {
    "mcpServers": {
        "uniassist": {
            "command": "uv",
            "args": ["--directory", "/home/leapfrog/AI-GenAI-labs/10-RAG", "run", "mcp_server.py"],
        },
        "notes": {
            "command": "uv",
            "args": ["--directory", "/home/leapfrog/AI-GenAI-labs/11-MCP", "run", "server.py"],
        },
    }
}

gemini = genai.Client()  # reads GOOGLE_API_KEY from .env
client = Client(SERVERS)  # one client for ALL the servers


async def ask(question: str) -> str:
    async with client:
        # ---- Get the tools from all servers ----
        # With more than one server, tool names get the server name in front,
        # e.g. "uniassist_search_policies" and "notes_add_note".
        mcp_tools = await client.list_tools()
        print("Tools:", [tool.name for tool in mcp_tools])

        # ---- Turn MCP tools into Gemini tools ----
        gemini_tools = []
        for tool in mcp_tools:
            gemini_tools.append(
                types.FunctionDeclaration(
                    name=tool.name,
                    description=tool.description,
                    parameters_json_schema=tool.input_schema,
                )
            )
        config = types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=gemini_tools)]
        )

        # ---- Ask Gemini ----
        contents = [types.Content(role="user", parts=[types.Part(text=question)])]
        response = gemini.models.generate_content(
            model=MODEL_NAME, contents=contents, config=config
        )

        # No tool needed? Then Gemini already answered.
        if not response.function_calls:
            return response.text

        # ---- Gemini picked a tool: we call it on the MCP server ----
        contents.append(response.candidates[0].content)

        for function_call in response.function_calls:
            print(f"Calling: {function_call.name}({function_call.args})")
            result = await client.call_tool(function_call.name, function_call.args)

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": result.content[0].text},
                        )
                    ],
                )
            )

        # ---- Gemini reads the tool result and answers ----
        final_response = gemini.models.generate_content(
            model=MODEL_NAME, contents=contents, config=config
        )
        return final_response.text


if __name__ == "__main__":
    print(asyncio.run(ask("How many credits do I need to graduate?")))
    print()
    print(asyncio.run(ask("What notes do I have?")))
