import socket

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("206.189.51.244", serverPort))
serverSocket.listen(1)
print("Server is listening")

while True:
    connectionSocket, addr1 = serverSocket.accept()
    player1 = connectionSocket
    print("player1 connected.")
    player1.send("white".encode())

    connectionSocket, addr2 = serverSocket.accept()
    player2 = connectionSocket
    print("player2 connected.")
    player2.send("black".encode())

    while True:
        # Game is on
        move = player1.recv(1024).decode()
        player2.send(move.encode())

        move = player2.recv(1024).decode()
        player1.send(move.encode())


    connectionSocket.close()
