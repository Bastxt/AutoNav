import socket
import sys
        
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.39.142', 8080)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

def sendMsg(msg):
    sock.sendall(message)

try:
    # Send data
    message = '304,200'
    print('sending: ',message)
    message = message.encode()
    
    sock.send(message)

    # Look for the response
    amount_received = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    amount_expected = len(message)
except ValueError:
    print('closing socket')
    sock.close()