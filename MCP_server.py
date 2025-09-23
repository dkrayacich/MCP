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
def get_doc(doc_id: str) -> Resource:
    return Resource(uri = f"resource://docs/{doc_id}", 
                    name = f"Doc {doc_id}", 
                    mimeType = "text/plain", 
                    description = "document in the dataset")

@mcp.read_resource("resource://docs/{doc_id}")
def get_contents(doc_id: str) -> List(TextContent):
    return [TextContent(type="text", text=DOCS.get(doc_id, ""))]

class SearchArgs(BaseModel):
    query:str
    k:int = 5

@mcp.tool()
def search(args: SearchArgs) -> Dict:
    q = args.query.lower()
    hits = []
    for doc_id, text in DOCS.items():
        if q in text.lower():
            hits.append({
                "doc_id": doc_id,
                "uri": f"resource://docs/{doc_id}", 
                "snippet": text[:200]
            })
    return {"results": hits[: args.k]}

if __name__ == "__main__":
    mcp.run_stdio()