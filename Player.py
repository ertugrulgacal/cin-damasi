import socket


def notation_to_square(squareNotation):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    return (filesToCols[squareNotation[0]], ranksToRows[squareNotation[1]])


class Player:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverName = "206.189.51.244"
    serverPort = 12000

    def __init__(self):
        self.color = self.connect()

    def connect(self):
        self.clientSocket.connect((self.serverName, self.serverPort))
        color = self.clientSocket.recv(1024)
        return color

    def disconnect(self):
        self.clientSocket.close()

    def send(self, move):
        self.clientSocket.send(move.encode())

    def receive_squares(self):
        move = self.clientSocket.recv(1024)
        startSquare = notation_to_square(move[:2])
        endSquare = notation_to_square(move[2:])
        return startSquare, endSquare


player = Player()
player.connect()

while True:
    player.send(input("> "))
    print("Received:", player.receive_squares())
