#!/usr/bin/env python3
import sys
sys.path.append("../common")
import clone
import setup
from utils import *

if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    clone.start_clone_containers(argvs[1])
    setup.start_setup(argvs[1])
