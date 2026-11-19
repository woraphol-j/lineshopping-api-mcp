import json
import os
import httpx
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers


async def forward_oaplus_api_key(request: httpx.Request) -> None:
    environment_api_key = os.getenv("X_API_KEY")
    api_key = (
        environment_api_key
        if environment_api_key is not None and environment_api_key.strip()
        else get_http_headers().get("x-api-key")
    )
    if api_key is None or not api_key.strip():
        raise ToolError("LINE Shopping API key is required")

    request.headers["X-API-KEY"] = api_key


def create_server():
    """Create and configure the LINE Shopping API MCP server."""
    client = httpx.AsyncClient(
        base_url="https://developers-oaplus.line.biz",
        event_hooks={"request": [forward_oaplus_api_key]},
    )

    # Get the package directory to find openapi.json
    package_dir = Path(__file__).parent
    openapi_path = package_dir / "openapi.json"

    # Fallback to current directory for backwards compatibility
    if not openapi_path.exists():
        openapi_path = Path("./openapi.json")

    with open(openapi_path, "r") as f:
        openapi_spec = json.load(f)

    # Create the MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="LINE Shopping API MCP server",
    )

    return mcp


def main():
    """Main entry point for the CLI."""
    server = create_server()
    server.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        path="/mcp/",
    )


if __name__ == "__main__":
    main()