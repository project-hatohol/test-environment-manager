#!/usr/bin/env python3
import lxc
import os
import sys

def print_success_message(name):
    print("Create Container: %s" % name)


if not os.geteuid() == 0:
    print("You need root permission to use this script.")
    sys.exit(1)


base_name = "env_base"
base = lxc.Container(base_name)
if not base.defined:
    base.create("centos")
    print_success_message("Create Container: %s" % base_name)

    base.start()
    base.get_ips(timeout=30)
    base.attach_wait(lxc.attach_run_command,
                     ["yum", "upgrade", "-y"])

    if not base.shutdown(30):
        base.stop()
