#!/usr/bin/env python3
import sys
import encodings.idna
import apport
import requests
import json
sys.path.append("../common")
import definevalue

def send_data_and_get_response(send_content):
    send_data = json.dumps(send_content)
    response = requests.post(definevalue.ZABBIX_SERVER_ADDRESS,
                             data=send_data,
                             headers=definevalue.ZABBIX_API_HEADER)
    return response.json()


def get_authtoken_of_zabbix_server():
    SEND_CONTENT = {"method": "user.login",
                    "id": 1,
                    "params": {
                        "password": "zabbix",
                        "user":"Admin"},
                    "jsonrpc": "2.0"}
    response_json = send_data_and_get_response(SEND_CONTENT)

    return response_json["result"]


def get_linux_servers_group_id(auth_token):
    SEND_CONTENT = {"method": "hostgroup.get",
                    "id": 1,
                    "params": {
                        "output": "shorten",
                        "filter": {
                            "name": ["Linux servers"]
                        }
                    },
                    "auth": auth_token,
                    "jsonrpc": "2.0"}
    response_json = send_data_and_get_response(SEND_CONTENT)

    return response_json["result"][0]["groupid"]


def get_template_os_linux_id(auth_token):
    SEND_CONTENT = {"method": "template.get",
                    "id":1,
                    "params": {
                        "output": "shorten",
                        "filter": {
                            "name": ["Template OS Linux"]
                        }
                    },
                    "auth": auth_token,
                    "jsonrpc": "2.0"}
    response_json = send_data_and_get_response(SEND_CONTENT)

    return response_json["result"][0]["templateid"]


def add_monitored_hosts(list_of_monitored_host, group_id,
                        template_id, auth_token):
    for target_info in list_of_monitored_host:
        SEND_CONTENT = {"method": "host.create",
                        "id": 1,
                        "params": {
                            "host": target_info["host"],
                            "interfaces": [
                                {
                                    "type": 1,
                                    "main": 1,
                                    "useip": 1,
                                    "ip": target_info["ip"],
                                    "dns": "",
                                    "port": "10050"
                                }
                            ],
                            "groups": [
                                {
                                    "groupid": group_id
                                }
                            ],
                            "templates": [
                                {
                                    "templateid": template_id
                                }
                            ],
                        },
                        "auth": auth_token,
                        "jsonrpc": "2.0"}
        response_json = send_data_and_get_response(SEND_CONTENT)

        if "error" in response_json:
            print("The host is already added. %s: %s"
                  % (target_info["host"], target_info["ip"]))
        else:
            print("The host is added successfuly. %s: %s"
                  % (target_info["host"], target_info["ip"]))


def get_zabbix_server_id(auth_token):
    SEND_CONTENT = {"method": "host.get",
                    "id": 1,
                    "params": {
                        "output": "shorten",
                        "filter": {
                            "host": [
                                "Zabbix server"
                            ]
                        }
                    },
                    "auth": auth_token,
                    "jsonrpc": "2.0"}
    response_json = send_data_and_get_response(SEND_CONTENT)

    return response_json["result"][0]["hostid"]
