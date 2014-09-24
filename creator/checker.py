#!/usr/bin/env python3
import lxc
import os
import sys


base_name = "env_base"
zabbix_server22_name = "env_zabbix_server22"
zabbix_server20_name = "env_zabbix_server20"
zabbix_agent22_name = "env_zabbix_agent22"
zabbix_agent20_name = "env_zabbix_agent20"
nagios_server3_name = "env_nagios_server3"
nagios_server4_name = "env_nagios_server4"
nagios_nrpe_name = "env_nagios_nrpe"
hatohol_build_name = "env_hatohol_build"
hatohol_rpm_name = "env_hatohol_rpm"
fluentd_name = "env_fluentd"
redmine_name = "env_redmine"
base = lxc.Container(base_name)
zabbix_server22 = lxc.Container(zabbix_server22_name)
zabbix_server20 = lxc.Container(zabbix_server20_name)
zabbix_agent22 = lxc.Container(zabbix_agent22_name)
zabbix_agent20 = lxc.Container(zabbix_agent20_name)
nagios_server3 = lxc.Container(nagios_server3_name)
nagios_server4 = lxc.Container(nagios_server4_name)
nagios_nrpe = lxc.Container(nagios_nrpe_name)
hatohol_build = lxc.Container(hatohol_build_name)
hatohol_rpm = lxc.Container(hatohol_rpm_name)
fluentd = lxc.Container(fluentd_name)
redmine = lxc.Container(container_name)


if __name__ == '__main__':
    if not os.geteuid() == 0:
        print("You need root permission to use this script.")
        sys.exit(1)
