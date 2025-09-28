# mcp-helvarnet
a MCP server to control and potentially commission your Helvar Lighting System

> [!CAUTION]
> Helvar™ is a registered trademark of Helvar Ltd.
> This software is an independent, unofficial project and is not affiliated with,
> supported, or endorsed by Helvar Ltd. in any capacity. The use of the Helvar™ trademark is for the sole purpose of identifying compatibility and does not imply any official relationship with the company.

# Video demonstration
[YouTube Link](https://youtu.be/cjotGWdjD44)

https://github.com/user-attachments/assets/c3c06a4f-2fa1-4a84-88c4-994899bbfe3c

# Attribution
Thank you to the following libraries for making this project possible.
- [FastMCP](https://gofastmcp.com/getting-started/welcome): FastMCP makes it easier to make Python MCP servers!
- [aiohelvar](https://github.com/tomplayford/aiohelvar): aiohelvar by Tom Playford 

# Installation
Locate your MCP config path [here](https://modelcontextprotocol.io/quickstart/user) or check your MCP client settings.

## Using Docker (recommended)
Coming soon, our Thala should be working on it soon

## Run Directly via `uvx`
This is the easiest and quickest method. You need to install [uv](https://docs.astral.sh/uv/) for this to work. <br>
Add this to your MCP server configuration:
```
{
  "mcpServers": {
    "mcp-helvarnet":{
      "command": "uvx",
        "args": [
          "--python=3.10",
          "--from",
          "git+https://github.com/nkapila6/mcp-helvarnet",
          "mcp-helvarnet"
        ]
      }
  }
}
```

# MCP Clients
The MCP server should work with any MCP client that supports tool calling. Has been tested on the below clients.

- Claude Desktop
- Cursor
- Goose
- Others? You try!

# Contributing
Have ideas or want to improve this project? Issues, feature requests and pull requests are welcome!

# License
This project is licensed under the GNU GPLv3 License.

