#!/usr/bin/env python3
import sys

def finish_if_argument_is_not_given(number_of_argument):
    if (number_of_argument == 1):
        print("Error: argument is not given")
        sys.exit(1)
