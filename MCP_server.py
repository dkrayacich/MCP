from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, TextContent
from pydantic import BaseModel

mcp_serv = FastMCP("test_server")

DOCS = {
    "1": "LeBron James averaged 27 points, 7 rebounds, and 9 assists.",
    "2": "Stephen Curry averaged 30 points, 5 rebounds, and 6 assists.",
    "3": "Giannis Antetokounmpo averaged 29 points, 11 rebounds, and 5 assists.",
    "4": "Nikola Jokic averaged 26 points, 12 rebounds, and 9 assists.",
    "5": "Luka Doncic averaged 32 points, 8 rebounds, and 8 assists.",
    "6": "Joel Embiid averaged 33 points, 10 rebounds, and 4 assists.",
    "7": "Kevin Durant averaged 29 points, 7 rebounds, and 5 assists.",
    "8": "Kawhi Leonard averaged 24 points, 6 rebounds, and 4 assists.",
    "9": "Jayson Tatum averaged 28 points, 8 rebounds, and 4 assists.",
    "10": "Jimmy Butler averaged 23 points, 6 rebounds, and 5 assists.",
    "11": "Ja Morant averaged 27 points, 6 rebounds, and 8 assists.",
    "12": "Damian Lillard averaged 32 points, 4 rebounds, and 7 assists.",
    "13": "Anthony Davis averaged 25 points, 11 rebounds, and 3 blocks.",
    "14": "Zion Williamson averaged 26 points, 7 rebounds, and 4 assists.",
    "15": "Devin Booker averaged 28 points, 5 rebounds, and 5 assists.",
    "16": "Donovan Mitchell averaged 27 points, 4 rebounds, and 5 assists.",
    "17": "Shai Gilgeous-Alexander averaged 31 points, 5 rebounds, and 6 assists.",
    "18": "Kyrie Irving averaged 26 points, 4 rebounds, and 6 assists.",
    "19": "James Harden averaged 22 points, 6 rebounds, and 10 assists.",
    "20": "Jaylen Brown averaged 26 points, 7 rebounds, and 3 assists."
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

@mcp_serv.tool()
def search(query:str, k:int = 5) -> Dict:
    q = query.lower()
    hits = []
    for doc_id, text in DOCS.items():
        if q in text.lower():
            hits.append({
                "doc_id": doc_id,
                "uri": f"resource://docs/{doc_id}", 
                "snippet": text[:200]
            })
    return {"results": hits[: k]}

if __name__ == "__main__":
    mcp_serv.run()