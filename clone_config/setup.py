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
sys.path.append('../common')
import definevalue
from utils import *
import clone
import zabbix


def prepare_setup_zabbix_server(argument):
    FILES = ['assets/zabbix_server.conf', 'assets/zabbix.conf',
             'assets/zabbix.conf.php']
    argument = load_asset_files(argument, FILES)
    return argument


def install_config_files_of_zabbix(zabbix_conf_server,
                                   zabbix_conf_httpd,
                                   zabbix_conf_php):
    ZABBIX_CONF_SERVER_PATH = '/etc/zabbix/zabbix_server.conf'
    ZABBIX_CONF_HTTPD_PATH = '/etc/httpd/conf.d/zabbix.conf'
    ZABBIX_CONF_PHP_PATH = '/etc/zabbix/web/zabbix.conf.php'
    INSTALL_FILES = [[definevalue.ZBX_SRV_PATH['CONFIG'], zabbix_conf_server],
                     [definevalue.ZBX_SRV_PATH['HTTPD'], zabbix_conf_httpd],
                     [definevalue.ZBX_SRV_PATH['PHP'], zabbix_conf_php]]
    for (path, content) in INSTALL_FILES:
        remove_file_if_exists(path)

        write_data_to_file(content, path)

    CMDS = [['service', 'httpd', 'restart'],
            ['service', 'zabbix-server', 'restart']]
    for run_command in CMDS:
        subprocess.call(run_command)


def start_zabbix_api_functions(list_of_monitored_host):
    auth_token = zabbix.get_authtoken_of_zabbix_server()

    zabbix_server_id = zabbix.get_zabbix_server_id(auth_token, 'Zabbix server')
    zabbix.enable_zabbix_server(zabbix_server_id, auth_token)

    group_id = zabbix.get_linux_servers_group_id(auth_token)
    template_id = zabbix.get_template_os_linux_id(auth_token)
    zabbix.add_monitored_hosts(list_of_monitored_host,
                               group_id, template_id, auth_token)


def run_setup_zabbix_server(argument):
    list_of_monitored_host = argument[0]['target']
    zabbix_conf_server = argument[1]
    zabbix_conf_httpd = argument[2]
    zabbix_conf_php = argument[3]
    install_config_files_of_zabbix(zabbix_conf_server,
                                   zabbix_conf_httpd,
                                   zabbix_conf_php)
    start_zabbix_api_functions(list_of_monitored_host)


def prepare_setup_zabbix_agent(argument):
    FILES = ['assets/zabbix_agentd.conf']
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_zabbix_agent(argument):
    remove_file_if_exists(definevalue.ZBX_AGT_PATH['CONFIG'])

    server_ip_and_host_name = argument[0]
    output_data = argument[1]

    SERVER_OLD = 'Server=127.0.0.1'
    SERVER_NEW = 'Server=' + server_ip_and_host_name['server_ipaddress']
    SERVER_ACTIVE_OLD = 'ServerActive=127.0.0.1'
    SERVER_ACTIVE_NEW = 'Server=' + server_ip_and_host_name['server_ipaddress']
    HOST_NAME_OLD = 'Hostname=Zabbix server'
    HOST_NAME_NEW = 'Hostname=' + server_ip_and_host_name['host_name']
    replace_sequence = [[SERVER_OLD, SERVER_NEW],
                        [SERVER_ACTIVE_OLD, SERVER_ACTIVE_NEW],
                        [HOST_NAME_OLD, HOST_NAME_NEW]]
    for (old, new) in replace_sequence:
        output_data = output_data.replace(old, new)
    write_data_to_file(output_data, definevalue.ZBX_AGT_PATH['CONFIG'])


def install_config_file_for_nagios(config_data, commands_data, ndo2db_data,
                                   config_path, commands_path, ndo2db_path,
                                   server_dir_path):
    PATH = [[config_data, config_path], [commands_data, commands_path],
            [ndo2db_data, ndo2db_path]]
    for (data, path) in PATH:
        remove_file_if_exists(path)
        write_data_to_file(data, path)

    if os.path.exists(server_dir_path):
        shutil.rmtree(server_dir_path)

    os.makedirs(server_dir_path)


def add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     server_path):
    EXTENSION = '.cfg'
    HOST_NAME_DEFAULT_HOST = '        host_name               host_name'
    HOST_NAME_PREFIX_HOST = '        host_name               '
    HOST_NAME_DEFAULT_SERVICE = \
        '        host_name                       host_name'
    HOST_NAME_PREFIX_SERVICE = \
        '        host_name                       '
    ALIAS_DEFAULT = 'alias                   host_name'
    ALIAS_PREFIX = 'alias                   '
    ADDRESS_DEFAULT = 'address                 127.0.0.1'
    ADDRESS_PREFIX = 'address                 '

    for monitored_info in list_of_monitored_host:
        output_data = host_data
        ip_address = monitored_info['ip']
        host_name = monitored_info['host']
        file_name = server_path + host_name + EXTENSION

        replace_points = [[HOST_NAME_DEFAULT_HOST,
                           HOST_NAME_PREFIX_HOST + host_name],
                          [ALIAS_DEFAULT, ALIAS_PREFIX + host_name],
                          [ADDRESS_DEFAULT, ADDRESS_PREFIX + ip_address],
                          [HOST_NAME_DEFAULT_SERVICE,
                           HOST_NAME_PREFIX_SERVICE + host_name]]
        for (old, new) in replace_points:
            output_data = output_data.replace(old, new)

        write_data_to_file(output_data, file_name)


