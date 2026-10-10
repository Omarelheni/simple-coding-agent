from mcp import Client, StdioServerParameters


class MCPClient:

    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp_server.server"],

        )
        self.client = Client(self.server_params)

    async def __aenter__(self):
        self.client = await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def list_tools(self):
        return await self.client.list_tools()

    async def call_tool(self, name, arguments):
        return await self.client.call_tool(name, arguments)