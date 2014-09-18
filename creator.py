#!/usr/bin/env python3
import lxc
import os
import sys

if not os.geteuid() == 0:
    print("You need root permission to use this script.")
    sys.exit(1)
