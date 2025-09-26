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
from typing import Dict, List

from fastmcp import FastMCP
from aiohelvar.router import Router

mcp = FastMCP("mcp-helvarnet: control your Helvar DALI system")


@click.command()
@click.option("--host", "-h", default="localhost", help="router host/ip address")
@click.option("--port", "-p", default=8080, type=int, help="router port")
def cli(host, port):
    # incoming hostname and path from command line arguments
    # TODO: trivial: check if no cmdline args, use env vars
    asyncio.run(main(host, port))


async def main(host, port):
    """
    This function acts like an entry point to parse command line arguments before the MCP server starts. Function should exit or perhaps try again if router connect fails.

    Further, the library guarantees that a connection remains alive thanks to the asyncio task.
    """

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

    router = Router(host, port)

    try:
        await router.connect()
        await router.initialize()
        mcp.run()

    except Exception as e:
        logging.error(f"Failed to connect to router: {e}")
        return


if __name__ == "__main__":
    cli()
