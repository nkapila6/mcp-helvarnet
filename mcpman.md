## mcp-helvarnet features

### System Information & Discovery
You can get a good overview of the entire lighting system.

- **`get_router_overview()`**: Lists all devices and groups configured on the router.
- **`get_all_groups()`**: Provides a list of all lighting groups with their names and IDs.
- **`get_all_devices_overview()`**: Gives a detailed summary of all light devices, including statistics about health and brightness.
- **`get_workgroup_name()`, `get_cluster_id()`, `get_host_ip()`, `get_port()`**: These tools provide basic information about the router's configuration.

### Group Control
You have several ways to control lighting groups.

- **On/Off Control**: You can use `switch_on_group()` and `switch_off_group()` for basic control.
- **Preset Brightness Levels**: Functions like `set_group_to_x_percent()`, (x=25, 50, 75, 100) allow you to set predefined brightness levels.
- **Custom Scene Recall**: For more specific control, `set_group_level_to_scene()` lets you recall a particular scene for any group.

### Device Information & Filtering
You can query and filter individual devices based on different criteria.

- **`get_device_overview()`**: Gets a comprehensive report about a single device, including its brightness, health, and scene configuration.
- **`get_devices_by_health_status()`**: Helps you find devices that are working correctly or ones that have issues.
- **`get_devices_by_brightness_range()`**: Lets you find devices that are within a specific brightness range (e.g., to see which lights are on).
- **`get_devices_by_protocol()`**: You can list devices that use a specific protocol, such as DALI.

## Coming soon

- **Real-time Subscriptions**: The underlying `aiohelvar` library supports real-time updates for device and group states, but this has not been integrated into the MCP server yet.
- **Individual Device Control**: There are no tools to directly set the brightness of an individual light. You can only control lights as part of a group.
- **Scene Management**: `scenes.py` thinking of what to add yet.
- **Clusters and Sensors**: There is no implementation for controlling or getting information from clusters or sensors.

## What else?
You suggest.