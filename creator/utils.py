#!/usr/bin/env python3

def print_success_message(name):
    print("Create Container: %s" % name)


def print_exists_message(name):
    print("Container already exists: %s" % name)


def print_container_exist_message(name):
    print("Container \"%s\": True" % name)


def print_container_non_exist_message(name):
    print("Container \"%s\": false" % name)


def print_container_name(name):
    print("Container name: %s" % name)


def print_new_line():
    print("")


def shutdown_container(container):
    if not container.shutdown(30):
        container.stop()
