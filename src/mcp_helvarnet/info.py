#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 16:00:58 Saturday

@author: Nikhil Kapila
"""

from typing import Dict, Any, Callable

from aiohelvar import Router
from pydantic import Field
from fastmcp import FastMCP

def register_info_tools(mcp:FastMCP, get_router:Callable[[], Router]):
    """Register all router info tools with the MCP server."""

    @mcp.tool()
    def get_router_overview() -> Dict[str, Any]:
        """Get a comprehensive overview of the router's devices and groups.

        Retrieves all devices and groups configured on the Helvar router system.
        This provides a complete inventory of what lighting devices and groups
        are available for control.
        """
        try:
            router = get_router()
            router_devices = {} # device address
            router_groups = {} # group address
            # TODO: scene blocks can be HUGE! check later for those ones with names and return
            # router_scenes = {}

            # router devices
            for key, value in router.devices.devices.items():
                # key is addr, value is desc
                router_devices[str(key)] = str(value)

            # router groups
            for key, value in router.groups.groups.items():
                # key is group#, value is group#: name
                router_groups[str(key)] = str(value)

            # router scenes
            # for key, value in router.scenes.scenes.items():
            #     print(f"    {value}")

            return {
                "devices_on_system": router_devices,
                "groups_on_devices": router_groups
                    }
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_workgroup_name()-> Dict[str, Any]:
        """Get the workgroup name of the Helvar router."""
        try:
            router = get_router()
            return {"workgroup_name": router.workgroup_name}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_cluster_id()-> Dict[str, Any]:
        """Get the cluster ID of the Helvar router."""
        try:
            router = get_router()
            return {"cluster_id": router.cluster_id}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_host_ip() -> Dict[str, str]:
        """Get the host IP address of the Helvar router."""
        try:
            router = get_router()
            return {"host_ip": router.host}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_port() -> Dict[str, Any]:
        """Get the network port of the Helvar router."""
        try:
            router = get_router()
            return {"port": router.port}
        except Exception as e:
            return {"error": str(e)}
