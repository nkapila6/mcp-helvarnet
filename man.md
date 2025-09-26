# man
A minified man page to understand how the library works and interacts with HelvarNET

# Parsers
- address.py:
  - HelvarAddress represents a Helvar device address
  - SceneAddress represents a Helvar scene address

- command.py:
  - Command issues command to router:
    - CommandType - QUERY_CLUSTERS, DIRECT_LEVEL_DEVICE, etc
    - CommandParameters: G:1, S:3, etc
    - CommandMessageType: command, internal command, err, resp
    - CommandAddr: HelvarAddress -> issue address to this Helvar "device"

- command_parameter.py:
  - CommandParameterType: mapping to TCP IP packet
  - CommandParameter takes CommandParameterType

- command_type.py:
  - CommandType: tuples, mapping of string to enums
      - Queries:
        - QUERY_CLUSTERS = (101, "Query Clusters.")
        - QUERY_GROUP_DESCRIPTION = (105, "Query group description.")
        - QUERY_DEVICE_DESCRIPTION = (106, "Query device description.")
        - QUERY_DEVICE_TYPES_AND_ADDRESSES = (100, "Query Device Types and Addresses")
        - QUERY_DEVICE_STATE = (110, "Query Device State")
        - QUERY_WORKGROUP_NAME = (107, "Query Workgroup Name")
        - QUERY_DEVICE_LOAD_LEVEL = (152, "Query Device Load Level")
        - QUERY_SCENE_INFO = (167, "Query device scene levels.")
        - QUERY_ROUTER_TIME = (185, "Query Router Time")
        - QUERY_LAST_SCENE_IN_GROUP = (109, "Query last scene selected in a group.")
        - QUERY_LAST_SCENE_IN_BLOCK = (103, "Query last scene selected in a group block.")
        - QUERY_GROUP = (164, "Query devices in group.")
        - QUERY_GROUPS = (165, "Query all groups.")
        - QUERY_SCENE_NAMES = (166, "Query all scene names in group.")
        - QUERY_ROUTER_VERSION = (190, "Query the router software version.")
      QUERY_HELVARNET_VERSION = (191, "Query the HelvarNet software version.")

      - Commands:
        - DIRECT_LEVEL_DEVICE = (14, "Direct Level, Device")
        - RECALL_SCENE = (11, "Recall Scene")

- parser.py:
parser.py takes everything above and generates a command. Vice-versa case: takes in response and generates result.

# config.py
Represents a Helvar config

# devices.py
- Device: represents a helvar device: driver, relays, sensors, etc
  - has associated functions to set brightness, check if disabled, missing, is_faulty, is_lamp_failure, is_load, _set_level, set_scene_level, get_level_for_scene

- Devices: takes above Device class

- get_devices(router): fetches device from router and registers it as a `Device`

# exceptions.py
3 error cases: Error (base class): ParserError, UnrecogCommand, CommandRespTimeout

# groups.py
- Group(): base class
- Groups(): group related commands: get_scenes_for_group, set_scene, get_groups, update_group_last_scene

# scenes.py
- Scene(): base class
- Scenes(): similar to above, has methods to get and set scenes.

# router.py
- Router(): controls a helvar router
  - on init, parses host and port
  - registers base classes for groups, devices, scenes

  - connect(): connects to Router and calls internal func _keep_alive_task that keeps the TCP connection alive

  - disconnect(): disconnects

  - internal funcs: has incoming resp parser and outgoing request parser

  - init: performs connect, initialize base classes for groups devices, scenes, etc.

  - send_command(): sends command

# static.py
initiates (#define) different enums/dicts for different types of devices, protocols, etc

# overall DAG
Based on my understanding, overall DAG should be:
1. make Router object
2. call initiates on Router to init everything from Router
3. et voila; do whatever you likey.
  - router.devices: has methods from devices.py
  - router.groups: has methods from groups.py
  - router.scenes: has methods from scenes.py
