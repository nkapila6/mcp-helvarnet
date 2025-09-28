#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 14:56:55 Saturday

@author: Nikhil Kapila
"""

from typing import Annotated, Dict, Any, Callable, Union

from pydantic import Field
from fastmcp import FastMCP
from aiohelvar import Router

from aiohelvar.parser.command_type import (
    COMMAND_TYPES_DONT_LISTEN_FOR_RESPONSE,
    CommandType,
    MessageType,
)

from aiohelvar.parser.address import SceneAddress, HelvarAddress
from aiohelvar.parser.command_parameter import CommandParameter, CommandParameterType
from aiohelvar.parser.command import Command


def register_group_tools(mcp: FastMCP, get_router: Callable[[], Router]):
    """Register all group control and info tools with the MCP server."""

    async def _fetch_groups(router)->Dict[str, Dict[str,str]]:
        """Fetch all available lighting groups and their descriptions."""
        
        response = await router._send_command_task(Command(CommandType.QUERY_GROUPS))
        group_ids = response.result.split(",")
        groups={}
        
        for group_id in group_ids:
            group_id = group_id.strip()
            if group_id: 
                int(group_id)

                group_name = await router._send_command_task(
                    Command(
                        CommandType.QUERY_GROUP_DESCRIPTION,
                        [CommandParameter(CommandParameterType.GROUP, group_id)],
                        )
                    )

                groups[group_id] = {
                    "group_number": group_id,
                    "name": group_name.result
                    }

        return groups

    async def _set_group_level_to_pct(
        router: Router, 
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to control. Can be numeric like '5' or descriptive like 'Living Room'")],
        block_id: Annotated[int, Field(description="Block ID for the scene (usually 1)", ge=1)] = 1,
        scene_id: Annotated[int, Field(description="Scene ID within the block. Different scenes represent different brightness levels (1=ON, 2=75%, 3=50%, 4=25%, 5=10%, 8=OFF)", ge=1)] = 1
    ) -> dict:
        if isinstance(group_id, str):
            gdict = await _fetch_groups(router)
            gdict = [k for k,v in gdict.items() if v['name']==group_id]
            if (len(gdict)==0):
                return {"result": "Sorry, not able to find the group by name, please specify group number."}
            group_id = gdict[0] # always assume we get only exact match
            
        scene_address = SceneAddress(int(group_id), block_id, scene_id)

        # TODO: add fade times later
        await router.send_command(
                Command(
                    CommandType.RECALL_SCENE,
                    [
                        CommandParameter(CommandParameterType.GROUP, str(scene_address.group)),
                        CommandParameter(CommandParameterType.BLOCK, str(scene_address.block)),
                        CommandParameter(CommandParameterType.SCENE, str(scene_address.scene)),
                        #CommandParameter(CommandParameterType.FADE_TIME, fade_time),
                    ],
                )
        )
        
        return {"result": "Your group should be set to the scene shortly."}


    @mcp.tool()
    async def get_all_groups() -> Dict[str, Any]:
        """Fetch all available lighting groups and their descriptions.
        
        Retrieves a complete list of all lighting groups configured in the system,
        including their group numbers and human-readable names/descriptions.
        """
        try:
            router = get_router()
            return await _fetch_groups(router)
        except Exception as e:
            return {"error": str(e)}


    @mcp.tool()
    async def switch_on_group(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to turn on. Can be either a numeric ID like '5' or a descriptive name like 'Living Room'")]
    ) -> str:
        """Turn on a lighting group to full brightness.
        
        Activates the default ON scene for the specified lighting group,
        setting all lights in the group to maximum brightness.
        """
        try:
            router = get_router()
            # default ON scene is group.1.1
            await _set_group_level_to_pct(router, group_id, 1, 1)
            return "Your lights should be switch ON shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def set_group_to_75_percent(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to set to 75% brightness. Examples: '3', 'Kitchen', 'Bedroom Lights'")]
    ) -> str:
        """Set a lighting group to 75% brightness.
        
        Perfect for normal room lighting when you want bright but not maximum illumination.
        """
        try:
            router = get_router()
            # default 75% scene is group.1.2
            await _set_group_level_to_pct(router, group_id, 1, 2)
            return "Your lights should be switch ON shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def set_group_to_50_percent(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to set to 50% brightness. Examples: '3', 'Kitchen', 'Bedroom Lights'")]
    ) -> str:
        """Set a lighting group to 50% brightness.
        
        Ideal for comfortable ambient lighting or when you want moderate illumination.
        """
        try:
            router = get_router()
            # default 50% scene is group.1.3
            await _set_group_level_to_pct(router, group_id, 1, 3)
            return "Your lights should be switch ON shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def set_group_to_25_percent(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to set to 25% brightness. Examples: '3', 'Kitchen', 'Bedroom Lights'")]
    ) -> str:
        """Set a lighting group to 25% brightness.
        
        Great for evening lighting, watching TV, or creating a cozy atmosphere.
        """
        try:
            router = get_router()
            await _set_group_level_to_pct(router, group_id, 1, 4)
            return "Your lights should be switch ON shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def set_group_to_10_percent(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to set to 10% brightness for very dim ambient lighting. Examples: '3', 'Kitchen', 'Bedroom Lights'")]
    ) -> str:
        """Set a lighting group to 10% brightness (very dim lighting).
        
        Perfect for nighttime navigation, sleeping with minimal light, or creating a very subtle ambient glow.
        """
        try:
            router = get_router()
            # default 10% scene is group.1.5
            await _set_group_level_to_pct(router, group_id, 1, 5)
            return "Your lights should be switch ON shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def switch_off_group(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to turn off completely. Examples: '3', 'Kitchen', 'Bedroom Lights'")]
    ) -> str:
        """Turn off a lighting group completely.
        
        Turns off all lights in the group to save energy.
        """
        try:
            router = get_router()
            # default OF scene is group.1.8
            await _set_group_level_to_pct(router, group_id, 1, 8)    
            return "Your lights should switch OFF shortly."
        except Exception as e:
            return str(e)

    @mcp.tool()
    async def set_group_level_to_scene(
        group_id: Annotated[Union[int, str], Field(description="Group ID number or group name to control. Can be numeric like '5' or descriptive like 'Living Room'")],
        block_id: Annotated[int, Field(description="Block ID for the scene (usually 1)", ge=1)] = 1,
        scene_id: Annotated[int, Field(description="Scene ID within the block. Different scenes represent different brightness levels (1=ON, 2=75%, 3=50%, 4=25%, 5=10%, 8=OFF)", ge=1)] = 1
    ) -> dict:
        """Recall a scene for a group by providing group, block and scene ids."""
        try:
            router = get_router()
            return await _set_group_level_to_pct(router, group_id, block_id, scene_id)
        except Exception as e:
            return {"error": str(e)}