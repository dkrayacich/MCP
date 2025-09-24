import json, subprocess, sys, threading
from typing import Any, Dict
import ollama
from mcp.client.stdio import StdioServer

MODEL = "llama3.1"

server = StdioServer(command=[sys.executable, "server.py"])
client = server.start()

tools = client.list_tools().result()