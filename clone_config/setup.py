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
    zabbix_conf_server = open("assets/zabbix_server.conf").read()
    zabbix_conf_httpd = open("assets/zabbix.conf").read()
    zabbix_conf_php = open("assets/zabbix.conf.php").read()
    argument.append(zabbix_conf_server)
    argument.append(zabbix_conf_httpd)
    argument.append(zabbix_conf_php)
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
    zabbix_agentd_conf = open("assets/zabbix_agentd.conf").read()
    argument.append(zabbix_agentd_conf)
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


def install_config_file_for_nagios(config_data, commands_data,
                                   config_path, commands_path,
                                   server_dir_path):
    PATH = [[config_data, config_path], [commands_data, commands_path]]
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
                                         password_file_path):
    if os.path.exists(password_file_path):
        os.remove(password_file_path)

    cmd = ["htpasswd", "-bc", password_file_path, username, password]
    subprocess.call(cmd)


def prepare_setup_nagios_server3(argument):
    nagios_conf = open("assets/nagios3.cfg").read()
    host_conf = open("assets/host_name.cfg").read()
    commands_conf = open("assets/commands3.cfg").read()
    cgi_conf = open("assets/cgi3.cfg").read()
    argument.append(nagios_conf)
    argument.append(host_conf)
    argument.append(commands_conf)
    argument.append(cgi_conf)
    return argument


def run_setup_nagios_server3(argument):
    list_of_monitored_host = argument[0]["target"]
    username = argument[0]["username"]
    password = argument[0]["password"]
    config_data = argument[1]
    host_data = argument[2]
    commands_data = argument[3]
    cgi_data = argument[4]
    CONFIG_PATH = "/etc/nagios/nagios.cfg"
    COMMANDS_PATH = "/etc/nagios/objects/commands.cfg"
    SERVER_DIR = "/etc/nagios/servers/"
    PASSWORD_PATH = "/etc/nagios/passwd"
    install_config_file_for_nagios(config_data, commands_data,
                                   CONFIG_PATH, COMMANDS_PATH,
                                   SERVER_DIR)
    add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     SERVER_DIR)
    set_username_and_password_for_nagios(username, password, PASSWORD_PATH)


def prepare_setup_nagios_server4(argument):
    nagios_conf = open("assets/nagios4.cfg").read()
    host_conf = open("assets/host_name.cfg").read()
    commands_conf = open("assets/commands3.cfg").read()
    cgi_conf = open("assets/cgi4.cfg").read()
    argument.append(nagios_conf)
    argument.append(host_conf)
    argument.append(commands_conf)
    argument.append(cgi_conf)
    return argument


def run_make_install_config_for_nagios4():
    os.chdir("/nagios-4.0.8")
    CMD = ["make", "install-config"]
    subprocess.call(CMD)


def run_setup_nagios_server4(argument):
    list_of_monitored_host = argument[0]["target"]
    username = argument[0]["username"]
    password = argument[0]["password"]
    config_data = argument[1]
    host_data = argument[2]
    commands_data = argument[3]
    cgi_data = argument[4]
    CONFIG_PATH = "/usr/local/nagios/etc/nagios.cfg"
    COMMANDS_PATH = "/usr/local/nagios/etc/objects/commands.cfg"
    SERVER_DIR = "/usr/local/nagios/etc/servers/"
    PASSWORD_PATH = "/usr/local/nagios/etc/htpasswd.users"
    run_make_install_config_for_nagios4()
    install_config_file_for_nagios(config_data, commands_data,
                                   CONFIG_PATH, COMMANDS_PATH,
                                   SERVER_DIR)
    add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     SERVER_DIR)
    set_username_and_password_for_nagios(username, password, PASSWORD_PATH)


def prepare_setup_nagios_nrpe(argument):
    nrpe_cfg = open("assets/nrpe.cfg").read()
    argument.append(nrpe_cfg)
    return argument


def run_setup_nagios_nrpe(argument):
    NRPE_FILE_PATH = "/etc/nagios/nrpe.cfg"
    os.remove(NRPE_FILE_PATH)

    nrpe_cfg = open(NRPE_FILE_PATH, "w")
    nrpe_cfg.write(argument[0])
    nrpe_cfg.close()


def prepare_setup_redmine(argument):
    file_list = ["database.yml", "configuration.yml", "my_setting"]

    for file_name in file_list:
        read_file = open(file_name)
        lines = read_file.readlines()
        read_file.close()

        argument.append(lines)

    return argument


def create_setup_file(file_path, argument):
    file = open(file_path, "w")
    file.writelines(argument)
    file.close()


def run_setup_redmine(argument):
    os.chdir("/var/lib/redmine")

    file_paths = ["/var/lib/redmine/config/database.yml",
                  "/var/lib/redmine/config/xonfiguration.yml",
                  "/var/lib/redmine/my_setting"]

    project_data = {
                    "project":{
                      "name": argument[0]["project_name"],
                      "identifier": argument[0]["project_id"]
                     }
                   }

    send_data = json.dumps(project_data)

    cmd = [
           ["bundle install --without development test"],
           ["bundle", "exec", "rake", "generate_secret_token"],
           ["RAILS_ENV=production bundle exec rake db:migrate"],
           ["passenger-install-apache2-module", "--snippet"],
           ["mysql -uroot db_redmine < my_setting"],
           ["chown", "-R", "apache", "/var/lib/redmine"],
           ["chgrp", "-R", "apache", "/var/lib/redmine"],
           ["service", "httpd", "restart"]
          ]

    for each_path_and_argument in range(len(file_paths)):
        create_setup_file(file_paths[each_path_and_argument],
                          argument[each_path_and_argument + 1])

    subprocess.call(cmd[0], shell = True)
    subprocess.Popen(cmd[1])
    subprocess.call(cmd[2], shell = True)
    subprocess.Popen(cmd[3], stdout = open("/etc/httpd/conf.d/passenger.conf", "w"))
    subprocess.call(cmd[4], shell = True)
    subprocess.Popen(cmd[5])
    subprocess.Popen(cmd[6])

    responce = requests.post("http://127.0.0.1/projects.json", data = send_data,
                             headers = {"Content-Type": "application/json"},
                             auth = ("admin", "admin"))

    subprocess.Popen(cmd[7])

def prepare_setup_fluentd(argument):
    td_agent_conf = open("assets/td-agent.conf").read()
    argument.append(td_agent_conf)
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


def get_container_name_and_function_to_setup(config_info_name):
    list_of_container_name = config_info_name.keys()
    return_list = []
    for container_name in list_of_container_name:
        info_of_container_name = config_info_name[container_name]
        list_of_key_in_info = info_of_container_name.keys()
        setup_functions = get_function_and_arguments(info_of_container_name,
                                                     list_of_key_in_info)
        return_list.append([container_name, setup_functions])

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


def start_setup(yaml_file_path):
    config_info = get_config_info(yaml_file_path)
    list_of_setup_containers = \
        get_container_name_and_function_to_setup(config_info)
    setup_containers(list_of_setup_containers)


if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    start_setup(argvs[1])
