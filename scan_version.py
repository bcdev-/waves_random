#!/usr/bin/python3

import requests
from nodes import node_list

for node in node_list:
    try:
        r = requests.get('http://' + node + ':6869' + '/node/version')
        print(node, r.json()['version'])
    except Exception:
        print(node + " - DOWN!")

