#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 16:00:58 Saturday

@author: Nikhil Kapila
"""

def get_router_overview(router)->dict:
    router_devices = {} # device address
    router_groups = {} # group address
    # TODO: scene blocks can be HUGE! check later for those ones with names and return
    # router_scenes = {} 
    
    # print("Router devices: ")
    for key, value in router.devices.devices.items():
        # key is addr, value is desc
        router_devices[key] = value

    # print("Router groups: ")
    for key, value in router.groups.groups.items():
        # key is group#, value is group#: name
        router_groups[key] = value

    # print("Router scenes: ")
    # for key, value in router.scenes.scenes.items():
    #     print(f"    {value}")

    return {
        "devices_on_system": router_devices,
        "groups_on_devices": router_groups
            }