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
    
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages()
    running = True

    SQselected = () #no square is selected, keeps track of the last click of the user (tuple: row, column)
    playerClicks = [] #keeps track of player clicks which is 'piece from' and 'piece to' locations(two tuples: )
    while running: 
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            #mouse handlers    
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE #because location =column* SQ_SIZE
                row = location[1]//SQ_SIZE  
                if SQselected == (row,col): #checks to see if the player selected the same square twice
                    SQselected = () #this deselects the square/piece
                    playerClicks = [] #clear player clicks, renewing the selecting process
                else: 
                    SQselected = (row,col)
                    playerClicks.append(SQselected) #append for both 1st and 2nd click
                if len(playerClicks) ==2: #after the second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    
                    SQselected = () #reset user click
                    playerClicks = []
            
            #key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True #in order to trigger the moveMade, create another assortment of valid moves 

        if moveMade: #creates another assortment of valid moves
            validMoves = gs.getValidMoves()
            moveMade = False

                
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
