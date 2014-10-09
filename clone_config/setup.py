#!/usr/bin/env python3
import os
import sys
import yaml
import lxc
sys.path.append("../common")
import definevalue
from utils import *

def run_setup_zabbix_server():
    print("Not implemented yet: run_setup_zabbix_server")


def run_setup_zabbix_agent():
    print("Not implemented yet: run_setup_zabbix_agent")


def run_setup_nagios_server3():
    print("Not implemented yet: run_setup_nagios_server3")


def run_setup_nagios_server4():
    print("Not implemented yet: run_setup_nagios_server4")


def run_setup_nagios_nrpe():
    print("Not implemented yet: run_setup_nagios_nrpe")


def run_setup_redmine():
    print("Not implemented yet: run_setup_redmine")


def run_setup_fluentd():
    print("Not implemented yet: run_setup_fluentd")


SETUP_FUNCTIONS = {"zabbix-server": run_setup_zabbix_server,
                   "zabbix-agent": run_setup_zabbix_agent,
                   "nagios3": run_setup_nagios_server3,
                   "nagios4": run_setup_nagios_server4,
                   "nrpe": run_setup_nagios_nrpe,
                   "redmine": run_setup_redmine,
                   "fluentd": run_setup_fluentd}

if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))
