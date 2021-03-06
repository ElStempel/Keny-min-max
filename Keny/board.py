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

    def evaluate(self):
        return self.white_left - self.grey_left + (self.white_kings * 0.25 - self.grey_kings * 0.25)
        #self.white_left - self.grey_left + (self.white_kings * 0.5 - self.grey_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

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

        # direction: -1 w g??r??, 1 w d????, 0 w oba (plus jumpy nad swoimi oraz unlimited dystans)

        if piece.color == GRAY:
            direction = -1  # forward is up
        if piece.color == WHITE:
            direction = 1  # forward is down
        if piece.king:
            direction = 0  # both
        if piece.color==GRAY:
            moves.update(self._traverse_left(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right,False))
            moves.update(self._traverse_right(direction, row, col, piece.color,
                        right_stop, step_right, right, left_stop, step_left, left,False))
            moves.update(self._traverse_up(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right,False))
            moves.update(self._traverse_down(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right,False))
        else:
            moves.update(self._traverse_left(direction, row, col, piece.color,
                        left_stop, step_left, left, right_stop, step_right, right,False))
            moves.update(self._traverse_right(direction, row, col, piece.color,
                        right_stop, step_right, right, left_stop, step_left, left,False))
            moves.update(self._traverse_down(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right,False))
            moves.update(self._traverse_up(direction, row, col, piece.color,
                     left_stop, step_left, left, right_stop, step_right, right,False))
                     

        return moves

    def _traverse_left(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right,hostile, skipped=[]):
        moves = {}
        last = []
        friendly= False
        enemy=hostile
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
                                 step_left, left-1, right_stop, step_right, right-1,enemy, skipped=skipped+last))
                    moves.update(self._traverse_up(direction, row, col-2, color, left_stop,
                                 step_left, left-1, right_stop, step_right, right-1,enemy, skipped=skipped+last))
                    moves.update(self._traverse_down(direction, row, col-2, color, left_stop,
                                 step_left, left-1, right_stop, step_right, right-1,enemy, skipped=skipped+last))
                    # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d????
                break

            elif current.color == color and not enemy:
                #break
                if left > 0:              
                    nextField = self.board[row][left-1]
                    if nextField ==0:
                        last = [current]
                        friendly = True
                    else:
                        break
                else:
                    break
                 #do skakania nad swoimi
            elif current.color != color:
                if left > 0:
                    nextField = self.board[row][left-1]
                    if nextField ==0:
                        enemy = True
                        last = [current]
                    
                    else:
                        break
                else:
                    break
            else:
                break
            left -= 1

        return moves

    def _traverse_right(self, direction, row, col, color, right_stop, step_right, right, left_stop, step_left, left,hostile, skipped=[]):
        moves = {}
        last = []
        friendly= False
        enemy =hostile
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
                                 step_right, right+1, left_stop, step_left, left+1,enemy,skipped=skipped+last))
                    moves.update(self._traverse_up(direction, row, col+2, color, left_stop,
                                 step_left, left+1, right_stop, step_right, right+1,enemy, skipped=skipped+last))
                    moves.update(self._traverse_down(direction, row, col+2, color, left_stop,
                                 step_left, left+1, right_stop, step_right, right+1,enemy, skipped=skipped+last))
                    # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d????
                break

            elif current.color == color and not enemy:
                #break     
                if right<7:
                    nextField = self.board[row][right+1]
                    if nextField ==0:
                        last = [current]
                        friendly = True
                    else:
                        break
                 #do skakania nad swoimi
            elif current.color != color:
                if right<7:
                    nextField = self.board[row][right+1]
                    if nextField ==0:
                        enemy=True
                        last = [current]   
                    else:
                        break
            else:
                break
            right += 1

        return moves

    def _traverse_up(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right,hostile, skipped=[]):
        moves = {}
        last = []
        up = row - 1
        down = row + 1
        stop = 0
        step = -1
        friendly= False
        enemy = hostile
        
        if direction == -1 or direction == 0:  # going forward SZARY

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
                                     step_right, right, left_stop, step_left, left,enemy, skipped=skipped+last))
                        moves.update(self._traverse_left(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right, enemy,skipped=skipped+last))
                        moves.update(self._traverse_up(direction, row-2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right,enemy, skipped=skipped+last))
                        # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d???? i boki

                    break
                elif current.color == color and not enemy:
                    #break
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                            friendly = True
                        else:
                            break #do skakania nad swoimi
                elif current.color != color:
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            enemy=True
                            last = [current]
                        else:
                            break
                else:
                    break
                up -= 1

            return moves

        #TODO naprawi?? by tylko m??g?? bi??
        elif direction == 1:  # going backward BIA??Y tylko bicie
            
            for r in range(row, stop, step):
                if up < 0:
                    break

                current = self.board[up][col]
                #moves[(up, col)] = last
                if current == 0 :
                    if enemy:
                        #enemy = False
                        
                        if last != [] and skipped != [] and not friendly:
                            
                            moves.update(self._traverse_down(direction, row-2, col, color, left_stop,
                                        step_left, left, right_stop, step_right, right,enemy ,skipped=skipped+last))
                            moves.update(self._traverse_right(direction, row-2, col, color, right_stop,
                                        step_right, right, left_stop, step_left, left,enemy, skipped=skipped+last))
                            moves.update(self._traverse_left(direction, row-2, col, color, left_stop,
                                        step_left, left, right_stop, step_right, right,enemy, skipped=skipped+last))
                    break   
                        # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d???? i boki    
                elif current.color != color:
                    if up>0:
                        nextField = self.board[up-1][col]
                        if nextField ==0:
                            last = [current]
                            enemy=True
                            moves[(up-1, col)] =skipped +last
                        else:
                            break
                else: break
                up -= 1
            
            return moves

    def _traverse_down(self, direction, row, col, color, left_stop, step_left, left, right_stop, step_right, right, hostile,skipped=[]):
        moves = {}
        last = []
        up = row - 1
        down = row + 1  # row + 1
        stop = 7
        step = 1
        friendly= False
        enemy = hostile
        
        if direction == 1 or direction == 0:  # going forward BIA??Y

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
                                     step_right, right, left_stop, step_left, left,enemy, skipped=skipped+last))
                        moves.update(self._traverse_left(direction, row+2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right,enemy, skipped=skipped+last))
                        moves.update(self._traverse_down(direction, row+2, col, color, left_stop,
                                     step_left, left, right_stop, step_right, right,enemy, skipped=skipped+last))
                        
                        # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d???? i boki

                    break
                elif current.color == color and not enemy:
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
                            enemy=True
                        else:
                            break
                else: break            
                down += 1

            return moves

        #TODO naprawi?? by tylko m??g?? bi??
        elif direction == -1:  # SZARY BACKWARDS
            
            for r in range(row, stop, step):
                if down > 7:
                    break

                current = self.board[down][col]
                if current == 0 :
                    if enemy:
                        #enemy = False
                        
                        if last != [] and skipped != [] and not friendly:
                            
                            moves.update(self._traverse_down(direction, row+2, col, color, left_stop,
                                        step_left, left, right_stop, step_right, right,enemy ,skipped=skipped+last))
                            moves.update(self._traverse_right(direction, row+2, col, color, right_stop,
                                        step_right, right, left_stop, step_left, left,enemy, skipped=skipped+last))
                            moves.update(self._traverse_left(direction, row+2, col, color, left_stop,
                                        step_left, left, right_stop, step_right, right,enemy, skipped=skipped+last))
                    break   
                        # tu wsadzi?? szukanie kolejnych ruch??w w g??r?? i d???? i boki    
                elif current.color != color:
                    if down<7:
                        nextField = self.board[down+1][col]
                        if nextField ==0:
                            last = [current]
                            enemy=True
                            moves[(down+1, col)] =skipped +last
                        else:
                            break
                else: break
                    

                down += 1

            return moves
