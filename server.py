"""
MCP Server — Myntra Catalog Tools
Detection signals: McpServer, @server.tool(), StdioServerTransport, from mcp import Server
Asset type: mcp_server
"""
import asyncio
import json
import os
from typing import Any

from mcp import Server
from mcp.server.stdio import StdioServerTransport
from mcp.types import Tool, TextContent

# Initialize MCP Server
server = Server("myntra-catalog-mcp")


@server.tool()
async def search_products(query: str, category: str = "", limit: int = 10) -> list[dict]:
    """Search Myntra product catalog."""
    # In production: calls internal catalog API
    return [{"id": "PROD-001", "name": "Blue Denim Jacket", "price": 1999, "category": category}]


@server.tool()
async def get_product_details(product_id: str) -> dict:
    """Get detailed info for a specific product."""
    return {"id": product_id, "name": "Sample Product", "in_stock": True}


@server.tool()
async def get_user_orders(user_id: str, limit: int = 5) -> list[dict]:
    """Fetch recent orders for a user."""
    return [{"order_id": "ORD-12345", "status": "delivered", "items": 3}]


@server.tool()
async def check_inventory(product_id: str, size: str) -> dict:
    """Check inventory levels for a product/size combination."""
    return {"product_id": product_id, "size": size, "available": True, "quantity": 42}


@server.resource("myntra://catalog/categories")
async def list_categories() -> str:
    """List all available product categories."""
    categories = ["Men", "Women", "Kids", "Home & Living", "Beauty", "Accessories"]
    return json.dumps(categories)


async def main():
    transport = StdioServerTransport()
    await server.run(transport)


if __name__ == "__main__":
    asyncio.run(main())
