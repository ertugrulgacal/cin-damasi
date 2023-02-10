import socket

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("206.189.51.244", serverPort))
serverSocket.listen(1)
print("Server is listening")

while True:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("connectionSocket: ", connectionSocket, "addr:", addr)

        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()

        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()
