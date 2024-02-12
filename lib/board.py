from typing import List
import math
import random

from .errors import InvalidMoveError, AlreadyPlayedError
from .constants import EMPTY_SYMBOL

class Board:
    def __init__(self):
        self.none = EMPTY_SYMBOL
        self.board: List[str] = [self.none] * 9 
        # self.empty_squares = []


    def print(self):    
        j = 0
        
        print(' ')
        for i in range(3):
            start = j * 3
            end = start + 3

            board = self.board.copy()
            board[start + 1] += " "
            print(" ", " | ".join(board[start:end]), " ")

            if i < 2:
                print( " --  " * 3)
            
            if (i + 1) // 3 == 0:
                j = j + 1
        
        print(' ')
        
            
    def play(self, char: str, row: int, col: int) -> bool:
        if 0 > row or row > 2 or 0 > col or col > 2:
            raise InvalidMoveError(row=row, column=col)
        
        pos = (row * 3) + col
        if self.board[pos] == ' ':
            self.board[pos] = char
            return True

        else:
            raise AlreadyPlayedError(row, col)

        return False
    
    def get_value_at(self, row, column):
        pos = self.normalize(row, column)
        return self.board[pos]


    def copy(self):
        return self.board.copy()


    def check(self, row, column):
        pos = self.normalize(row, column)
        return self.check_normalized(pos)


    def unset(self, row, column):
        pos = self.normalize(row, column)
        self.board[pos] = self.none


    def is_empty(self, row, column):
        pos = self.normalize(row, column)
        if self.board[pos] != self.none:
            return False

        return True


    def check_normalized(self, last_played) -> bool:
        if self._check_row(last_played):
            return True

        if self._check_col(last_played):
            return True

        if self._check_major_diagonal(last_played):
            return True

        if self._check_minor_diagonal(last_played):
            return True

        return False


    def _check_row(self, last_played: int) -> bool:
        nrow = self.denormalize(last_played)[0]
        row = nrow * 3
        if self.board[row ] == self.board[row  + 1] == self.board[row + 2] and self.board[row] != self.none:
            return True
        return False


    def _check_col(self, last_played: int) -> bool:
        col = self.denormalize(last_played)[1]

        if self.board[col] == self.board[col + 3] == self.board[col + 6] and self.board[col] != self.none:
            return True
        return False


    def _check_major_diagonal(self, last_played: int) -> bool:
        if last_played not in [4, 8, 0]:
            return False

        if self.board[0] == self.board[4] == self.board[8] and self.board[4] != self.none:
            return True        
        return False
    

    def _check_minor_diagonal(self, last_played: int) -> bool:
        if last_played not in [2, 4, 6]:
            return False

        if self.board[2] == self.board[4] == self.board[6] and self.board[4] != self.none:
            return True
        return False


    def get_empty_squares(self, shuffle=False):
        squares = []

        for idx, value in enumerate(self.board):
            if value == self.none:
                squares.append(self.denormalize(idx))


        if shuffle:
            random.shuffle(squares)
            
        return squares

    
    @staticmethod         
    def denormalize(pos):
        row = pos // 3
        col = pos - (row * 3)
        return [row, col]


    @staticmethod
    def normalize(row, col):    
        return (row * 3) + col