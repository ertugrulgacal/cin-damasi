import pygame as p
import Player

import Engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Loading piece images at the start of the program to not load them every time
def loadImages():
    pieces = ["wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = Engine.GameState()
    validMoves = gs.getAllPossibleMoves()
    moveMade = False  # to check if a move was made or not
    animate = False

    loadImages()  # load images at the start of the main
    running = True

    squareSelected = ()  # keeping track of last clicked square
    playerClicks = []  # keeping track of player clicks [(2, 3), (2, 5)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # mouse presses
                location = p.mouse.get_pos()  # get mouse locations
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                if squareSelected == (row, col):  # clicking the same square twice
                    squareSelected = ()  # unselect
                    playerClicks = []  # clear clicks
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)

                if len(playerClicks) == 2:  # move piece after 2nd click
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getNotation())
                    if move in validMoves:
                        gs.makeMove(move)  # make move
                        moveMade = True
                        animate = True
                        squareSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [squareSelected]

            elif e.type == p.KEYDOWN:  # undo move
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False

                if e.key == p.K_r:  # restart game
                    gs = Engine.GameState()
                    validMoves = gs.getAllPossibleMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                try:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock)
                except IndexError:
                    pass
            validMoves = gs.getAllPossibleMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, squareSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


# Graphics
def drawGameState(screen, gs, validMoves, squareSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, squareSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray40")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # draw squares


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # draw the pieces


def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('dark green'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQUARE_SIZE*move.endCol, SQUARE_SIZE*move.endRow))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 4
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
