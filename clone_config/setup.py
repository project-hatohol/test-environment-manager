#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import yaml
import lxc
import requests
import json
import apport
import encodings.idna
sys.path.append("../common")
import definevalue
from utils import *
import clone
import zabbix

def prepare_setup_zabbix_server(argument):
    FILES = ["assets/zabbix_server.conf", "assets/zabbix.conf",
             "assets/zabbix.conf.php"]
    argument = load_asset_files(argument, FILES)
    return argument


def install_config_files_of_zabbix(zabbix_conf_server,
                                   zabbix_conf_httpd,
                                   zabbix_conf_php):
    ZABBIX_CONF_SERVER_PATH = "/etc/zabbix/zabbix_server.conf"
    ZABBIX_CONF_HTTPD_PATH = "/etc/httpd/conf.d/zabbix.conf"
    ZABBIX_CONF_PHP_PATH = "/etc/zabbix/web/zabbix.conf.php"
    INSTALL_FILES = [[ZABBIX_CONF_SERVER_PATH, zabbix_conf_server],
                     [ZABBIX_CONF_HTTPD_PATH, zabbix_conf_httpd],
                     [ZABBIX_CONF_PHP_PATH, zabbix_conf_php]]
    for (path, content) in INSTALL_FILES:
        if os.path.exists(path):
            os.remove(path)

        install_file = open(path, "w")
        install_file.write(content)
        install_file.close()

    CMDS = [["service", "httpd", "restart"],
            ["service", "zabbix-server", "restart"]]
    for run_command in CMDS:
        subprocess.call(run_command)


def start_zabbix_api_functions(list_of_monitored_host):
    auth_token = zabbix.get_authtoken_of_zabbix_server()

    zabbix_server_id = zabbix.get_zabbix_server_id(auth_token)
    zabbix.enable_zabbix_server(zabbix_server_id, auth_token)

    group_id = zabbix.get_linux_servers_group_id(auth_token)
    template_id = zabbix.get_template_os_linux_id(auth_token)
    zabbix.add_monitored_hosts(list_of_monitored_host,
                               group_id, template_id, auth_token)


def run_setup_zabbix_server(argument):
    list_of_monitored_host = argument[0]["target"]
    zabbix_conf_server = argument[1]
    zabbix_conf_httpd = argument[2]
    zabbix_conf_php = argument[3]
    install_config_files_of_zabbix(zabbix_conf_server,
                                   zabbix_conf_httpd,
                                   zabbix_conf_php)
    start_zabbix_api_functions(list_of_monitored_host)


def prepare_setup_zabbix_agent(argument):
    FILES = ["assets/zabbix_agentd.conf"]
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_zabbix_agent(argument):
    CONF_FILE_PATH = "/etc/zabbix/zabbix_agentd.conf"
    os.remove(CONF_FILE_PATH)

    server_ip_and_host_name = argument[0]
    output_data = argument[1]

    zabbix_agentd_conf = open(CONF_FILE_PATH, "w")
    SERVER_OLD = "Server=127.0.0.1"
    SERVER_NEW = "Server=" + server_ip_and_host_name["server_ipaddress"]
    SERVER_ACTIVE_OLD = "ServerActive=127.0.0.1"
    SERVER_ACTIVE_NEW = "Server=" + server_ip_and_host_name["server_ipaddress"]
    HOST_NAME_OLD = "Hostname=Zabbix server"
    HOST_NAME_NEW = "Hostname=" + server_ip_and_host_name["host_name"]
    replace_sequence = [[SERVER_OLD, SERVER_NEW],
                        [SERVER_ACTIVE_OLD, SERVER_ACTIVE_NEW],
                        [HOST_NAME_OLD, HOST_NAME_NEW]]
    for (old, new) in replace_sequence:
        output_data = output_data.replace(old, new)
    zabbix_agentd_conf.write(output_data)


def install_config_file_for_nagios(config_data, commands_data, ndo2db_data,
                                   config_path, commands_path, ndo2db_path,
                                   server_dir_path):
    PATH = [[config_data, config_path], [commands_data, commands_path],
            [ndo2db_data, ndo2db_path]]
    for (data, path) in PATH:
        if os.path.exists(path):
            os.remove(path)
        install_file = open(path, "w")
        install_file.write(data)
        install_file.close()

    if os.path.exists(server_dir_path):
        shutil.rmtree(server_dir_path)

    os.makedirs(server_dir_path)


