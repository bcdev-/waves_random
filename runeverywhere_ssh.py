#!/usr/bin/python3
import subprocess
import nodes
import time

command = """echo "cat waves-testnet.json | grep 4tTi2AdFh6KWXjik5X748tE19QuSDd5dHYzC6XZGh3RoM12pTYqCRvaRLPhFS3NSrjfGcvQV7mvVm96kB2FmMWWC8" """

for node in nodes.node_list:
    print("\t\t\t\t" + node)
    subprocess.run(command + " | ssh root@" + node, shell=True)

