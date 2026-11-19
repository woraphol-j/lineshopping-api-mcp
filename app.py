from lineshopping_api_mcp.app import create_server


mcp = create_server()

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        path="/mcp/",
    )