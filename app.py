import os
import json

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()  # Load environment variables from .env

api_key = os.getenv("X_API_KEY")  # Get the API key

# Create an HTTP client for your API with the header
client = httpx.AsyncClient(
    base_url="https://developers-oaplus.line.biz",
    headers={"X-API-KEY": api_key}
)

# Load your OpenAPI spec
with open("./openapi.json", "r") as f:
    openapi_spec = json.load(f)

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="LINE Shopping API MCP server",
    timeout=30.0
)

if __name__ == "__main__":
    mcp.run()