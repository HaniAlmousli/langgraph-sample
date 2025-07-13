#!/usr/bin/env python3
"""
MCP Server for Email Agent Graph
This server exposes the email_agent_graph as MCP tools for Claude Desktop
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from langchain_core.messages import HumanMessage
from graphs.email_agent import email_agent_graph, tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.server_name = "email-agent-mcp"
        self.server_version = "1.0.0"
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "initialize":
            return self._handle_initialize(request_id, params)
        elif method == "tools/list":
            return self._handle_list_tools(request_id, params)
        elif method == "tools/call":
            return await self._handle_call_tool(request_id, params)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method {method} not found"}
            }
    
    def _handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.server_name,
                    "version": self.server_version
                }
            }
        }
    
    def _handle_list_tools(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list tools request"""
        mcp_tools = []
        
        # # Add the main email agent tool
        mcp_tools.append({
            "name": "process_email",
            "description": "Process an email using the email agent graph. This will analyze the email and take appropriate actions like forwarding, sending notifications, or extracting notice data.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "email_content": {
                        "type": "string",
                        "description": "The email content to process"
                    },
                    "user_instructions": {
                        "type": "string",
                        "description": "Optional instructions for how to handle the email"
                    }
                },
                "required": ["email_content"]
            }
        })
        
        # # Add individual tools
        # for tool in tools:
        #     mcp_tools.append({
        #         "name": tool.name,
        #         "description": tool.description,
        #         "inputSchema": {
        #             "type": "object",
        #             "properties": {
        #                 arg: {"type": "string"} for arg in tool.args.keys()
        #             },
        #             "required": list(tool.args.keys())
        #         }
        #     })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": mcp_tools}
        }
    
    async def _handle_call_tool(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call request"""
        try:
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not name:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32602, "message": "Tool name is required"}
                }
            
            # return await self._handle_individual_tool(request_id, name, arguments)
            return await self._handle_email_agent(request_id, arguments)

            # if name == "process_email":
            #     return await self._handle_email_agent(request_id, arguments)
            # else:
            #     # Handle individual tool calls
            #     return await self._handle_individual_tool(request_id, name, arguments)
                
        except Exception as e:
            logger.error(f"Error in tool call: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
    
    async def _handle_email_agent(self, request_id: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the main email agent graph"""
        try:
            email_content = arguments.get("email_content", "")
            user_instructions = arguments.get("user_instructions", "")
            
            # Prepare the initial message
            if user_instructions:
                message = f"User instructions: {user_instructions}\n\nEmail content:\n{email_content}"
            else:
                message = email_content
            
            # Create the initial state for the graph
            initial_state = {
                "messages": [HumanMessage(content=message)]
            }
            
            # Invoke the email agent graph
            result = email_agent_graph.invoke(initial_state)
            
            # Extract the final response
            final_messages = result.get("messages", [])
            if final_messages:
                response = final_messages[-1].content
            else:
                response = "No response generated"
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": response}]
                }
            }
            
        except Exception as e:
            logger.error(f"Error in email agent: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Email agent error: {str(e)}"}
            }
    
    # async def _handle_individual_tool(self, request_id: Any, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    #     """Handle individual tool calls"""
    #     try:
    #         # Find the tool by name
    #         tool = None
    #         for t in tools:
    #             if t.name == name:
    #                 tool = t
    #                 break
            
    #         if not tool:
    #             return {
    #                 "jsonrpc": "2.0",
    #                 "id": request_id,
    #                 "error": {"code": -32602, "message": f"Tool '{name}' not found"}
    #             }
            
    #         # Execute the tool
    #         result = tool.invoke(arguments)
            
    #         # Format the result
    #         if isinstance(result, dict):
    #             result_text = json.dumps(result, indent=2)
    #         else:
    #             result_text = str(result)
            
    #         return {
    #             "jsonrpc": "2.0",
    #             "id": request_id,
    #             "result": {
    #                 "content": [{"type": "text", "text": result_text}]
    #             }
    #         }
            
    #     except Exception as e:
    #         logger.error(f"Error executing tool {name}: {str(e)}")
    #         return {
    #             "jsonrpc": "2.0",
    #             "id": request_id,
    #             "error": {"code": -32603, "message": f"Tool execution error: {str(e)}"}
    #         }

async def main():
    """Main function to run the MCP server"""
    server = MCPServer()
    
    # Read from stdin and write to stdout for MCP communication
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # Write response to stdout
            await asyncio.get_event_loop().run_in_executor(None, lambda: sys.stdout.write(json.dumps(response) + "\n"))
            await asyncio.get_event_loop().run_in_executor(None, sys.stdout.flush)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            await asyncio.get_event_loop().run_in_executor(None, lambda: sys.stdout.write(json.dumps(error_response) + "\n"))
            await asyncio.get_event_loop().run_in_executor(None, sys.stdout.flush)

if __name__ == "__main__":
    asyncio.run(main()) 