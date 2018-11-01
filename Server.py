import socket
import sys
from check import ip_checksum

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 2163  # Arbitrary non-privileged port

# Datagram (udp) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

expect_seq = 0

# now keep talking with the client
while 1:
    # receive data from client (data, addr)
    data, addr = s.recvfrom(1024)

    checksum = data[:2]
    seq = data[2]
    pkt = data[3]

    if not data:
        break

    if ip_checksum(data) == checksum:
        s.sendto("ACK" + seq, addr)

    reply = 'OK...'.encode() + data

    s.sendto(reply, addr)
    print('Message[' + str(addr[0]) + ':' + str(addr[1]) + '] - ' + str(data.strip()))

s.close()
