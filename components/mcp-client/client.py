"""MCP client that connects to downstream MCP servers."""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    server_params = StdioServerParameters(
        command="python",
        args=["../mcp-server/server.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("search_products", {"query": "kurta"})
            print(result)

asyncio.run(run())
