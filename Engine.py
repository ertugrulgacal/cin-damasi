import numpy as np


class GameState():
    def __init__(self):
        self.board = np.array([
            ["--", "--", "--", "--", "--", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "--", "--", "--", "--", "--"]
        ])

        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # the square the piece left becomes empty
        self.board[move.endRow][move.endCol] = move.pieceMoved  # the square the piece arrives at
        self.moveLog.append(move)  # logging the move
        # self.whiteToMove = not self.whiteToMove  # change turn

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved  # take the piece back to its position
            self.board[move.endRow][move.endCol] = "--"  # remove the piece in the position we put it in
            self.whiteToMove = not self.whiteToMove

    def getAllPossibleMoves(self, player):  # All legal moves
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                pieceColor = self.board[r][c][0]
                # if (pieceColor == 'w' and self.whiteToMove and player == "white" ) \
                #         or (pieceColor == 'b' and not self.whiteToMove and player == "black"):
                if (pieceColor == 'w' and self.whiteToMove) or (pieceColor == 'b' and not self.whiteToMove):
                    self.getMoves(r, c, moves)
        return moves

    def getMoves(self, r, c, moves):  # All legal moves of a specific piece
        if self.whiteToMove:  # white pieces
            try:  # Move up
                if self.board[r-1][c] == "--":
                    moves.append(Move((r, c), (r-1, c), self.board))
            except IndexError:
                pass

            try:  # Move right
                if self.board[r][c+1] == "--":
                    moves.append(Move((r, c), (r, c+1), self.board))
            except IndexError:
                pass

            if (0 <= r <= 2) and (5 <= c <= 7):  # Checking if we can move backwards (if we are in opponents squares)
                if self.board[r+1][c] == "--" and (0 <= r+1 <= 2):
                    moves.append(Move((r, c), (r+1, c), self.board))
                if self.board[r][c-1] == "--" and (5 <= c-1 <= 7):
                    moves.append(Move((r, c), (r, c-1), self.board))
            self.getJumpingMoves(r, c, moves, (r, c))

        else:  # black pieces
            try:  # Move down
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
            except IndexError:
                pass

            try:  # Move left
                if self.board[r][c-1] == "--":
                    moves.append(Move((r, c), (r, c-1), self.board))
            except IndexError:
                pass

            if (5 <= r <= 7) and (0 <= c <= 2):  # Checking if we can move backwards (if we are in opponents squares)
                if self.board[r-1][c] == "--" and (5 <= r-1 <= 7):
                    moves.append(Move((r, c), (r-1, c), self.board))
                if self.board[r][c+1] == "--" and (0 <= c+1 <= 2):
                    moves.append(Move((r, c), (r, c+1), self.board))
            self.getJumpingMoves(r, c, moves, (r, c))

    def getJumpingMoves(self, r, c, moves, originalSquare):  # Calculating legal moves where we jump on top of pieces.
        # originalSquare is needed, so we don't forget the starting square while doing recursion
        # saving the location of the piece when the function is called for the first time in getMoves()
        startRow = originalSquare[0]
        startCol = originalSquare[1]
        if self.whiteToMove:  # white pieces
            try:
                if self.board[r-1][c] != "--" and self.board[r-2][c] == "--":  # Checking if we can jump
                    moves.append(Move((startRow, startCol), (r-2, c), self.board))
                    self.getJumpingMoves(r-2, c, moves, originalSquare)  # Recursion
            except IndexError:
                pass

            try:
                if self.board[r][c+1] != "--" and self.board[r][c+2] == "--":  # Checking the other direction
                    moves.append(Move((startRow, startCol), (r, c+2), self.board))
                    self.getJumpingMoves(r, c+2, moves, originalSquare)
            except IndexError:
                pass

            if (0 <= startRow <= 2) and (5 <= startCol <= 7):  # moving backwards in opponents squares
                if startRow == 0:
                    if self.board[startRow+1][startCol] != "--" and self.board[startRow+2][startCol] == "--":
                        moves.append(Move((startRow, startCol), (r+2, c), self.board))
                if startCol == 7:
                    if self.board[startRow][startCol-1] != "--" and self.board[startRow][startCol-2] == "--":
                        moves.append(Move((startRow, startCol), (r, c-2), self.board))

        else:  # black pieces
            try:
                if self.board[r+1][c] != "--" and self.board[r+2][c] == "--":  # Checking if we can jump
                    moves.append(Move((startRow, startCol), (r+2, c), self.board))
                    self.getJumpingMoves(r+2, c, moves, originalSquare)  # Recursion
            except IndexError:
                pass

            try:
                if self.board[r][c-1] != "--" and self.board[r][c-2] == "--":  # Checking the other direction
                    moves.append(Move((startRow, startCol), (r, c-2), self.board))
                    self.getJumpingMoves(r, c-2, moves, originalSquare)  # Recursion
            except IndexError:
                pass

            if (5 <= startRow <= 7) and (0 <= startCol <= 2):  # moving backwards in opponents squares
                if startRow == 7:
                    if self.board[startRow-1][startCol] != "--" and self.board[startRow-2][startCol] == "--":
                        moves.append(Move((startRow, startCol), (r-2, c), self.board))
                if startCol == 0:
                    if self.board[startRow][startCol+1] != "--" and self.board[startRow][startCol+2] == "--":
                        moves.append(Move((startRow, startCol), (r, c+2), self.board))


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}  # Converting our rows and columns to notation a1, b6 etc.

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.movID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol*1  # representing a move as a 4-digit number

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.movID == other.movID
        else:
            return False

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r ,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

def notationToSquare(squareNotation):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    return (filesToCols[squareNotation[0]], ranksToRows[squareNotation[1]])