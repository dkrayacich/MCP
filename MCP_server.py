from typing import List, Dict
from mcp.server.fastmcp import FastMCP, Resource, TextContent
from pydantic import BaseModel

mcp = FastMCP("test_server")

DOCS = {
    "1": "MCP is an open protocol for connecting models to tools and data.",
    "2": "Resources in MCP are addressable by URI and provide context.",
    "3": "Tools in MCP let models call functions like search or lookup."
}

@mcp.resource("resource://docs/{doc_id}")
def get_doc(doc_id: str)