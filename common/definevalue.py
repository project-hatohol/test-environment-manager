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

ZABBIX_CONF_SERVER_PATH = "/etc/zabbix/zabbix_server.conf"
ZABBIX_CONF_HTTPD_PATH = "/etc/httpd/conf.d/zabbix.conf"
ZABBIX_CONF_PHP_PATH = "/etc/zabbix/web/zabbix.conf.php"

ZABBIX_CONF_FILE_PATH = "/etc/zabbix/zabbix_agentd.conf"

NAGIOS3_LIST_OF_PATH = {"CONFIG": "/etc/nagios/nagios.cfg",
                        "COMMANDS": "/etc/nagios/objects/commands.cfg",
                        "SERVER_DIR": "/etc/nagios/servers/",
                        "PASSWORD": "/etc/nagios/passwd",
                        "CGI": "/etc/nagios/cgi.cfg",
                        "NDO2DB": "/etc/nagios/ndo2db.cfg"}

NAGIOS4_LIST_OF_PATH = {"CONFIG": "/usr/local/nagios/etc/nagios.cfg",
                        "COMMANDS": "/usr/local/nagios/etc/objects/commands.cfg",
                        "SERVER_DIR": "/usr/local/nagios/etc/servers/",
                        "PASSWORD": "/usr/local/nagios/etc/htpasswd.users",
                        "CGI": "/usr/local/nagios/etc/cgi.cfg",
                        "NDO2DB": "/usr/local/nagios/etc/ndo2db.cfg"}

NRPE_FILE_PATH = "/etc/nagios/nrpe.cfg"

REDMINE_LIST_OF_PATH = ["/var/lib/redmine/config/database.yml",
                        "/var/lib/redmine/config/configuration.yml",
                        "/var/lib/redmine/my_setting",
                        "/var/lib/redmine/setting_command.sh"]

TD_AGENT_FILE_PATH = "/etc/td-agent/td-agent.conf"

