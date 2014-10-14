#!/usr/bin/env python3

CONTAINER_NAMES = ["env_base", "env_zabbix_server22", "env_zabbix_server20",
                  "env_zabbix_agent22", "env_zabbix_agent20",
                  "env_nagios_server3", "env_nagios_server4",
                  "env_nagios_nrpe", "env_hatohol_build", "env_hatohol_rpm",
                  "env_fluentd", "env_redmine"]

KEY_OF_BASE_CONTAINER = "base_container"
TIMEOUT_VALUE = 30

ZABBIX_SERVER_ADDRESS = "http://127.0.0.1/zabbix/api_jsonrpc.php"
ZABBIX_API_HEADER = {"content-type": "application/json"}
