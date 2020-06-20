#! /usr/bin/env python3

import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind(("", 8008))

peers = []


while True:
    data, addr = sock.recvfrom(1024)
    print("received message: ", data, "from address: ", addr)
    
    if addr not in peers:
        peers.append(addr)

    res = {
        "ext": addr,
        "peers": peers
    }

    sock.sendto(pickle.dumps(res), addr)