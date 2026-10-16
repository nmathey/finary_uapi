"""Client de test du serveur MCP Finary (sans Node.js).
Usage : python test_client.py [url] [outil]
Variable optionnelle : MCP_AUTH_TOKEN (envoyé en Bearer)
"""
import asyncio
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/mcp"
TOOL = sys.argv[2] if len(sys.argv) > 2 else "finary_me"


async def main():
    token = os.environ.get("MCP_AUTH_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else None
    async with streamablehttp_client(URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"{len(tools.tools)} outils disponibles")
            result = await session.call_tool(TOOL, {})
            text = result.content[0].text
            print(f"--- {TOOL} (isError={result.isError}) ---")
            print(text[:1500] + ("\n[...tronqué]" if len(text) > 1500 else ""))


asyncio.run(main())
