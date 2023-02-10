import socket

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("206.189.51.244", serverPort))
serverSocket.listen(1)
print("Server is listening")

while True:
    player1, _ = serverSocket.accept()
    print("player1 connected.")

    player2, _ = serverSocket.accept()
    print("player2 connected.")

    player1.send("white".encode())
    player2.send("black".encode())

    while True:
        # Game is on
        move = player1.recv(1024).decode()
        player2.send(move.encode())

        move = player2.recv(1024).decode()
        player1.send(move.encode())

