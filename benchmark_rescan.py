#!/usr/bin/python3

import requests
import time
NODE = "46.101.215.195:6869"
TARGET_BLOCK = 150500

while True:
    try:
        r = requests.get('http://' + NODE + '/blocks/height', timeout=10)
        start = time.time()
        print("Starting! Current time:", start)
        print("Current block:", r.json()['height'])
        break
    except requests.exceptions.ConnectionError:
        print("Node is down, waiting...")
    except Exception:
        import traceback
        traceback.print_exc()
    time.sleep(1)

while True:
    try:
        r = requests.get('http://' + NODE + '/blocks/height', timeout=10)
        current = time.time()
        print("Block:", r.json()['height'], "Time:", current - start)
        if r.json()['height'] >= TARGET_BLOCK:
            print("Benchmark done. Node synchronized", r.json()['height'], "blocks in", current - start, "time")
            print((r.json()['height'] / (current - start)), "blocks per second")
            break
    except Exception:
        import traceback
        traceback.print_exc()
    time.sleep(1)


