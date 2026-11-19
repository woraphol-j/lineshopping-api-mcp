import os
import unittest
from unittest.mock import patch

import httpx
from fastmcp.exceptions import ToolError

from lineshopping_api_mcp.app import forward_oaplus_api_key


class ForwardOaplusApiKeyTests(unittest.IsolatedAsyncioTestCase):
    async def test_prefers_environment_api_key(self):
        request = httpx.Request("GET", "https://developers-oaplus.line.biz/test")
        environment_api_key = "environment-key/+="

        with (
            patch.dict(os.environ, {"X_API_KEY": environment_api_key}),
            patch(
                "lineshopping_api_mcp.app.get_http_headers",
                return_value={"x-api-key": "client-key"},
            ),
        ):
            await forward_oaplus_api_key(request)

        self.assertEqual(request.headers["X-API-KEY"], environment_api_key)

    async def test_forwards_client_api_key_without_environment_key(self):
        request = httpx.Request("GET", "https://developers-oaplus.line.biz/test")
        client_api_key = "merchant-key/+="

        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "lineshopping_api_mcp.app.get_http_headers",
                return_value={"x-api-key": client_api_key},
            ),
        ):
            await forward_oaplus_api_key(request)

        self.assertEqual(request.headers["X-API-KEY"], client_api_key)

    async def test_forwards_client_api_key_when_environment_key_is_blank(self):
        request = httpx.Request("GET", "https://developers-oaplus.line.biz/test")
        client_api_key = "merchant-key/+="

        with (
            patch.dict(os.environ, {"X_API_KEY": "  "}),
            patch(
                "lineshopping_api_mcp.app.get_http_headers",
                return_value={"x-api-key": client_api_key},
            ),
        ):
            await forward_oaplus_api_key(request)

        self.assertEqual(request.headers["X-API-KEY"], client_api_key)

    async def test_rejects_missing_api_key(self):
        request = httpx.Request("GET", "https://developers-oaplus.line.biz/test")

        with (
            patch.dict(os.environ, {}, clear=True),
            patch("lineshopping_api_mcp.app.get_http_headers", return_value={}),
        ):
            with self.assertRaisesRegex(ToolError, "LINE Shopping API key is required"):
                await forward_oaplus_api_key(request)

        self.assertNotIn("X-API-KEY", request.headers)


if __name__ == "__main__":
    unittest.main()