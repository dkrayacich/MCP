from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, TextContent
from pydantic import BaseModel

mcp_serv = FastMCP("test_server")

DOCS = {
    "1": "MCP is an open protocol for connecting models to tools and data.",
    "2": "Resources in MCP are addressable by URI and provide context.",
    "3": "Tools in MCP let models call functions like search or lookup."
}

@mcp_serv.resource("resource://docs/{doc_id}")
def get_doc(doc_id: str) -> Resource:
    return Resource(uri = f"resource://docs/{doc_id}", 
                    name = f"Doc {doc_id}", 
                    mimeType = "text/plain", 
                    description = "document in the dataset")

@mcp_serv.resource("resource://docs/{doc_id}")
def get_contents(doc_id: str) -> str:
    return DOCS.get(doc_id, "")

class SearchArgs(BaseModel):
    query:str
    k:int = 5

@mcp_serv.tool("search", input_model=SearchArgs)
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
    mcp_serv.run()