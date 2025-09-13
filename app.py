import os, json, httpx
from fastmcp import FastMCP

client = httpx.AsyncClient(
    base_url="https://developers-oaplus.line.biz",
    headers={"X-API-KEY": os.getenv("X_API_KEY")}
)

with open("./openapi.json", "r") as f:
    openapi_spec = json.load(f)

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="LINE Shopping API MCP server",
)

if __name__ == "__main__":
    mcp.run()