def add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     server_path):
    EXTENSION = ".cfg"
    HOST_NAME_DEFAULT_HOST = "        host_name               host_name"
    HOST_NAME_PREFIX_HOST = "        host_name               "
    HOST_NAME_DEFAULT_SERVICE = \
        "        host_name                       host_name"
    HOST_NAME_PREFIX_SERVICE = \
        "        host_name                       "
    ALIAS_DEFAULT = "alias                   host_name"
    ALIAS_PREFIX = "alias                   "
    ADDRESS_DEFAULT = "address                 127.0.0.1"
    ADDRESS_PREFIX = "address                 "

    for monitored_info in list_of_monitored_host:
        output_data = host_data
        ip_address = monitored_info["ip"]
        host_name = monitored_info["host"]
        file_name = server_path + host_name + EXTENSION

        replace_points = [[HOST_NAME_DEFAULT_HOST,
                           HOST_NAME_PREFIX_HOST + host_name],
                          [ALIAS_DEFAULT, ALIAS_PREFIX + host_name],
                          [ADDRESS_DEFAULT, ADDRESS_PREFIX + ip_address],
                          [HOST_NAME_DEFAULT_SERVICE,
                           HOST_NAME_PREFIX_SERVICE + host_name]]
        for (old, new) in replace_points:
            output_data = output_data.replace(old, new)

        host_file = open(file_name, "w")
        host_file.write(output_data)
        host_file.close()


def set_username_and_password_for_nagios(username, password,
                                         config_data, config_file_path,
                                         password_file_path):
    FILES = [config_file_path, password_file_path]
    for file_path in FILES:
        if os.path.exists(password_file_path):
            os.remove(password_file_path)

    DEFAULT_USERNAME = "nagiosadmin"
    config_data = config_data.replace(DEFAULT_USERNAME, username)
    config_file = open(config_file_path, "w")
    config_file.write(config_data)

    cmd = ["htpasswd", "-bc", password_file_path, username, password]
    subprocess.call(cmd)


def run_setup_for_nagios_server(argument, list_of_path):
    list_of_monitored_host = argument[0]["target"]
    username = argument[0]["username"]
    password = argument[0]["password"]
    config_data = argument[1]
    host_data = argument[2]
    commands_data = argument[3]
    cgi_data = argument[4]
    ndo2db_data = argument[5]

    install_config_file_for_nagios(config_data, commands_data, ndo2db_data,
                                   list_of_path["CONFIG"],
                                   list_of_path["COMMANDS"],
                                   list_of_path["NDO2DB"],
                                   list_of_path["SERVER_DIR"])
    add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     list_of_path["SERVER_DIR"])
    set_username_and_password_for_nagios(username, password, cgi_data,
                                         list_of_path["CGI"],
                                         list_of_path["PASSWORD"])


def prepare_setup_nagios_server3(argument):
    FILES = ["assets/nagios3.cfg", "assets/host_name.cfg",
             "assets/commands3.cfg", "assets/cgi3.cfg",
             "assets/ndo2db3.cfg"]
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_server3(argument):
    LIST_OF_PATH = {"CONFIG": "/etc/nagios/nagios.cfg",
                    "COMMANDS": "/etc/nagios/objects/commands.cfg",
                    "SERVER_DIR": "/etc/nagios/servers/",
                    "PASSWORD": "/etc/nagios/passwd",
                    "CGI": "/etc/nagios/cgi.cfg",
                    "NDO2DB": "/etc/nagios/ndo2db.cfg"}
    run_setup_for_nagios_server(argument, LIST_OF_PATH)


def prepare_setup_nagios_server4(argument):
    FILES = ["assets/nagios4.cfg", "assets/host_name.cfg",
             "assets/commands3.cfg", "assets/cgi4.cfg",
             "assets/ndo2db4.cfg"]
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_server4(argument):
    LIST_OF_PATH = {"CONFIG": "/usr/local/nagios/etc/nagios.cfg",
                    "COMMANDS": "/usr/local/nagios/etc/objects/commands.cfg",
                    "SERVER_DIR": "/usr/local/nagios/etc/servers/",
                    "PASSWORD": "/usr/local/nagios/etc/htpasswd.users",
                    "CGI": "/usr/local/nagios/etc/cgi.cfg",
                    "NDO2DB": "/usr/local/nagios/etc/ndo2db.cfg"}
    run_setup_for_nagios_server(argument, LIST_OF_PATH)


