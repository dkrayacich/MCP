import json, subprocess, sys, threading
from typing import Any, Dict
import ollama
from mcp.client.stdio import StdioServer

MODEL = "llama3.1"

server = StdioServer(command=[sys.executable, "server.py"])
client = server.start()

tools = client.list_tools().result()

def mcp_tools_to_ollama(tools):
    out = []
    for t in tools.tools:
        out.append({
            "type": "function",
            "function": {
                "name": t.name, 
                "description": t.description or "", 
                "parameters": t.inputSchema or {"type": "object", "properties": {}}
            }
        })
    return out

ollama_tools = mcp_tools_to_ollama(tools)

def call_mcp_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    return client.tool_call(name, arguments).result()

user_q = "Find MCP basics and cite the resource."
resp = ollama.chat(
    MODEL, 
    messages={"role":"user","content":user_q},
    tools=ollama_tools,
)

while resp.get("message", {}).get("tool_calls"):
    tc = resp["message"]["tool_calls"][0]
    result = call_mcp_tool(tc["function"]["name"], json.loads(tc["function"]["arguments"]))

    resp = ollama.chat(
        MODEL,
        messages=[
            {"role":"user","content":user_q},
            {"role":"tool","content":json.dumps(result), "name":tc["function"]["name"]}
        ],
        tools=ollama_tools
    )

print(resp["message"]["content"])
server.stop()