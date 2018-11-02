import socket
import sys
import time
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
timeout_test = True

# now keep talking with the client
while 1:
    # receive data from client (data, addr)
    data, addr = s.recvfrom(1024)

    checksum = data[:2]
    seq = data[2]
    pkt = data[3:]

    if not data:
        break
    # print(str(ip_checksum(pkt) == checksum))
  
    if ip_checksum(pkt) == checksum and seq == str(expect_seq):
        print('recv: Good Data Sending ACK' + str(seq))
        print('recv pkt: ' + str(pkt))
        if str(pkt) == 'Message 4':
           time.sleep(5)
        s.sendto(str(seq), addr)
        expect_seq = 1 - expect_seq
    else:
        if seq == str(expect_seq):
            print('recv: Bad Checksum Not Sending')
        else:
            print('recv: Bad Seq Sending ACK' + str(1 - expect_seq))
            s.sendto(str(1 - expect_seq), addr)

    # reply = 'OK...'.encode() + data
    # print('Message[' + str(addr[0]) + ':' + str(addr[1]) + '] - ' + str(data.strip()))

s.close()
