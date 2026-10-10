from app.tools.registry import TOOLS_SCHEMA,execute_tool
from app.agent.constants import SYSTEM_MESSAGE
from app.llm.client import call_llm
from app.agent.state import AgentState
import json
from app.mcp_client.client import MCPClient

client = MCPClient()

async def run_agent(task):
    state = AgentState(
        task=task,
        messages = [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            },
            {
                "role": "user",
                "content": task
            }
    ])

    while state.turn < state.max_turns:
        state.turn += 1

        response = call_llm(state.messages, TOOLS_SCHEMA)
        message = response.choices[0].message
        state.messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    }
                }
                for tool_call in (message.tool_calls or [])
            ]
        })
        async with MCPClient() as mcp_client:
            if not message.tool_calls:
                return message.content

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                try:
                    result = await execute_tool(mcp_client, tool_name, arguments)
                except Exception as e:
                    result = f"Error executing {tool_name}: {str(e)}"
                print(f"Tool {tool_name} executed with result: {result}")
                state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Tool {tool_name} executed with result: {result}"
                })

        
    return "Maximum number of turns reached without completing the task."