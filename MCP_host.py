import json, subprocess, sys, threading
from typing import Any, Dict
import ollama
from mcp.client.stdio import StdioServer

MODEL = "llama3.1"