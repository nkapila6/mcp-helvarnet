#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-09-27 15:58:44 Saturday

@author: Nikhil Kapila
"""

def get_device_overview(device):
    """
    Get a comprehensive overview of a Helvar device as a dictionary.
    
    Args:
        device: aiohelvar.devices.Device object
        
    Returns:
        dict: Complete device information
    """
    # Parse the state flags
    state_flags = device._get_states()
    
    # Get address components - HelvarAddress uses block, router, subnet, device
    address_str = str(device.address)  # Use the built-in __str__ method
    
    # Build address components dict
    address_components = {
        'block': device.address.block,
        'router': device.address.router,
        'subnet': device.address.subnet,
        'device': device.address.device
    }
    
    # Parse scene levels - find configured scenes
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
    
    # Get last scene info
    last_scene_info = None
    if device.last_scene:
        last_scene_info = {
            'group': device.last_scene.group,
            'block': device.last_scene.block,
            'scene': device.last_scene.scene,
            'address': str(device.last_scene)
        }
    
    # Health status summary
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
    
    # Determine bus type from subnet
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

def get_all_devices_overview(router):
    """
    Get overview of all light devices.
    
    Returns:
        dict: Complete overview with device summaries and statistics
    """
    light_devices = router.devices.get_light_devices()
    
    device_overviews = []
    total_brightness = 0
    health_summary = {'healthy': 0, 'issues': 0}
    protocol_counts = {}
    bus_type_counts = {}
    
    for device in light_devices:
        overview = get_device_overview(device)
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