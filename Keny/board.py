import pygame
from .constant import BLACK, GRAY, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BLUE, LIGHT_GRAY, CREME,BROWN
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
     
        self.grey_left = self.white_left = 16
        self.grey_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, CREME, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS or row ==0:
            piece.make_king()
            if piece.color==WHITE:
                self.white_kings+=1
            else:
                self.grey_kings+=1

    def get_piece(self,row,col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row > 0 and row < 3:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row > 4 and row < 7:
                    self.board[row].append(Piece(row, col, GRAY))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)