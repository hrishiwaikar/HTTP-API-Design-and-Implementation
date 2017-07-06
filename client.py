import socket
import sys
import struct
import time


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data



print 'Enter correct url for server in form -  http://serveraddress:port/'

url = raw_input('eg. http://localhost:10025/ : ')

hostaddress = url.split('//')
hostdata = hostaddress[1].split(':')
host = hostdata[0]
port = (hostdata[1].split('/'))
port = port[0]
#print host
#print port

while True:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (host, int(port))
    print
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        # Send data
        time.sleep(0.1)
        message = raw_input('Enter the http request uri : ')
        print >> sys.stderr, 'sending request "%s"' % message
        send_msg(sock, message)


        # Receive data
        data = recv_msg(sock)
        print >> sys.stderr, 'received response "%s"' % data

    finally:
        print >> sys.stderr, 'closing socket'
        sock.close()




#PUT /job
