#!/usr/bin/env python
#! coding: utf-8

import argparse
import yaml
import os
from pprint import pprint

def convert_1_to_2(config):
    for panel in config['Panels'][:]:
        if panel['Class'] == 'rviz/Time':
            config['Panels'].remove(panel)
        else:
            panel['Class'] = panel['Class'].replace('rviz', 'rviz_common')

    for tool in config['Visualization Manager']['Tools'][:]:
        if tool['Class'] == 'rviz/Interact':
            config['Visualization Manager']['Tools'].remove(tool)
        else:
            tool['Class'] = tool['Class'].replace('rviz', 'rviz_default_plugins')
    for display in config['Visualization Manager']['Displays'][:]:
        display['Class'] = display['Class'].replace('rviz', 'rviz_default_plugins')

    config['Visualization Manager']['Views']['Current']['Class'] = config['Visualization Manager']['Views']['Current']['Class'].replace('rviz', 'rviz_default_plugins')

    return config

def convert_2_to_1(config):
    for panel in config['Panels'][:]:
        panel['Class'] = panel['Class'].replace('rviz_common', 'rviz')
    panel = {'Class': 'rviz/Time',
             'Experimental': 'false',
             'Name': 'Grid',
             'SyncMode': '0',
             'SyncSource': "",
            }
    config['Panels'].append(panel)
    for tool in config['Visualization Manager']['Tools'][:]:
        tool['Class'] = tool['Class'].replace('rviz_default_plugins', 'rviz')

    tool = {'Class': 'rviz/Interact',
            'Hide Inactive Objects': 'true',
           }

    config['Visualization Manager']['Tools'].append(tool)

    for display in config['Visualization Manager']['Displays'][:]:
        display['Class'] = display['Class'].replace('rviz_default_plugins', 'rviz')

    config['Visualization Manager']['Views']['Current']['Class'] = config['Visualization Manager']['Views']['Current']['Class'].replace('rviz_default_plugins', 'rviz')
    return config

def output(config, path, overwrite_flag):
    name = None
    if overwrite_flag:
        name = path
    else:
        name = os.path.dirname(path) + '/converted_' + os.path.basename(path)

    with open(name, 'w') as f:
        f.write(yaml.dump(config, default_flow_style=False))
    print('successfully saved:', name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a rviz config to another rviz version')
    parser.add_argument('path', type=str,
                        help='path rviz config file. your/rviz/config/path/config.rviz')
    parser.add_argument('--version', default='1to2', type=str,
                        help='rviz version. 1to2 or 2to1 (default: 1to2)')
    parser.add_argument('--overwrite', action='store_true',
                        help='if false, add prefix "converted_" to output file name')

    args = parser.parse_args()

    root, ext = os.path.splitext(args.path)
    if ext != '.rviz':
        print("\33[31mthe extension of config file must be '.rviz'\33[0m")
        exit(-1)

    config = dict()
    with open(args.path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    print('version: ', args.version)

    if args.version == '1to2':
        print('convert rviz1 config to rviz2')
        config = convert_1_to_2(config)
        output(config, args.path, args.overwrite)
    elif args.version == '2to1':
        print('convert rviz2 config to rviz1')
        config = convert_2_to_1(config)
        output(config, args.path, args.overwrite)
    else:
        print('\33[31minvalid version\33[0m')
