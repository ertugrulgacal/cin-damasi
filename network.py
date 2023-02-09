import socket
import sys
import threading


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


def client():
    rendezvous = ("localhost", 55555)

    print("connecting to rendezvous server")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 50001))
    sock.sendto(b"0", rendezvous)

    while True:
        data = sock.recv(1024).decode()

        if data.strip() == "ready":
            print("checked in with the server, waiting")
            break

    data = sock.recv(1024).decode()
    ip, source_port, destination_port = data.split(" ")
    source_port = int(source_port)
    destination_port = int(destination_port)

    print("\ngot peer")
    print(f"\tip:\t{ip}")
    print(f"\tsource port:\t{source_port}")
    print(f"\tdestination port:\t{destination_port}")

    print("punching hole")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", source_port))
    sock.sendto(b"0", (ip, destination_port))

    def listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", source_port))

        while True:
            data = sock.recv(1024)
            print(f"\rpeer: {data.decode()}\n", end="")

    listener = threading.Thread(target=listen, daemon=True)
    listener.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", destination_port))

    while True:
        msg = input("> ")
        sock.sendto(msg.encode(), (ip, source_port))

client()