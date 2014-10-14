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