def prepare_setup_nagios_nrpe(argument):
    FILES = ["assets/nrpe.cfg"]
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_nrpe(argument):
    NRPE_FILE_PATH = "/etc/nagios/nrpe.cfg"
    os.remove(NRPE_FILE_PATH)

    nrpe_cfg = open(NRPE_FILE_PATH, "w")
    nrpe_cfg.write(argument[0])
    nrpe_cfg.close()


def prepare_setup_redmine(argument):
    file_list = ["database.yml", "configuration.yml", "my_setting",
                 "setting_command.sh"]

    for file_name in file_list:
        read_file = open("assets/" + file_name)
        lines = read_file.readlines()
        read_file.close()

        argument.append(lines)

    return argument


def create_setup_file(file_path, argument):
    file = open(file_path, "w")
    file.writelines(argument)
    file.close()


def print_request_responce(request_result):
    if request_result.status_code == 201:
        print("Successed to create a new project")

    else:
        print("Failed to create a new project.")
        print(request_result.text + "\n")


def run_setup_redmine(argument):
    os.chdir("/var/lib/redmine")

    file_paths = ["/var/lib/redmine/config/database.yml",
                  "/var/lib/redmine/config/configuration.yml",
                  "/var/lib/redmine/my_setting",
                  "/var/lib/redmine/setting_command.sh"]

    project_info = argument[0]
    project_data = {"project": {"name": project_info["project_name"],
                      "identifier": project_info["project_id"]}}

    send_data = json.dumps(project_data)

    for each_path_and_argument in range(len(file_paths)):
        create_setup_file(file_paths[each_path_and_argument],
                          argument[each_path_and_argument + 1])

    subprocess.call(["sh","setting_command.sh"])

    request_result = requests.post("http://127.0.0.1/projects.json",
                                   data = send_data,
                                   headers = {"Content-Type": "application/json"},
                                   auth = ("admin", "admin"))
    print_request_responce(request_result)

    subprocess.call(["service", "httpd", "restart"])


def prepare_setup_fluentd(argument):
    FILES = ["assets/td-agent.conf"]
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_fluentd(argument):
    TD_AGENT_FILE_PATH = "/etc/td-agent/td-agent.conf"
    os.remove(TD_AGENT_FILE_PATH)

    td_agent_conf = open(TD_AGENT_FILE_PATH, "w")
    td_agent_conf.write(argument[0])
    td_agent_conf.close()


SETUP_FUNCTIONS = {"zabbix-server": run_setup_zabbix_server,
                   "zabbix-agent": run_setup_zabbix_agent,
                   "nagios3": run_setup_nagios_server3,
                   "nagios4": run_setup_nagios_server4,
                   "nrpe": run_setup_nagios_nrpe,
                   "redmine": run_setup_redmine,
                   "fluentd": run_setup_fluentd}

PREPARE_FUNCTIONS = {run_setup_zabbix_server: prepare_setup_zabbix_server,
                     run_setup_zabbix_agent: prepare_setup_zabbix_agent,
                     run_setup_nagios_server3: prepare_setup_nagios_server3,
                     run_setup_nagios_server4: prepare_setup_nagios_server4,
                     run_setup_nagios_nrpe: prepare_setup_nagios_nrpe,
                     run_setup_redmine: prepare_setup_redmine,
                     run_setup_fluentd: prepare_setup_fluentd}


def get_function_and_arguments(info_of_container_name, list_of_key_in_info):
    list_of_setup_function = SETUP_FUNCTIONS.keys()
    return_list = []
    for key_in_info in list_of_key_in_info:
        if not key_in_info in list_of_setup_function:
            continue
        else:
            info_of_function = info_of_container_name[key_in_info]
            function_argument = []
            if info_of_function is not None:
                function_argument.append(info_of_function)
            return_list.append([SETUP_FUNCTIONS[key_in_info], function_argument])

    return return_list


