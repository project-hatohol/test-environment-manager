#!/usr/bin/env python3
import sys
import os

def finish_if_argument_is_not_given(number_of_argument):
    if (number_of_argument == 1):
        print("Error: argument is not given")
        sys.exit(1)


def finish_if_user_run_as_general_user():
    if not os.geteuid() == 0:
        print("Error: You need root permission to use this script.")
        sys.exit(1)
