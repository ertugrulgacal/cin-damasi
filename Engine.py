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
        self.whiteToMove = not self.whiteToMove  # change turn

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved  # take the piece back to its position
            self.board[move.endRow][move.endCol] = "--"  # remove the piece in the position we put it in
            self.whiteToMove = not self.whiteToMove

    def getAllPossibleMoves(self):  # All legal moves
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                pieceColor = self.board[r][c][0]
                if (pieceColor == 'w' and self.whiteToMove) or (pieceColor == 'b' and not self.whiteToMove):
                    self.getMoves(r, c, moves)
        return moves

    def getMoves(self, r, c, moves):  # All legal moves of a specific piece
        if self.whiteToMove:  # white pieces
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
            if self.board[r][c+1] == "--":
                moves.append(Move((r, c), (r, c+1), self.board))
            if (0 <= r <= 2) and (5 <= c <= 7):
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))

        else:  # black pieces
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
            if self.board[r][c-1] == "--":
                moves.append(Move((r, c), (r, c-1), self.board))


class Move():
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