from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, TextContent
from pydantic import BaseModel

mcp_serv = FastMCP("test_server")

DOCS = {
    "1": "Marbury v. Madison established that courts have the power of judicial review.",
    "2": "Brown v. Board of Education established that segregation in public schools is unconstitutional.",
    "3": "Roe v. Wade established that the Constitution protects a right to privacy regarding abortion.",
    "4": "Miranda v. Arizona established that suspects must be informed of their rights before police questioning.",
    "5": "Gideon v. Wainwright established that states must provide counsel to indigent defendants in criminal cases.",
    "6": "Tinker v. Des Moines established that students do not lose First Amendment rights at school.",
    "7": "United States v. Nixon established that executive privilege is limited and subject to judicial review.",
    "8": "New York Times v. United States established that prior restraint on the press is unconstitutional.",
    "9": "Loving v. Virginia established that bans on interracial marriage violate the Equal Protection Clause.",
    "10": "Obergefell v. Hodges established that same-sex couples have a constitutional right to marry.",
    "11": "Plessy v. Ferguson established that 'separate but equal' facilities were constitutional.",
    "12": "Bush v. Gore established that recount procedures in Florida violated the Equal Protection Clause.",
    "13": "Korematsu v. United States established that internment of Japanese Americans was upheld as constitutional.",
    "14": "Citizens United v. FEC established that corporations have free speech rights in campaign spending.",
    "15": "Texas v. Johnson established that flag burning is protected symbolic speech.",
    "16": "Mapp v. Ohio established that illegally obtained evidence cannot be used in state courts.",
    "17": "McCulloch v. Maryland established that Congress has implied powers under the Necessary and Proper Clause.",
    "18": "Schenck v. United States established that speech creating a clear and present danger is not protected.",
    "19": "Griswold v. Connecticut established that marital privacy is protected from state restrictions on contraception.",
    "20": "Johnson v. Metro Transit established that public transportation must provide equal digital access to riders."
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