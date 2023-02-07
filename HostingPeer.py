import socket

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

    while True:
        message = input("Enter a message: ")

        # send the message in lowercase
        message = message.lower()
        clientsocket.send(message.encode('utf-8'))
        print("Sent:", message)

        # receive and print the message from the second peer
        received_message = clientsocket.recv(1024).decode('utf-8')
        print("Received:", received_message)

    clientsocket.close()

host()