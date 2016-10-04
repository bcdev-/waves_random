#!/usr/bin/python3

import requests, time
from nodes import node_list
from multiprocessing import Pool

#for node in node_list:
def scan(node):
    try:
        r = requests.get('http://' + node + ':6869' + '/blocks/height', timeout=10)
        print(node, r.json()['height'])
    except Exception:
        print(node, "failed")

p = Pool(len(node_list))
p.map(scan, node_list)
time.sleep(666)

