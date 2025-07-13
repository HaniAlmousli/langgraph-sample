#!/usr/bin/env python3
"""
Test script for the MCP server
This script tests the MCP server functionality locally
"""

import asyncio
import json
import sys
from mcp_server import MCPServer

async def test_mcp_server():
    """Test the MCP server functionality"""
    server = MCPServer()
    
    # Test 1: Initialize
    print("Testing initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    init_response = await server.handle_request(init_request)
    print(f"Init response: {json.dumps(init_response, indent=2)}")
    
    # Test 2: List tools
    print("\nTesting list tools...")
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    list_response = await server.handle_request(list_request)
    print(f"List tools response: {json.dumps(list_response, indent=2)}")
    
    # Test 3: Process email
    print("\nTesting email processing...")
    email_content = """
    From: debby@stack.com
    Hey Betsy,
    Here's your invoice for $1000 for the cookies you ordered.
    """
    
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "process_email",
            "arguments": {
                "email_content": email_content,
                "user_instructions": "Process this invoice email"
            }
        }
    }
    call_response = await server.handle_request(call_request)
    print(f"Call tool response: {json.dumps(call_response, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 