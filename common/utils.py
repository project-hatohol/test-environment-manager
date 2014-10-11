#!/usr/bin/env python3
import sys
import os
import definevalue

def exit_if_argument_is_not_given(number_of_argument):
    if (number_of_argument == 1):
        print("Error: argument is not given")
        sys.exit(os.EX_USAGE)


def exit_if_user_run_this_as_general_user():
    if not os.geteuid() == 0:
        print("Error: You need root permission to use this script.")
        sys.exit(os.EX_NOPERM)


def print_success_message(name):
    print("Create Container: %s" % name)


def print_exists_message(name):
    print("Container already exists: %s" % name)


def print_new_line():
    print("")


def is_container_name_defined(container_name):
    if container_name in definevalue.CONTAINER_NAMES:
        return True
    else:
        print ("Provided name is wrong: %s" % container_name)
        return False


def shutdown_container(container):
    print_new_line()
    if not container.shutdown(definevalue.TIMEOUT_VALUE):
        container.stop()


def get_config_info(yaml_file_path):
    yaml_data = open(yaml_file_path).read()
    return yaml.load(yaml_data)
