#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 14:56:55 Saturday

@author: Nikhil Kapila
"""

from aiohelvar.router import Router

from aiohelvar.parser.command_type import (
    COMMAND_TYPES_DONT_LISTEN_FOR_RESPONSE,
    CommandType,
    MessageType,
)

from aiohelvar.parser.address import SceneAddress, HelvarAddress
from aiohelvar.parser.command_parameter import CommandParameter, CommandParameterType
from aiohelvar.parser.command import Command

async def fetch_groups(router)->dict:
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


async def switch_on_group(router:Router, group_id:int|str)->str:
    # default ON scene is group.1.1
    await set_group_level_to_pct(router, group_id, 1, 1)
    return "Your lights should be switch ON shortly."

async def set_group_to_75_percent(router:Router, group_id:int|str)->str:
    # default 75% scene is group.1.2
    await set_group_level_to_pct(router, group_id, 1, 2)
    return "Your lights should be switch ON shortly."

async def set_group_to_50_percent(router:Router, group_id:int|str)->str:
    # default 50% scene is group.1.3
    await set_group_level_to_pct(router, group_id, 1, 3)
    return "Your lights should be switch ON shortly."

async def set_group_to_25_percent(router:Router, group_id:int|str)->str:
    # default 25% scene is group.1.4
    await set_group_level_to_pct(router, group_id, 1, 4)
    return "Your lights should be switch ON shortly."

async def set_group_to_10_percent(router:Router, group_id:int|str)->str:
    # default 10% scene is group.1.5
    await set_group_level_to_pct(router, group_id, 1, 5)
    return "Your lights should be switch ON shortly."

async def switch_off_group(router:Router, group_id:int|str)->str:
    # default OF scene is group.1.8
    await set_group_level_to_pct(router, group_id, 1, 8)    
    return "Your lights should switch OFF shortly."

async def set_group_level_to_pct(router:Router, group_id:int|str, block_id:int, scene_id:int)->dict:
    if isinstance(group_id, str):
        gdict = await fetch_groups(router)
        gdict = [k for k,v in gdict.items() if v['name']==group_id]
        if (len(gdict)==0):
            return {"result": "Sorry, not able to find the group by name, please specify group number."}
        group_id = gdict[0] # always assume we get only exact match
        
    scene_address = SceneAddress(group_id, block_id, scene_id)

    # TODO: add fade times later
    await router.send_command(
            Command(
                CommandType.RECALL_SCENE,
                [
                    CommandParameter(CommandParameterType.GROUP, scene_address.group),
                    CommandParameter(CommandParameterType.BLOCK, scene_address.block),
                    CommandParameter(CommandParameterType.SCENE, scene_address.scene),
                    #CommandParameter(CommandParameterType.FADE_TIME, fade_time),
                ],
            )
    )
    
    return {"result": "Your group should be set to the scene shortly."}