#!/usr/bin/env python3
import definevalue

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
