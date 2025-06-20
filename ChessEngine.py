"""
This class is responsible for starting all the information about the current state of a chess game. 
It will also be responsible for determining the valid moves at the current state
It will also keep a move log.
"""

class GameState():
    def __init__(self):
        #board is an BxB 2d list, each element of the list has 2 characters.
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represe4ntys the type of the piece, 'K', 'Q'....
        #"--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "wp", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wR", "--", "--", "bB", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
        "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        #return self.board

    """
    Takes a move as a paramater and executes it (will not work for castling, en passant, and pawn promotion)
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #because when we move a piece, when leave behind the square blank
        self.board[move.endRow][move.endCol] = move.pieceMoved #and now it moves a piece into its end position
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players

    """
    Undo the last move made
    """
    def undoMove(self, move): 
#reverse the actions done in makeMove, and since it is recorded in moveLog, 
# see the last move that was made and reverse it
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    """
    All moves considering checks
    """
    def getValidMoves(self):
         return self.getAllPossibleMoves() #for now we will not worry about checks

    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves  = []
        for row in range(len(self.board)): #number of rows
            for col in range(len(self.board[row])): #number of columns in a given row
                turn = self.board[row][col][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):                    
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves) #calls the appropriate move function based on piece type
        return moves


    """
    Get all the pawn moves for the pawn located at the row, col and add these moves to the list
    White pawns move up the board and black pawns move down the board.
    Pawns can not go backwards.
    Pawns capture diagonally forward.
    Pawns can move 2 squares forward if its the first move.
    If you can make a one-square move, you can possibly make a two-square move.
    """
    def getPawnMoves(self,row, col, moves):
        if self.whiteToMove == True: #white pawn moves
            if self.board[row-1][col] == "--" : #One square pawn advance
                moves.append(Move((row,col), (row-1,col), self.board))
                if row == 6 and self.board[row-2][col] == "--": #Two square pawn advance
                    moves.append(Move((row,col), (row-2,col), self.board))
            
            #Captures by white pawn:
            #Capture to the left -> column should be greater than 0. Can't left capture beyond the board limit
            if col > 0:
                if self.board[row - 1][col - 1][0] == "b": #black piece to capture
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            
            #Captures to the right -> column should be less than 7
            if col < 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row -1, col + 1), self.board))

        else: #black pawn moves
            if self.board[row+1][col] == "--":
                moves.append(Move((row,col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row,col), (row+2,col), self.board))

            #Captures by black pawn:
            #Capture to the left -> Column should be greater than 0 again
            if col > 0:
                if self.board[row+1][col-1][0] == "w": 
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            
            #Captures to the right - Column should be less than 7
            if col < 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    
    """
    Get all the Rook moves for the Rook located at the row, col and add these moves to the list
    To things to check:
    1. Move as many squares as you can until you run into a piece
    Check going up; is the square above me is empty? if so check the next square until you run into a piece (for loop or while loop)
    It will be a valid move if run into a opposite color piece or is empty and then you end the loop(break)
    2. We also stop if we run into the edge of the board
    DO it in all four directions
    """
    def getRookMoves(self, row, col, moves):
        if self.whiteToMove == True: #white Rook moves
            #Rook moving upward
            for i in range(1,8):
                    if row - i < 0: #trying to see the edge of the board. Since here the rook moves upward only, row number should be greater than 0 only
                        break
                    if self.board[row - i][col] == "--":
                        moves.append(Move((row,col), (row - i, col), self.board))
                    elif self.board[row -i][col][0] == "b":
                        moves.append(Move((row,col), (row - i, col), self.board))
                        break
                    else:
                        break
            #Rook moving downward
            for i in range(1,8):
                    if row + i > 7 : #trying to see the edge of the board. Since here the rook moves downward only, row number should be less than 8
                        break
                    if self.board[row + i][col] == "--":
                        moves.append(Move((row,col), (row + i, col), self.board))
                    elif self.board[row + i][col][0] == "b":
                        moves.append(Move((row,col), (row + i, col), self.board))
                        break
                    else:
                        break
            #Rook moving rightward
            for i in range(1,8):
                    if col + i > 7 : #trying to see the edge of the board. Since here the rook moves rightward only, column number should be less than 8
                        break
                    if self.board[row][col + 1] == "--":
                        moves.append(Move((row,col), (row, col + i), self.board))
                    elif self.board[row][col + 1][0] == "b":
                        moves.append(Move((row,col), (row, col + i), self.board))
                        break
                    else:
                        break
            #Rook moving leftward
            for i in range(1,8):
                    if col - i < 0: #trying to see the edge of the board. Since here the rook moves leftward only, row number should be greater than 0 only
                        break
                    if self.board[row][col - i] == "--":
                        moves.append(Move((row,col), (row, col - i), self.board))
                    elif self.board[row][col - i][0] == "b":
                        moves.append(Move((row,col), (row, col - i), self.board))
                        break
                    else:
                        break
        else:
                        #Rook moving upward
            for i in range(1,8):
                    if row - i < 0: #trying to see the edge of the board. Since here the rook moves upward only, row number should be greater than 0 only
                        break
                    if self.board[row - i][col] == "--":
                        moves.append(Move((row,col), (row - i, col), self.board))
                    elif self.board[row -i][col][0] == "w":
                        moves.append(Move((row,col), (row - i, col), self.board))
                        break
                    else:
                        break
            #Rook moving downward
            for i in range(1,8):
                    if row + i > 7 : #trying to see the edge of the board. Since here the rook moves downward only, row number should be less than 8
                        break
                    if self.board[row + i][col] == "--":
                        moves.append(Move((row,col), (row + i, col), self.board))
                    elif self.board[row + i][col][0] == "w":
                        moves.append(Move((row,col), (row + i, col), self.board))
                        break
                    else:
                        break
            #Rook moving rightward
            for i in range(1,8):
                    if col + i > 7 : #trying to see the edge of the board. Since here the rook moves rightward only, column number should be less than 8
                        break
                    if self.board[row][col + 1] == "--":
                        moves.append(Move((row,col), (row, col + i), self.board))
                    elif self.board[row][col + 1][0] == "w":
                        moves.append(Move((row,col), (row, col + i), self.board))
                        break
                    else:
                        break
            #Rook moving leftward
            for i in range(1,8):
                    if col - i < 0: #trying to see the edge of the board. Since here the rook moves leftward only, row number should be greater than 0 only
                        break
                    if self.board[row][col - i] == "--":
                        moves.append(Move((row,col), (row, col - i), self.board))
                    elif self.board[row][col - i][0] == "w":
                        moves.append(Move((row,col), (row, col - i), self.board))
                        break
                    else:
                        break
                    
    """
    Get all the Knight moves for the knight located at the row, col and add these moves to the list
    Similar to the King -> interate over the 8 possible moves, checking for the edge of the board. 
    Dont worry what is around them; worry about the square they are landing on whether its an enemy piece or not.
    """
    def getKnightMoves(self, row, col, moves):
        pass

    """
    Get all the Bishop moves for the Bishop located at the row, col and add these moves to the list
    Same idea as rook but instead of up down left right we are looking at diagonals

    """
    def getBishopMoves(self, row, col, moves):
        pass

    """
    Get all the Queen moves for the Queen located at the row, col and add these moves to the list
    Mix of bishop and rook. Do at last
    """
    def getQueenMoves(self, row, col, moves):
        pass

    """
    Get all the King moves for the King located at the row, col and add these moves to the list
    Iterate over the possible 8 squares to see if you can move around. Check for edge of the board.
    """
    def getKingMoves(self, row, col, moves):
        pass



class Move():

    # maps key to values
    # key : value
    #the following is done because white queen should always be in white square and the square 1a should have a white rook
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                    "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                    "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0] #because startSq is a tuple: (row, col) from the 'SQselected' variable : this one is for source click
        self.startCol = startSq[1]
        self.endRow = endSq[0] #because there are 2 SQselected appended into playerClicks: this one is for dest click
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] #returns the captured piece
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #first 2 numbers will be the start row and col number, second 2 numbers will be the end row and column number
        print(self.moveID)

    """
    Overriding the equals method
    """    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False

    
    def getChessNotation(self):
        #return self.getRankFile(self.startRow, self.startCol) + " "+ self.getRankFile(self.endRow, self.endCol)
        notation = ""
        piece = self.pieceMoved[1]

        return piece + self.getRankFile(self.startRow, self.startCol) + " -> " + piece + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row] #concatinate to get Notation of a piece like '1a'


  