def set_username_and_password_for_nagios(username, password,
                                         config_data, config_file_path,
                                         password_file_path):
    FILES = [config_file_path, password_file_path]
    for file_path in FILES:
        remove_file_if_exists(password_file_path)

    DEFAULT_USERNAME = 'nagiosadmin'
    config_data = config_data.replace(DEFAULT_USERNAME, username)
    write_data_to_file(config_data, config_file_path)

    cmd = ['htpasswd', '-bc', password_file_path, username, password]
    subprocess.call(cmd)


def run_setup_for_nagios_server(argument, list_of_path):
    list_of_monitored_host = argument[0]['target']
    username = argument[0]['username']
    password = argument[0]['password']
    config_data = argument[1]
    host_data = argument[2]
    commands_data = argument[3]
    cgi_data = argument[4]
    ndo2db_data = argument[5]

    install_config_file_for_nagios(config_data, commands_data, ndo2db_data,
                                   list_of_path['CONFIG'],
                                   list_of_path['COMMANDS'],
                                   list_of_path['NDO2DB'],
                                   list_of_path['SERVER_DIR'])
    add_hosts_files_to_nagios_server(list_of_monitored_host, host_data,
                                     list_of_path['SERVER_DIR'])
    set_username_and_password_for_nagios(username, password, cgi_data,
                                         list_of_path['CGI'],
                                         list_of_path['PASSWORD'])


def prepare_setup_nagios_server3(argument):
    FILES = ['assets/nagios3.cfg', 'assets/host_name.cfg',
             'assets/commands3.cfg', 'assets/cgi3.cfg',
             'assets/ndo2db3.cfg']
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_server3(argument):
    run_setup_for_nagios_server(argument, definevalue.NAGIOS3_PATH)


def prepare_setup_nagios_server4(argument):
    FILES = ['assets/nagios4.cfg', 'assets/host_name.cfg',
             'assets/commands3.cfg', 'assets/cgi4.cfg',
             'assets/ndo2db4.cfg']
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_server4(argument):
    run_setup_for_nagios_server(argument, definevalue.NAGIOS4_PATH)


def prepare_setup_nagios_nrpe(argument):
    FILES = ['assets/nrpe.cfg']
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_nagios_nrpe(argument):
    nrpe_cfg_file = argument[0]
    remove_file_if_exists(definevalue.NRPE_PATH['CONFIG'])

    write_data_to_file(nrpe_cfg_file, definevalue.NRPE_PATH['CONFIG'])


def prepare_setup_redmine(argument):
    FILES = ['assets/database.yml', 'assets/configuration.yml',
             'assets/my_setting', 'assets/setting_command.sh']
    argument = load_asset_files(argument, FILES)
    return argument


def print_request_responce(request_result):
    if request_result.status_code == 201:
        print('Successed to create a new project')

    else:
        print('Failed to create a new project.')
        print(request_result.text + '\n')


def run_setup_redmine(argument):
    os.chdir('/var/lib/redmine')

    file_path_and_data = \
        [[definevalue.REDMINE_PATH['DATABASE'], argument[1]],
         [definevalue.REDMINE_PATH['CONFIG'], argument[2]],
         [definevalue.REDMINE_PATH['MYSQL'], argument[3]],
         [definevalue.REDMINE_PATH['SHELL'], argument[4]]]

    project_info = argument[0]
    project_data = {'project': {'name': project_info['project_name'],
                                'identifier': project_info['project_id']}}

    send_data = json.dumps(project_data)

    for (path, data) in file_path_and_data:
        remove_file_if_exists(path)
        write_data_to_file(data, path)

    CMDS = [['sh', 'setting_command.sh'], ['service', 'httpd', 'restart']]
    for cmd in CMDS:
        subprocess.call(cmd)

    request_result = requests.post(definevalue.REDMINE_SERVER_ADDRESS,
                                   data=send_data,
                                   headers=definevalue.REDMINE_API_HEADER,
                                   auth=definevalue.REDMINE_USERNAME_PASSWORD)
    print_request_responce(request_result)


def prepare_setup_fluentd(argument):
    FILES = ['assets/td-agent.conf']
    argument = load_asset_files(argument, FILES)
    return argument


def run_setup_fluentd(argument):
    td_agent_conf_file = argument[0]
    remove_file_if_exists(definevalue.TD_AGENT_PATH['CONFIG'])

    write_data_to_file(td_agent_conf_file,
                       definevalue.TD_AGENT_PATH['CONFIG'])


