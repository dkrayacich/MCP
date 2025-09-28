# MCP Server & Host Project

This repository implements a **Model Context Protocol (MCP)** setup consisting of a custom **MCP server** and **MCP host**, designed to extend LLM capabilities by exposing external tools and resources in a structured, reliable way.

The project demonstrates how to:
- Build an MCP server using [FastMCP] with custom resources and tools.  
- Run an MCP host that connects to the server and integrates with an LLM (via [Ollama](https://ollama.ai/)).  
- Enable basic **text-based search** across datasets, where LLMs issue tool calls and incorporate results into their responses.  

---

## 🚀 Features

### **Custom MCP Server**
- Exposes documents/resources as MCP resources.  
- Implements a lightweight text-match search tool.  
- Demonstrates resource handling with `@mcp.resource` and `@mcp.tool` decorators.  

### **MCP Host Integration**
- Connects an LLM (e.g., `llama3.1` via Ollama) to the MCP server.  
- Translates MCP tools into LLM-compatible function calls.  
- Handles tool call responses and passes them back to the model.  

### **Lightweight Search Tool**
- Performs basic keyword lookups across a toy dataset.  
- Shows how LLMs can retrieve external context without embeddings or semantic search.  
