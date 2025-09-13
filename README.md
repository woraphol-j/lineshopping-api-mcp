
# LINE Shopping API MCP Server

MCP Server for the LINE Shopping API, enabling AI agents and tools to interact with LINE Shopping data and operations via the Model Context Protocol. This server provides tools for managing products, inventory, orders, settlements, and more, using the official LINE Shopping API.

## Features

- **Product Management**: Search, create, update, and delete products and variants
- **Inventory Management**: Adjust, increase, or decrease inventory levels
- **Order Management**: Query, view, cancel, and update orders
- **Settlement**: Retrieve settlement details for orders
- **OpenAPI Integration**: All tools are auto-generated from the OpenAPI spec


## Prerequisites

1. Python >= 3.13
2. [uv](https://github.com/astral-sh/uv) (Python package manager)
3. LINE Shopping API Key (`X_API_KEY`)


## Installation

### Method 1: Using uvx (Recommended)

Install and run directly from PyPI using `uvx`:

```sh
# Install and run the MCP server (note the different executable name)
uvx --from lineshopping-api-mcp lineshopping-mcp
```

Or run with environment variables:

```sh
# Set your API key and run
X_API_KEY=your_api_key_here uvx --from lineshopping-api-mcp lineshopping-mcp
```

### Method 2: Clone and Run

1. **Clone the repository:**
	```sh
	git clone https://github.com/woraphol-j/lineshopping-api-mcp.git
	cd lineshopping-api-mcp
	```

2. **Install dependencies:**
	```sh
	uv add fastmcp httpx
	```

3. **Run the server:**
	```sh
	# Set your API key and run
	X_API_KEY=your_api_key_here uv run --with fastmcp fastmcp run app.py
	```

### Environment Configuration

For persistent configuration, create a `.env` file in your working directory:
```env
X_API_KEY=your_api_key_here
```


## Configuration & Integration

### Using uvx (PyPI Installation)

Configure your agent to use the PyPI-installed package:

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
			"command": "uvx",
			"args": [
				"--from",
				"lineshopping-api-mcp",
				"lineshopping-mcp"
			],
			"env": {
				"X_API_KEY": "${input:line-shopping-api-key}"
			}
		}
	}
}
```

### Using Local Clone

For local development or cloned repository:

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
			"command": "uv",
			"args": [
				"run",
				"--with",
				"fastmcp",
				"fastmcp",
				"run",
				"/Users/xxx/lineshopping-api-mcp/app.py"
			],
			"env": {
				"X_API_KEY": "${input:line-shopping-api-key}",
				"FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER": "true"
			}
		}
	}
}
```

## Available Tools

The following tools are exposed by the MCP server (see `openapi.json` for full details):

### Checkout & Links
- `create-checkout-link`: Generate a checkout link for order items

### Inventory Management
- `adjust-inventory`: Adjust inventory by ID
- `decrease-inventory`: Decrease inventory by ID
- `increase-inventory`: Increase inventory by ID

### Order Management
- `get-orders`: List orders with advanced filtering
- `get-order-detail`: Get details for a specific order
- `cancel-order`: Cancel an order
- `mark-order-paid`: Mark order as paid (COD)
- `mark-order-shipped`: Mark order as shipped and add tracking number
- `print-parcel-label`: Download parcel label for an order
- `send-order-message`: Send message via OA Plus flex message
- `update-shipment`: Update shipping tracking number

### Product Management
- `get-products`: List/search products
- `create-product`: Create a new product
- `delete-product`: Delete a product
- `update-product-detail`: Update product details
- `delete-product-variant`: Delete a product variant
- `update-product-display-status`: Update product's display status (onsale/hide)
- `update-product-price`: Update product price and instant discount
- `update-product-variant-detail`: Update product variant details
- `create-product-variants`: Create product variants

### Settlement
- `get-settlement-detail`: Get settlement details for an order

Refer to [`openapi.json`](./openapi.json) for all available tools, input parameters, and response formats.

## Debugging

If you run into issues, check your agent platform's MCP logs for errors. Common issues:
- **Authentication Errors**: Verify your API key and environment variable setup
- **API Errors**: Check rate limits, input formats, and required fields


## Development

### Local Development

```sh
# Clone the repository
git clone https://github.com/woraphol-j/lineshopping-api-mcp.git
cd lineshopping-api-mcp

# Install dependencies
uv add fastmcp httpx

# Run the server (with fastmcp)
X_API_KEY=your_api_key_here uv run --with fastmcp fastmcp run app.py
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
This project is not an HTTP REST API server. It is an MCP server for agent integrations. For more details, see [FastMCP](https://github.com/line/fastmcp) and [LINE Shopping API](https://developers-oaplus.line.biz).
