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
        self.whiteToMove = True
        self.moveLog = []
        #return self.board

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #because when we move a piece, when leave behind the square blank
        self.board[move.endRow][move.endCol] = move.pieceMoved #and now it moves a piece into its end position
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players


    
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
        self.pieceCaptured = board[self.endRow][self.endCol]
        
    
    def getChessNotation(self):
        #return self.getRankFile(self.startRow, self.startCol) + " "+ self.getRankFile(self.endRow, self.endCol)
        notation = ""
        piece = self.pieceMoved[1]

        return piece + self.getRankFile(self.startRow, self.startCol) + " -> " + piece + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row] #concatinate to get Notation of a piece like '1a'

        
