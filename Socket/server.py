import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.39.142', 8080)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        data = connection.recv(255)
        message = data.decode()

        print('received',message)
        if data:
            print("Robot:",message)
        else:
            print('no data from', client_address)
            break
    except ValueError:
        # Clean up the connection
        connection.close()
