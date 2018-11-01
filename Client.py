"""
    udp socket client
    Silver Moon
"""

import socket  # for sockets
import sys  # for exit
from check import ip_checksum


# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 2163

while 1:
    msg = 'Enter message to send : '.encode()

    try:
        # Set the whole string
        s.sendto(msg, (host, port))

        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print('Server reply : ' + str(reply))

    except socket.error as msg:
        print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
