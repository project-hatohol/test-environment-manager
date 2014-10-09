#!/usr/bin/env python3
import os
import sys
import yaml
import lxc
sys.path.append("../common")
import definevalue
from utils import *

if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))
