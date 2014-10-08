#!/usr/bin/env python3
import os
import sys
import yaml
import lxc

def get_dictionary_from_yaml_file(file_path):
    yaml_file = open(file_path).read()
    return yaml.load(yaml_file)


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)
