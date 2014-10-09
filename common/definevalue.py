#!/usr/bin/env python3

CONTAINER_NAMES = ["env_base", "env_zabbix_server22", "env_zabbix_server20",
                  "env_zabbix_agent22", "env_zabbix_agent20",
                  "env_nagios_server3", "env_nagios_server4",
                  "env_nagios_nrpe", "env_hatohol_build", "env_hatohol_rpm",
                  "env_fluentd", "env_redmine"]

SETUP_FUNCTIONS = {"zabbix-server": run_setup_zabbix_server,
                   "zabbix-agent": run_setup_zabbix_agent,
                   "nagios3": run_setup_nagios_server3,
                   "nagios4": run_setup_nagios_server4,
                   "nrpe": run_setup_nagios_nrpe,
                   "redmine": run_setup_redmine,
                   "fluentd": run_setup_fluentd}

KEY_OF_BASE_CONTAINER = "base_container"
TIMEOUT_VALUE = 30
