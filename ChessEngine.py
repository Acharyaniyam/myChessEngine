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
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": getRookMoves, "N": getKnightMoves,
        "B": getBishopMoves, "Q": getQu}
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
                    if piece == 'p':
                        self.getPawnMoves(row, col, moves)
                    elif piece == 'R':
                        self.getRookMoves(row, col, moves)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, moves)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, moves)
                    elif piece == 'K':
                        self.getKingMoves(row, col, moves)
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
                if row == 2 and self.board[row+2][col] == "--":
                    moves.append(Move((row,col), (row+2,col), self.board))

            #Captures by black pawn:
            #Capture to the left -> Column should be greater than 0 again
            if col > 0:
                if self.board[row+1][col-1][0] == "b": 
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            
            #Captures to the right - Column should be less than 7
            if col < 7:
                if self.board[row + 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
            


    
    """
    Get all the Rook moves for the Rook located at the row, col and add these moves to the list
    """
    def getRookMoves(self, row, col, moves):
        pass
    
    """
    Get all the Knight moves for the knight located at the row, col and add these moves to the list
    """
    def getKnightMoves(self, row, col, moves):
        pass

    """
    Get all the Bishop moves for the Bishop located at the row, col and add these moves to the list
    """
    def getBishopMoves(self, row, col, moves):
        pass

    """
    Get all the Queen moves for the Queen located at the row, col and add these moves to the list
    """
    def getQueenMoves(self, row, col, moves):
        pass

    """
    Get all the King moves for the King located at the row, col and add these moves to the list
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


        
