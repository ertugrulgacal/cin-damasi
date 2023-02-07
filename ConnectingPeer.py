import socket

def connect(host):
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    port = 54254

    # connect to the server
    clientsocket.connect((host, port))
    print("Connected to the first peer")

def send(clientsocket):
    # receive and print the message from the first peer
    received_message = clientsocket.recv(1024).decode('utf-8')
    print("Received:", received_message)
    message = input("Enter a message: ")
    # send the message in uppercase
    message = message.upper()
    clientsocket.send(message.encode('utf-8'))
    print("Sent:", message)


def close(clientsocket):
    clientsocket.close()