#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 2025-09-26 17:13:32

@author: Nikhil Kapila

Description: MCP server to control your Helvar DALI system using an LLM.... because why not?
"""

import asyncio
import logging
import click

from fastmcp import FastMCP

from aiohelvar.router import Router

mcp = FastMCP("mcp-helvarnet: control your Helvar DALI system")
router: Router | None = None

@click.command()
@click.option("--host", "-h", default="localhost", help="router host/ip address")
@click.option("--port", "-p", default=50000, type=int, help="router port for helvarnet (default: 50000 TCP or 50001 UDP)")
def cli(host, port):
    # incoming hostname and path from command line arguments
    # TODO: trivial: check if no cmdline args, use env vars
    asyncio.run(main(host, port))

async def main(host, port):
    """
    This function acts like an entry point to parse command line arguments before the MCP server starts. Function should exit or perhaps try again if router connect fails.

    Further, the library guarantees that a connection remains alive thanks to the asyncio task.
    """

    global router
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

    router = Router(host, port)

    try:
        await router.connect()
        await router.initialize()
        logging.info("Router connected successfully. Starting MCP server.")
        
        # Keep the connection alive and monitor for updates in background
        # The aiohelvar library automatically handles broadcast messages
        # and updates internal state when the connection stays alive
        mcp.run()

    except Exception as e:
        logging.error(f"Failed to connect to router: {e}")
        logging.warning("Starting server without router connection")
        # TODO: check how good performance is before I look into reconnects


if __name__ == "__main__":
    cli()
