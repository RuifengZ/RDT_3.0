"""
    udp socket client
    Silver Moon
"""

import socket  # for sockets
import sys  # for exit
from socket import timeout
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 2163

s.settimeout(5)
seq = 0
msg = 'Message '

for i in range(3):
    msg += str(i)
while 1:
    ack_received = False
    while not ack_received:
        try:
            # Set the whole string
            s.sendto(ip_checksum(msg) + str(seq) + msg, (host, port))
        except socket.error as msg:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        try:
            # receive data from client (data, addr)
            reply, addr = s.recvfrom(1024)
            ack = reply[0]
        except timeout:
            print('send: TIMEOUT')
        else:
            if ack == str(seq):
                print('send: ACK CORRECT')
                ack_received = True

    seq = 1 - seq
    # print('Server reply : ' + str(reply))
