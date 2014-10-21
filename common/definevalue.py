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

ZBX_SRV_PATH = {"CONFIG": "/etc/zabbix/zabbix_server.conf",
                "DAEMON": "/etc/httpd/conf.d/zabbix.conf",
                "PHP": "/etc/zabbix/web/zabbix.conf.php"}

ZBX_AGT_PATH = {"CONFIG":"/etc/zabbix/zabbix_agentd.conf"}

NAGIOS3_PATH = {"CONFIG": "/etc/nagios/nagios.cfg",
                "COMMANDS": "/etc/nagios/objects/commands.cfg",
                "SERVER_DIR": "/etc/nagios/servers/",
                "PASSWORD": "/etc/nagios/passwd",
                "CGI": "/etc/nagios/cgi.cfg",
                "NDO2DB": "/etc/nagios/ndo2db.cfg"}

NAGIOS4_PATH = {"CONFIG": "/usr/local/nagios/etc/nagios.cfg",
                "COMMANDS": "/usr/local/nagios/etc/objects/commands.cfg",
                "SERVER_DIR": "/usr/local/nagios/etc/servers/",
                "PASSWORD": "/usr/local/nagios/etc/htpasswd.users",
                "CGI": "/usr/local/nagios/etc/cgi.cfg",
                "NDO2DB": "/usr/local/nagios/etc/ndo2db.cfg"}

NRPE_PATH = {"CONFIG": "/etc/nagios/nrpe.cfg"}

REDMINE_PATH = {"DATABASE": "/var/lib/redmine/config/database.yml",
                "CONFIG": "/var/lib/redmine/config/configuration.yml",
                "MYSQL": "/var/lib/redmine/my_setting",
                "SHELL": "/var/lib/redmine/setting_command.sh"}

TD_AGENT_PATH = {"CONFIG": "/etc/td-agent/td-agent.conf"}

