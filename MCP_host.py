import asyncio, json
import ollama
from fastmcp import Client

MODEL = "llama3.1"

def mcp_tools_to_ollama(tools):
    out = []
    for t in tools:
        out.append({
            "type": "function",
            "function": {
                "name": t.name, 
                "description": t.description or "", 
                "parameters": t.inputSchema or {"type": "object", "properties": {}}
            }
        })
    return out

async def main():
    async with Client("./MCP_server.py") as client:
        tool_objs = await client.list_tools()
        ollama_tools = mcp_tools_to_ollama(tool_objs)

        user_q = "Find MCP basics and cite the resource."
        resp = ollama.chat(
            MODEL, 
            messages={"role":"user","content":user_q},
            tools=ollama_tools,
        )

        while resp.get("message", {}).get("tool_calls"):
            tc = resp["message"]["tool_calls"][0]
            result = await client.call_tool(tc["function"]["name"], json.loads(tc["function"]["arguments"]))

            resp = ollama.chat(
                MODEL,
                messages=[
                    {"role":"user","content":user_q},
                    {"role":"tool","content":json.dumps(result), "name":tc["function"]["name"]}
                ],
                tools=ollama_tools
            )

        print(resp["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())