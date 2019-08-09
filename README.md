# rviz_config_converter
Convert rviz configuration file format bidirectionally

## Requirement
- Python3

## Environment
- ROS kineitc or melodic <=> ROS2 dashing conversion is confirmed

## How to use
```
git clone https://github.com/taka-kazu/rviz_config_converter.git
cd rviz_config_converter
python3 rviz_config_converter.py your/rviz/config/path/ros1_config.rviz --version 1to2
```
in this case, your/rviz/config/path/converted_ros1_config.rviz is generated
