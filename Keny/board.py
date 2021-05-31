from typing import Tuple
import pygame
from pygame.constants import GL_CONTEXT_PROFILE_COMPATIBILITY
from .constant import BLACK, GRAY, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BLUE, LIGHT_GRAY, CREME, BROWN
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
            for col in range(COLS):  # row % 2, COLS, 2
                pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(win, CREME, (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE-2, SQUARE_SIZE-2))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == 7 and piece.color ==WHITE:
            piece.make_king()
            self.white_kings += 1
        elif row == 0 and piece.color ==GRAY:
            self.grey_kings += 1
            piece.make_king()

    def get_piece(self, row, col):
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

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece !=0:
                if piece.color == GRAY:
                    self.grey_left -=1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.grey_left <= 0:
            return GRAY 
        elif self.white_left <= 0:
            return WHITE

        return None 

    def get_valid_moves(self, piece):
        moves = {}

        col = piece.col
        right_stop = 7
        step_left = -1
        step_right = 1
        left_stop = 0
        left = piece.col - 1
        right = piece.col + 1

        row = piece.row

        # direction: -1 w górę, 1 w dół, 0 w oba (plus jumpy nad swoimi oraz unlimited dystans)

        if piece.color == GRAY:
            direction = -1  # forward is up
        if piece.color == WHITE:
            direction = 1  # forward is down
        if piece.king:
            direction = 0  # both
        if piece.color==GRAY:
            moves.update(self._traverse_left(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right))
            moves.update(self._traverse_right(direction, row, col, piece.color,
                        right_stop, step_right, right, left_stop, step_left, left))
            moves.update(self._traverse_up(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right))
            moves.update(self._traverse_down(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right))
        else:
            moves.update(self._traverse_left(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right))
            moves.update(self._traverse_right(direction, row, col, piece.color,
                        right_stop, step_right, right, left_stop, step_left, left))
            moves.update(self._traverse_down(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right))
            moves.update(self._traverse_up(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right))
                     

        return moves

    def _traverse_left(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right, skipped=[]):
        moves = {}
        last = []
        friendly= False
        for r in range(col, left_stop, step_left):
            if left < 0:
                break
            
            current = self.board[row][left]
            if current == 0:
                if skipped and not last and not friendly:
                    break
                elif skipped and not friendly:
                    moves[(row, left)] = last + skipped
                else:
                    moves[(row, left)] = last
            
                if last and not friendly:
                    moves.update(self._traverse_left(direction, row, col-2, color, left_stop,
                                 step_left, left-1, right_stop, step_right, right-1, skipped=last))
                    moves.update(self._traverse_up(direction, row, col-2, color, left_stop,
                                 step_left, left-1, right_stop, step_right, right-1, skipped=last))
                    moves.update(self._traverse_down(direction, row, col-2, color, left_stop,
                                 step_left, left-1, right_stop, step_right, right-1, skipped=last))
                    # tu wsadzić szukanie kolejnych ruchów w górę i dół
                break

            elif current.color == color:
                #break              
                nextField = self.board[row][left-1]
                if nextField ==0:
                    last = [current]
                    friendly = True
                else:
                    break
                 #do skakania nad swoimi
            else:
                nextField = self.board[row][left-1]
                if nextField ==0:
                    last = [current]
                    
                else:
                    break

            left -= 1

        return moves

    def _traverse_right(self, direction, row, col, color, right_stop, step_right, right, left_stop, step_left, left, skipped=[]):
        moves = {}
        last = []
        friendly= False
        for r in range(col, right_stop, step_right):
            if right > 7:
                break

            current = self.board[row][right]
            if current == 0:
                if skipped and not last and not friendly:
                    break
                elif skipped and not friendly:
                    moves[(row, right)] = last + skipped
                else:
                    moves[(row, right)] = last

                if last and not friendly:
                    moves.update(self._traverse_right(direction, row, col+2, color, right_stop,
                                 step_right, right+1, left_stop, step_left, left+1, skipped=last))
                    moves.update(self._traverse_up(direction, row, col+2, color, left_stop,
                                 step_left, left+1, right_stop, step_right, right+1, skipped=last))
                    moves.update(self._traverse_down(direction, row, col+2, color, left_stop,
                                 step_left, left+1, right_stop, step_right, right+1, skipped=last))
                    # tu wsadzić szukanie kolejnych ruchów w górę i dół
                break

            elif current.color == color:
                #break     
                if right<7:
                    nextField = self.board[row][right+1]
                    if nextField ==0:
                        last = [current]
                        friendly = True
                    else:
                        break
                 #do skakania nad swoimi
            else:
                if right<7:
                    nextField = self.board[row][right+1]
                    if nextField ==0:
                        last = [current]   
                    else:
                        break

            right += 1

        return moves

    def _traverse_up(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right, skipped=[]):
        moves = {}
        last = []
        up = row - 1
        down = row + 1
        stop = 0
        step = -1
        friendly= False
        if direction == -1:  # going forward SZARY

            for r in range(row, stop, step):
                if up < 0:
                    break

                current = self.board[up][col]
                if current == 0:
                    if skipped and not last and not friendly:
                        break
                    elif skipped and not friendly:
                        moves[(up, col)] = last + skipped
                    else:
                        moves[(up, col)] = last

                    if last and not friendly:
                        moves.update(self._traverse_right(direction, row-2, col, color, right_stop,
                                     step_right, right, left_stop, step_left, left, skipped=last))
                        moves.update(self._traverse_left(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        moves.update(self._traverse_up(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        # tu wsadzić szukanie kolejnych ruchów w górę i dół i boki

                    break
                elif current.color == color:
                    #break
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                            friendly = True
                        else:
                            break #do skakania nad swoimi
                else:
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                        else:
                            break

                up -= 1

            return moves

        #TODO naprawić by tylko mógł bić
        elif direction == 1:  # going backward BIAŁY tylko bicie/ szary ruch do przodu
            
            for r in range(row, stop, step):
                if up < 0:
                    break

                current = self.board[up][col]
                if current == 0:
                    if skipped and not last and not friendly:
                        break
                    elif skipped and not friendly:
                        moves[(up, col)] = last + skipped
                   # else:
                     #   moves[(up, col)] = last

                    if last and not friendly:
                        moves.update(self._traverse_right(direction, row-2, col, color, right_stop,
                                     step_right, right, left_stop, step_left, left, skipped=last))
                        moves.update(self._traverse_left(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        moves.update(self._traverse_up(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        # tu wsadzić szukanie kolejnych ruchów w górę i dół i boki

                    break
                elif current.color == color:
                    #break
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                            friendly = True
                        else:
                            break #do skakania nad swoimi
                else:
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                        else:
                            break

                up -= 1
            
            return moves

    def _traverse_down(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right, skipped=[]):
        moves = {}
        last = []
        up = row - 1
        down = row + 1  # row + 1
        stop = 7
        step = 1
        friendly= False
        
        if direction == 1:  # going forward BIAŁY

            for r in range(row, stop, step):
                if down > 7:
                    break

                current = self.board[down][col]
                if current == 0:
                    if skipped and not last and not friendly:
                        break
                    elif skipped and not friendly:
                        moves[(down, col)] = last + skipped
                    else:
                        moves[(down, col)] = last

                    if last and not friendly:
                        moves.update(self._traverse_right(direction, row+2, col, color, right_stop,
                                     step_right, right, left_stop, step_left, left, skipped=last))
                        moves.update(self._traverse_left(direction, row+2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        moves.update(self._traverse_down(direction, row+2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        # tu wsadzić szukanie kolejnych ruchów w górę i dół i boki

                    break
                elif current.color == color:
                    #break
                    if down<7:
                        nextField = self.board[down+1][col]
                        if nextField ==0:
                            last = [current]
                            friendly = True
                        else:
                            break #do skakania nad swoimi
                    else: break
                elif current.color != color:
                    if down<7:
                        nextField = self.board[down+1][col]
                        if nextField ==0:
                            last = [current]
                        else:
                            break

                down += 1

            return moves

        #TODO naprawić by tylko mógł bić
        elif direction == -1:  # SZARY BACKWARDS
            
            for r in range(row, stop, step):
                if down > 7:
                    break

                current = self.board[down][col]
                if current == 0:
                    if skipped and not last and not friendly:
                        break
                    elif skipped and not friendly:
                        moves[(down, col)] = last + skipped
                        
                    else:
                      moves[(down, col)] = last

                    if last and not friendly:
                        moves.update(self._traverse_right(direction, row+2, col, color, right_stop,
                                     step_right, right, left_stop, step_left, left, skipped=last))
                        moves.update(self._traverse_left(direction, row+2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, skipped=last))
                        moves.update(self._traverse_down(direction, row+2, col, color, left_stop,
                                    step_left, left, right_stop, step_right, right, skipped=last))
                        # tu wsadzić szukanie kolejnych ruchów w górę i dół i boki

                    break
                elif current.color == color:
                    #break 
                    if down<7:
                        nextField = self.board[down+1][col]
                        if nextField ==0:
                            last = [current]
                            friendly = True
                        else:
                            break #do skakania nad swoimi  
                else:
                    if(color == GRAY):
                        if down<7:
                            nextField = self.board[down+1][col]
                            if nextField ==0:
                                last = [current]
                            else:
                                break
                    else: break
                    

                down += 1

            return moves
