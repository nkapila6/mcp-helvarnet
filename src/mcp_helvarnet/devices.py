#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 15:58:44 Saturday

@author: Nikhil Kapila
"""

from typing import Annotated, Dict, Any, List, Callable
from pydantic import Field
from fastmcp import FastMCP
from aiohelvar import Router


def register_device_tools(mcp: FastMCP, get_router: Callable[[], Router]):
    """Register all device control and info tools with the MCP server."""
    
    @mcp.tool()
    def get_device_overview(
        device_address: Annotated[str, Field(description="Device address in format like '1.1.2.3' (block.router.subnet.device)")]
    ) -> Dict[str, Any]:
        """Get a comprehensive overview of a specific Helvar device.
        
        Provides detailed information about a single device including brightness,
        health status, scene configuration, and technical details.
        """
        try:
            router = get_router()
            
            # find the device by address
            device = None
            for dev in router.devices.devices.values():
                if str(dev.address) == device_address:
                    device = dev
                    break
            
            if not device:
                return {"error": f"Device with address {device_address} not found"}
            
            return _get_device_overview_internal(device)
            
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_all_devices_overview() -> Dict[str, Any]:
        """Get overview of all light devices in the system.
        
        Provides a comprehensive summary of all lighting devices including
        statistics, health status, and individual device information.
        """
        try:
            router = get_router()
            return _get_all_devices_overview_internal(router)
            
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_devices_by_health_status(
        status: Annotated[str, Field(description="Health status to filter by: 'healthy' or 'issues'")] = "issues"
    ) -> Dict[str, Any]:
        """Get devices filtered by their health status.
        
        Useful for finding problematic devices or checking which devices are working properly.
        """
        try:
            router = get_router()
            light_devices = router.devices.get_light_devices()
            
            filtered_devices = []
            for device in light_devices:
                overview = _get_device_overview_internal(device)
                if overview['health']['status'] == status:
                    filtered_devices.append(overview)
            
            return {
                'devices': filtered_devices,
                'count': len(filtered_devices),
                'filter': status,
                'summary': f"Found {len(filtered_devices)} devices with status '{status}'"
            }
            
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_devices_by_brightness_range(
        min_brightness: Annotated[int, Field(description="Minimum brightness percentage", ge=0, le=100)] = 0,
        max_brightness: Annotated[int, Field(description="Maximum brightness percentage", ge=0, le=100)] = 100
    ) -> Dict[str, Any]:
        """Get devices within a specific brightness range.
        
        Useful for finding devices that are on, off, or at specific brightness levels.
        """
        try:
            router = get_router()
            light_devices = router.devices.get_light_devices()
            
            filtered_devices = []
            for device in light_devices:
                if min_brightness <= device.load_level <= max_brightness:
                    overview = _get_device_overview_internal(device)
                    filtered_devices.append(overview)
            
            return {
                'devices': filtered_devices,
                'count': len(filtered_devices),
                'brightness_range': f"{min_brightness}%-{max_brightness}%",
                'summary': f"Found {len(filtered_devices)} devices with brightness between {min_brightness}% and {max_brightness}%"
            }
            
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    def get_devices_by_protocol(
        protocol: Annotated[str, Field(description="Protocol to filter by (e.g., 'DALI', 'DIM', etc.)")]
    ) -> Dict[str, Any]:
        """Get devices that use a specific protocol.
        
        Useful for understanding the mix of device types and protocols in the system.
        """
        try:
            router = get_router()
            light_devices = router.devices.get_light_devices()
            
            filtered_devices = []
            for device in light_devices:
                if device.protocol == protocol:
                    overview = _get_device_overview_internal(device)
                    filtered_devices.append(overview)
            
            return {
                'devices': filtered_devices,
                'count': len(filtered_devices),
                'protocol': protocol,
                'summary': f"Found {len(filtered_devices)} devices using {protocol} protocol"
            }
            
        except Exception as e:
            return {"error": str(e)}

def _get_device_overview_internal(device):
    """
    Internal function to get device overview (your original function logic).
    """
    # parse the state flags
    state_flags = device._get_states()
    
    # get address components - HelvarAddress uses block, router, subnet, device
    address_str = str(device.address)  # Use the built-in __str__ method
    
    # build address components dict
    address_components = {
        'block': device.address.block,
        'router': device.address.router,
        'subnet': device.address.subnet,
        'device': device.address.device
    }
    
    # parse scene levels - find configured scenes
    configured_scenes = []
    for i, level in enumerate(device.levels):
        if level != '*' and level != '0':
            # Convert index back to scene address
            block = (i // 16) + 1
            scene = (i % 16) + 1
            configured_scenes.append({
                'block': block,
                'scene': scene,
                'level': level,
                'index': i
            })
    
    # get last scene info
    last_scene_info = None
    if device.last_scene:
        last_scene_info = {
            'group': device.last_scene.group,
            'block': device.last_scene.block,
            'scene': device.last_scene.scene,
            'address': str(device.last_scene)
        }
    
    # health status summary
    health_issues = []
    if device.is_disabled:
        health_issues.append("disabled")
    if device.is_missing:
        health_issues.append("missing")
    if device.is_faulty:
        health_issues.append("faulty")
    if device.is_lamp_failure:
        health_issues.append("lamp_failure")
    
    health_status = "healthy" if not health_issues else "issues"
    
    # determine bus type from subnet
    bus_type = device.address.bus_type()
    
    return {
        # basic id stuff
        'name': device.name,
        'address': address_str,
        'address_components': address_components,
        
        # device type n protocols
        'protocol': device.protocol,
        'type': device.type,
        'bus_type': bus_type,
        'is_controllable': device.is_light,
        
        # state right now
        'brightness': {
            'percentage': device.load_level,
            'value_255': device.brightness,
            'last_level': device.last_load_level
        },
        
        # health! ~ healthy missing
        'health': {
            'status': health_status,
            'issues': health_issues,
            # 'raw_state': device.state,
            # 'state_flags': state_flags
        },
        
        # scene info
        'scenes': {
            'last_scene': last_scene_info,
            'configured_scenes': configured_scenes,
            'total_configured': len(configured_scenes)
        },
        
        # TODO: subscription info, this isn't added yet even tho the lib seems to support it (needs testing)
        # 'subscriptions': {
        #     'count': len(device.subscriptions),
        #     'has_subscribers': len(device.subscriptions) > 0
        # },
        
        # overall summary
        'summary': f"{device.name} ({device.type}) at {device.load_level}% brightness"
    }

def _get_all_devices_overview_internal(router):
    """
    Internal function to get all devices overview (your original function logic).
    """
    light_devices = router.devices.get_light_devices()
    
    device_overviews = []
    total_brightness = 0
    health_summary = {'healthy': 0, 'issues': 0}
    protocol_counts = {}
    bus_type_counts = {}
    
    for device in light_devices:
        overview = _get_device_overview_internal(device)
        device_overviews.append(overview)
        
        total_brightness += device.load_level
        health_summary[overview['health']['status']] += 1
        
        protocol = overview['protocol']
        protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
        
        bus_type = overview['bus_type']
        if bus_type:
            bus_type_counts[bus_type] = bus_type_counts.get(bus_type, 0) + 1
    
    avg_brightness = total_brightness / len(light_devices) if light_devices else 0
    
    return {
        'devices': device_overviews,
        'statistics': {
            'total_devices': len(light_devices),
            'average_brightness': round(avg_brightness, 1),
            'health_summary': health_summary,
            'protocols': protocol_counts,
            'bus_types': bus_type_counts,
            'devices_on': len([d for d in device_overviews if d['brightness']['percentage'] > 0]),
            'devices_off': len([d for d in device_overviews if d['brightness']['percentage'] == 0])
        },
        'quick_summary': f"{len(light_devices)} devices, {health_summary['healthy']} healthy, avg {avg_brightness:.1f}% brightness"
    }