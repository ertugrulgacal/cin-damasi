import socket

def getHostName():
    return socket.gethostbyname(socket.gethostname())

def connect(host):
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    port = 54254

    # connect to the server
    clientsocket.connect((host, port))
    print("Connected to the first peer")
    return clientsocket

def host():
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()
    port = 54254

    # bind to the port
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(1)

    print("Waiting for a connection...")

    # establish a connection
    clientsocket, addr = serversocket.accept()
    print("Connected to:", addr)

    return clientsocket

def sendMove(clientsocket, message):
    # send the message in lowercase
    clientsocket.send(message.encode('utf-8'))
    print("Sent:", message)

def recvMove(clientsocket):
    # receive and print the message from the second peer
    received_message = clientsocket.recv(1024).decode('utf-8')
    print("Received:", received_message)
    return received_message


def close(clientsocket):
    clientsocket.close()