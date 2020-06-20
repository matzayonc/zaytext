#! /usr/bin/python3
import socket
import pickle
import threading

TRACKER = "zayonc.pl"
DEFAULT_PORT= 8008


def update(sock, debug=True):
    sock.sendto(str.encode("open"), (TRACKER, 8008))

    res = sock.recvfrom(1024)
    global data
    data = pickle.loads(res[0])
    return data


def listen(sock, buffer=1024):
    while True:
        res, addr = sock.recvfrom(buffer)
        
        print(addr, str(res, 'utf-8'), sep=': ')
        
        if res == b'Elo' and addr != data['ext']:
            update(sock)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        sock.bind(("", DEFAULT_PORT))
        break
    except:
        DEFAULT_PORT += 1


data = update(sock)
t = threading.Thread(target=listen, args=(sock, 1024))

for i in data['peers']:
    sock.sendto(str.encode('Elo'), i)

t.start()

while True:
    message = str.encode(input())

    for peer in data['peers']:
        sock.sendto(message, peer)