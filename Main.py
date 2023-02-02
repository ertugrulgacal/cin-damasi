import pygame as p
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
                    squareSelected = ()
                    playerClicks = []  # reset user clicks

            elif e.type == p.KEYDOWN:  # key presses
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getAllPossibleMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# Graphics
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")]
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


if __name__ == "__main__":
    main()
