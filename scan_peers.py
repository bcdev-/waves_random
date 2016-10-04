#!/usr/bin/python3

import requests
from nodes import node_list

for node in node_list:
    r = requests.get('http://' + node + ':6869' + '/peers/connected')
    print(node, len(r.json()['peers']))