SETUP_FUNCTIONS = {'zabbix-server': run_setup_zabbix_server,
                   'zabbix-agent': run_setup_zabbix_agent,
                   'nagios3': run_setup_nagios_server3,
                   'nagios4': run_setup_nagios_server4,
                   'nrpe': run_setup_nagios_nrpe,
                   'redmine': run_setup_redmine,
                   'fluentd': run_setup_fluentd}

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
        if key_in_info not in list_of_setup_function:
            continue
        else:
            info_of_function = info_of_container_name[key_in_info]
            function_argument = []
            if info_of_function is not None:
                function_argument.append(info_of_function)
            return_list.append([SETUP_FUNCTIONS[key_in_info],
                               function_argument])

    return return_list


def get_container_info(info_of_container, list_of_key_in_info):
    list_of_setup_function = SETUP_FUNCTIONS.keys()
    return_info = {}
    for key_in_info in list_of_key_in_info:
        if (key_in_info not in list_of_setup_function and
                key_in_info not in 'base_container'):
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
    print('Start setup process: %s' % container_name)
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
    group_file_path = os.path.join(container_info['container_path'], 'group')
    write_data_to_file(str(container_info['monitor_group']), group_file_path)


def install_container_config_file(container_info):
    config_file_path = os.path.join(container_info['container_path'], 'config')
    config_file_path_tmp = config_file_path + '.tmp'
    IPV4_SETTING_KEY = 'lxc.network.ipv4 = '
    IPV4_GATEWAY_SETTING_KEY = 'lxc.network.ipv4.gateway = '
    START_AUTO_SETTING_KEY = 'lxc.start.auto = '
    ipv4_setting_value = \
        IPV4_SETTING_KEY + container_info['ip_address'] + '\n'
    ipv4_gateway_setting_value = \
        IPV4_GATEWAY_SETTING_KEY + container_info['gateway'] + '\n'
    start_auto_setting_value = \
        START_AUTO_SETTING_KEY + str(container_info['auto_start']) + '\n'

    config_file_old = read_data_from_file(config_file_path, True)
    content_for_new_file = []
    set_ipv4_setting = False
    set_ipv4_gateway_setting = False
    set_auto_setting = False
    for line in config_file_old:
        if IPV4_SETTING_KEY in line:
            content_for_new_file.append(ipv4_setting_value)
            set_ipv4_setting = True
        elif IPV4_GATEWAY_SETTING_KEY in line:
            content_for_new_file.append(ipv4_gateway_setting_value)
            set_ipv4_gateway_setting = True
        elif START_AUTO_SETTING_KEY in line:
            content_for_new_file.append(start_auto_setting_value)
            set_auto_setting = True
        else:
            content_for_new_file.append(line)

    if not (set_ipv4_setting and set_ipv4_gateway_setting
            and set_auto_setting):
        append_content = [ipv4_setting_value, ipv4_gateway_setting_value,
                          start_auto_setting_value]
        for content in append_content:
            content_for_new_file.append(content)

    write_data_to_file(content_for_new_file, config_file_path_tmp, True)
    remove_file_if_exists(config_file_path)
    os.rename(config_file_path_tmp, config_file_path)


def install_ifcfg_eth0_file(argument):
    ifcfg_eth0_data = argument[0]
    IFCFG_ETH0_PATH = '/etc/sysconfig/network-scripts/ifcfg-eth0'

    remove_file_if_exists(IFCFG_ETH0_PATH)
    write_data_to_file(ifcfg_eth0_data, IFCFG_ETH0_PATH)


def prepare_install_ifcfg_eth0_file(container_name):
    FILE = ['assets/ifcfg-eth0']
    argument = []
    argument = load_asset_files(argument, FILE)

    container = lxc.Container(container_name)
    container.start()
    container.attach_wait(install_ifcfg_eth0_file, argument)
    shutdown_container(container)


def install_container_config(container_name, container_info):
    print('Install config files: %s' % container_name)
    if 'monitor_group' in container_info:
        install_monitor_group_file(container_info)
    install_container_config_file(container_info)

    prepare_install_ifcfg_eth0_file(container_name)


def install_containers_config(list_of_container_info):
    for (container_name, container_info) in list_of_container_info:
        install_container_config(container_name, container_info)


def start_setup_containers(yaml_file_path):
    config_info = get_config_info(yaml_file_path)
    list_of_setup_containers = \
        get_container_name_and_info(config_info, get_function_and_arguments)
    list_of_container_info = \
        get_container_name_and_info(config_info, get_container_info)
    setup_containers(list_of_setup_containers)
    install_containers_config(list_of_container_info)

    print('Finish setup container process!\n')


if __name__ == '__main__':
    argvs = sys.argv
    exit_if_user_run_this_as_general_user()
    exit_if_argument_is_not_given(len(argvs))

    start_setup_containers(argvs[1])