def get_container_info(info_of_container, list_of_key_in_info):
    list_of_setup_function = SETUP_FUNCTIONS.keys()
    return_info = {}
    for key_in_info in list_of_key_in_info:
        if (not key_in_info in list_of_setup_function and
                not key_in_info in "base_container"):
            return_info[key_in_info] = info_of_container[key_in_info]

    return return_info


def get_container_name_and_info(config_info, get_function_name):
    list_of_container_name = config_info.keys()
    return_list = []
    for container_name in list_of_container_name:
        info_of_container_name = config_info[container_name]
        list_of_key_in_info = info_of_container_name.keys()
        append_content = get_function_name(info_of_container_name,
                                           list_of_key_in_info)
        return_list.append([container_name, append_content])

    return return_list


def setup_container(container_name, run_function_names):
    print("Start setup process: %s" % container_name)
    container = lxc.Container(container_name)
    container.start()
    container.get_ips(timeout=definevalue.TIMEOUT_VALUE)

    for (run_function_name, argument) in run_function_names:
        run_argument = PREPARE_FUNCTIONS[run_function_name](argument)
        container.attach_wait(run_function_name, run_argument)

    shutdown_container(container)


def setup_containers(list_of_setup_containers):
    for (container_name, setup_function) in list_of_setup_containers:
        setup_container(container_name, setup_function)


def install_monitor_group_file(container_info):
    group_file_path = container_info["container_path"] + "/group"
    group_file = open(group_file_path, "w")
    group_file.write(str(container_info["monitor_group"]))
    group_file.close()


def install_container_config_file(container_info):
    config_file_path = container_info["container_path"] + "/config"
    config_file_path_tmp = config_file_path + ".tmp"
    IPV4_SETTING_KEY = "lxc.network.ipv4 = "
    START_AUTO_SETTING_KEY = "lxc.start.auto = "
    ipv4_setting_value = \
        IPV4_SETTING_KEY + container_info["ip_address"] + "\n"
    start_auto_setting_value = \
        START_AUTO_SETTING_KEY + str(container_info["auto_start"]) + "\n"

    config_file_old = open(config_file_path, "r").readlines()
    content_for_new_file = []
    set_ipv4_setting = False
    set_auto_setting = False
    for line in config_file_old:
        if IPV4_SETTING_KEY in line:
            content_for_new_file.append(ipv4_setting_value)
            set_ipv4_setting = True
        elif START_AUTO_SETTING_KEY in line:
            content_for_new_file.append(start_auto_setting_value)
            set_auto_setting = True
        else:
            content_for_new_file.append(line)

    if not (set_ipv4_setting and set_auto_setting):
        append_content = [ipv4_setting_value, start_auto_setting_value]
        for content in append_content:
            content_for_new_file.append(content)

    open(config_file_path_tmp, "w").writelines(content_for_new_file)
    os.remove(config_file_path)
    os.rename(config_file_path_tmp, config_file_path)


def install_ifcfg_eth0_file(argument):
    ifcfg_eth0_data = argument[0]
    IFCFG_ETH0_PATH = "/etc/sysconfig/network-scripts/ifcfg-eth0"

    os.remove(IFCFG_ETH0_PATH)
    open(IFCFG_ETH0_PATH, "w").write(ifcfg_eth0_data)


def prepare_install_ifcfg_eth0_file(container_name):
    ifcfg_eth0_file = open("assets/ifcfg-eth0").read()
    argument = [ifcfg_eth0_file]

    container = lxc.Container(container_name)
    container.start()
    container.attach_wait(install_ifcfg_eth0_file, argument)
    shutdown_container(container)


def install_container_config(container_name, container_info):
    print("Install config files: %s" % container_name)
    if "monitor_group" in container_info:
        install_monitor_group_file(container_info)
    install_container_config_file(container_info)

    prepare_install_ifcfg_eth0_file(container_name)


def install_containers_config(list_of_container_info):
    for (container_name, container_info) in list_of_container_info:
        install_container_config(container_name, container_info)


def start_setup(yaml_file_path):
    config_info = get_config_info(yaml_file_path)
    list_of_setup_containers = \
        get_container_name_and_info(config_info, get_function_and_arguments)
    list_of_container_info = \
        get_container_name_and_info(config_info, get_container_info)
    setup_containers(list_of_setup_containers)
    install_containers_config(list_of_container_info)


if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    start_setup(argvs[1])
