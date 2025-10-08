#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 2025-09-26 17:13:32

@author: Nikhil Kapila

Description: MCP server to control your Helvar DALI system using an LLM.... because why not?
"""

from contextlib import asynccontextmanager
import logging
import os

from aiohelvar.router import Router
from fastmcp import FastMCP
import click

from .info import register_info_tools
from .devices import register_device_tools
from .groups import register_group_tools
# from .scenes import register_scene_tools #TODO

router: Router | None = None

def get_router()->Router:
    if router is None:
        raise RuntimeError("Router not initialized. Please configure router connection first.")
    return router

@asynccontextmanager
async def lifespan(app: FastMCP, host: str, port: int):
    """Manage the router connection lifecycle."""
    global router

    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])

    try:
        logging.info("Connecting to router at %s:%d...", host, port)
        router = Router(host, port)
        await router.initialize()
        logging.info("Router connected successfully.")
        yield
    except Exception as e:
        logging.error(f"Failed to connect to router: %s", e)
        logging.warning("Continuing without router connection.")
        # router = None
        yield

HELVAR_HOST = os.getenv("HELVAR_HOST", "192.168.1.129")
HELVAR_PORT = int(os.getenv("HELVAR_PORT", "50000"))

# from https://gofastmcp.com/integrations/fastapi#combining-lifespans
mcp = FastMCP(
    "mcp-helvarnet: control your Helvar DALI system",
    lifespan=lambda app: lifespan(app, HELVAR_HOST, HELVAR_PORT),
)

register_info_tools(mcp, get_router)
register_device_tools(mcp, get_router)
register_group_tools(mcp, get_router)

@click.command()
@click.option(
    "--host",
    "-h",
    default=HELVAR_HOST,
    help="router host/ip address",
    envvar="HELVAR_HOST",
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    default=HELVAR_PORT,
    type=int,
    help="router port for helvarnet (default: 50000 TCP or 50001 UDP)",
    envvar="HELVAR_PORT",
    show_default=True,
)
def cli(host, port):
    """MCP server to control your Helvar DALI system."""
    mcp.run()

if __name__ == "__main__":
    cli()
