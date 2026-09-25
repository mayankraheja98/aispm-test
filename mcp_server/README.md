# Myntra MCP Server
Exposes Myntra's internal catalog, orders, and inventory APIs as MCP tools
for use by AI agents (Claude, Cursor, etc.).

**Asset type:** MCP Server
**Tools exposed:** search_products, get_product_details, get_user_orders, check_inventory
**Transport:** stdio (local agents) + SSE (remote agents)
