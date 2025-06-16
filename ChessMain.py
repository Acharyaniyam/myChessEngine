"""
This is our main driver file. It will be responsible for handling user input and displaying the current 
GameState object.
"""

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512 #400 is also good option
DIMENSION = 8 #dimension of a chess board are 8x8
SQ_SIZE  = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

"""
Initialize a global dictinoary of images. This will be called exactly once in the main.
"""

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wQ', 'wK', 'wB', 'bp', 'bR', 'bN', 'bQ', 'bK', 'bB']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"), (SQ_SIZE, SQ_SIZE)) #transforming the image of the piece taking up the entire size of a square
    #Note: we can access an image by saving 'IMAGES['wp']


"""
The main driver for our code. This will handle user input and updating the graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    #print(gameState.board) #just a step to check the board

    loadImages()
    running = True

    while running: 
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all the graphics within a current game state.
"""

def drawGameState(screen, gs):
    drawBoard(screen) #draw the squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw the piece on top of those squares 



"""
Draw the squares on the board.
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("darkgreen")]
    for row in range(DIMENSION): #here i and j are rows and columns in the chess board 
        for column in range(DIMENSION):
            if (row+column) % 2 == 0:
                SQ_Color = p.Color("white")
            else:
                SQ_Color = p.Color("darkgreen")


            p.draw.rect(screen, SQ_Color, p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draw the rectangle on the SCREEN, with the SQ_Color and the rectangle object with col * row dimensions

"""
Draw the pieces on the board using the current GamState.board
"""
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            square = board[row][column] #this goes through the row number and then the column number
            if square != "--": #non empty
                screen.blit(IMAGES[square], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    


if __name__ == "__main__": 
    #reason to do this is if we want to call the main() function in another tab, we will type __main__, otherwise the main() function will only run in this python file 
    main()









