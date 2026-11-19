
# LINE Shopping API MCP Server

MCP Server for the LINE Shopping API, enabling AI agents and tools to interact with LINE Shopping data and operations via the Model Context Protocol. This server provides tools for managing products, inventory, orders, settlements, and more, using the official LINE Shopping API.

## Features

- **Product Management**: Search, create, update, and delete products and variants
- **Inventory Management**: Adjust, increase, or decrease inventory levels
- **Order Management**: Query, view, cancel, and update orders
- **Settlement**: Retrieve settlement details for orders
- **OpenAPI Integration**: All tools are auto-generated from the OpenAPI spec


## Prerequisites

1. Python >= 3.11
2. [uv](https://github.com/astral-sh/uv) (Python package manager)
3. LINE Shopping API key, supplied in the MCP request's `X-API-KEY` header or through the optional `X_API_KEY` environment variable


## Installation

### Method 1: Using uvx (Recommended)

Install and run directly from PyPI using `uvx`:

```sh
# Run the Streamable HTTP server at http://127.0.0.1:8000/mcp/
uvx --from lineshopping-api-mcp lineshopping-mcp
```

### Method 2: Clone and Run

1. **Clone the repository:**
	```sh
	git clone https://github.com/woraphol-j/lineshopping-api-mcp.git
	cd lineshopping-api-mcp
	```

2. **Install dependencies:**
	```sh
	uv sync
	```

3. **Run the server:**
	```sh
	uv run fastmcp run app.py --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp/
	```

### Authentication

LINE API tool calls need the merchant's API key in the incoming MCP request:

```http
X-API-KEY: <merchant-api-key>
```

The server forwards this header to the corresponding OAPlus API request. If the `X_API_KEY` environment variable is set to a non-blank value, it takes precedence over the request header. Otherwise, each request can provide its own key. A missing key fails the LINE API tool call; MCP initialization and tool discovery do not require one.


## Configuration & Integration

### Connect an MCP client

Start the local Streamable HTTP server:

```sh
uv run fastmcp run app.py --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp/
```

Configure the client to send its merchant key as an HTTP header:

```jsonc
{
	"inputs": [
		{
			"type": "promptString",
			"id": "line-shopping-api-key",
			"description": "LINE Shopping API Key",
			"password": true
		}
	],
	"servers": {
		"LINE Shopping API MCP": {
			"type": "http",
			"url": "http://127.0.0.1:8000/mcp/",
			"headers": {
				"X-API-KEY": "${input:line-shopping-api-key}"
			}
		}
	}
}
```

For GitHub repository MCP settings, configure a reachable Streamable HTTP endpoint. GitHub's cloud agent cannot reach a local `127.0.0.1` server directly.

## Available Tools

The following tools are generated from the packaged OpenAPI spec at [`lineshopping_api_mcp/openapi.json`](./lineshopping_api_mcp/openapi.json):

### Checkout & Links
- `Create_checkout_link`: Generate a checkout link for order items

### Inventory Management
- `Adjust_inventory`: Adjust inventory by ID
- `Decrease_inventory`: Decrease inventory by ID
- `Increase_inventory`: Increase inventory by ID

### Order Management
- `Get_all_orders`: List orders with advanced filtering
- `Order_detail`: Get details for a specific order
- `Cancel_Order`: Cancel an order
- `Confirm_order_delivery`: Confirm order delivery
- `Mark_as_paid_COD`: Mark order as paid (COD)
- `Mark_as_ship`: Mark order as shipped
- `Print_parcel_label`: Download parcel label for an order
- `Send_message_via_OA_Plus_flex_message_services`: Send an OA Plus message
- `Update_tracking_number`: Update the shipment tracking number

### Product Management
- `Get_all_products`: List/search products
- `Create_product`: Create a product
- `Delete_product`: Delete a product
- `Update_product_detail`: Update product details
- `Delete_product_variant`: Delete a product variant
- `Update_products_display_status`: Update product display status
- `Update_product_price`: Update product price and instant discount
- `Update_product_variant_detail`: Update product variant details
- `Create_product_variants`: Create product variants

### Settlement
- `Settlement_detail`: Get settlement details for an order

The server loads the packaged OpenAPI file above. The root-level [`openapi.json`](./openapi.json) is only a fallback if the packaged file is absent.

## Debugging

If you run into issues, check your agent platform's MCP logs for errors. Common issues:
- **Authentication Errors**: Verify the `X-API-KEY` request header or optional `X_API_KEY` environment variable
- **API Errors**: Check rate limits, input formats, and required fields


## Development

### Local Development

```sh
# Clone the repository
git clone https://github.com/woraphol-j/lineshopping-api-mcp.git
cd lineshopping-api-mcp

# Install dependencies
uv sync

# Run the server (with fastmcp)
uv run fastmcp run app.py --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp/
```

### Building and Publishing

```sh
# Build the package
uv build

# Publish to PyPI (requires API token)
uv publish --token your_pypi_token
```

## Dependencies

- fastmcp - MCP protocol implementation
- httpx - HTTP client for API requests

## License

MIT

---
This project is not an HTTP REST API server. It is an MCP server for agent integrations. For more details, see [FastMCP](https://gofastmcp.com/) and [LINE Shopping API](https://developers-oaplus.line.biz).
