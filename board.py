from random import *

class BoardPosition:
    def __init__(self, position, bomb_count=None, symbol="█"):
        self.line = position[0]
        self.column = position[1]
        self.bomb_count = bomb_count
        self.symbol = symbol

    def isEqualTo(self, second_position):
        return self.line==second_position.line and self.column==second_position.column

def countBombs(line, column, hidden_bombs):
    count = 0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if (line+i, column+j) in hidden_bombs:
                count+=1
    return count

class MineSweeperBoard:
    def __init__(self, width, height, bombs_quantity):
        self.width = width
        self.height = height
        self.bombs_quantity = bombs_quantity
        self.board = self.setBoard()
        self.cleared_positions = []

    def setHiddenBombsPositions(self):
        hidden_bombs = []
        while len(hidden_bombs) < self.bombs_quantity:
            rand = (randint(1, self.height), randint(1, self.width))
            if rand not in hidden_bombs:
                hidden_bombs.append(rand)

        print("\n----- \n Bombs at : ", hidden_bombs, "\n----- \n ")
        return hidden_bombs

    def setBoard(self):
        hidden_bombs = self.setHiddenBombsPositions()
        board = []
        for i in range(self.height):
            line_entries = []
            for j in range(self.width):
                line = i+1
                column = j+1
                if (line, column) in hidden_bombs:
                    line_entries.append(BoardPosition((line, column), "BOMB"))
                else:
                    line_entries.append(BoardPosition((line, column), countBombs(line, column, hidden_bombs)))
            board.append(line_entries)
        return board

    def positionHasBomb(self, board_position):
        line = board_position.line-1
        column = board_position.column-1
        return self.board[line][column].bomb_count=="BOMB"

    def getBombsQuantityFromPosition(self, board_position):
        line = board_position.line-1
        column = board_position.column-1
        return self.board[line][column].bomb_count

    def bombPosition(self, board_position):
        line = board_position.line-1
        column = board_position.column-1
        self.board[line][column].bomb_count = "BOMB"
        self.board[line][column].symbol = "☢"

    def clearRoundingZeroPositions(self, line, column):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if line+i>0 and line+i<=self.height and \
                column+j>0 and column+j<=self.width:
                    if (i,j)!=(0,0) and \
                    (line-1+i, column-1+j) not in self.cleared_positions and \
                    self.board[line-1+i][column-1+j].bomb_count==0:
                        self.clearPosition(BoardPosition((line+i,column+j)))

    def clearRoundingPositions(self, line, column):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if line+i>0 and line+i<=self.height and \
                column+j>0 and column+j<=self.width:
                    if (i,j)!=(0,0) and \
                    (line-1+i, column-1+j) not in self.cleared_positions and \
                    self.board[line-1+i][column-1+j].bomb_count!=0:
                        neighbor_bomb_count = self.board[line-1+i][column-1+j].bomb_count
                        self.board[line-1+i][column-1+j].symbol = str(neighbor_bomb_count)
                        self.cleared_positions.append((line-1+i, column-1+j))

    def clearPosition(self, board_position):
        line = board_position.line
        column = board_position.column
        bomb_count = self.board[line-1][column-1].bomb_count
        self.board[line-1][column-1].symbol = str(bomb_count)
        self.cleared_positions.append((line-1, column-1))

        self.clearRoundingZeroPositions(line, column)
        if bomb_count!=0:
            return
        self.clearRoundingPositions(line, column)

    def isVictorious(self):
        return self.height*self.width - self.bombs_quantity==len(self.cleared_positions)

    def printBoard(self):
        print("     |  ", end="")
        for j in range(self.width):
            print("", end="")
            print(j+1, end="  |  ")

        for i in range(self.height):
            print("\n\n   " + str(i+1) + " | ", end=" ")
            for j in range(self.width):
                print(self.board[i][j].symbol, end="  |  ")
