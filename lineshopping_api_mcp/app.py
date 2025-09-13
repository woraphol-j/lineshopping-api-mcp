import os
import json
import httpx
from pathlib import Path
from fastmcp import FastMCP


def create_server():
    """Create and configure the LINE Shopping API MCP server."""
    client = httpx.AsyncClient(
        base_url="https://developers-oaplus.line.biz",
        headers={"X-API-KEY": os.getenv("X_API_KEY")}
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
    server.run()


if __name__ == "__main__":
    main()