# /* Neutrophil.py

import pygame

from data.classes.Piece import Piece

class Neutrophil(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = 'assets/' + color[0] + '_neutrophil.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 15, board.tile_height - 15))
        self.notation = ' '

    def get_possible_moves(self, board):
        output = []
        moves = []
        # move forward
        if self.color == 'red':
            if not self.has_moved:
                moves.append((0, 1))
                moves.append((0, 2))
                moves.append((0, 3))
            else:
                moves.append((0, 1))
        elif self.color == 'blue':
            if not self.has_moved:
                moves.append((0, -1))
                moves.append((0, -2))
                moves.append((0, -3))
            else:
                moves.append((0, -1))
        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < 12 and new_pos[1] >= 0:
                output.append(
                    board.get_square_from_pos(new_pos)
                )
        return output

    def get_moves(self, board):
        output = []
        for square in self.get_possible_moves(board):
            if square.occupying_piece != None:
                break
            else:
                output.append(square)
        if self.color == 'red':
            # Diagonal captures: (x+1, y+1) and (x-1, y+1)
            if self.x + 1 < 12 and self.y + 1 < 12:
                square = board.get_square_from_pos(
                    (self.x + 1, self.y + 1)
                )
                if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                    output.append(square)
            if self.x - 1 >= 0 and self.y + 1 < 12:
                square = board.get_square_from_pos(
                    (self.x - 1, self.y + 1)
                )
                if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                    output.append(square)
        elif self.color == 'blue':
            # Diagonal captures: (x+1, y-1) and (x-1, y-1)
            if self.x + 1 < 12 and self.y - 1 >= 0:
                square = board.get_square_from_pos(
                    (self.x + 1, self.y - 1)
                )
                if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                    output.append(square)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = board.get_square_from_pos(
                    (self.x - 1, self.y - 1)
                )
                if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                    output.append(square)
        return output

    def attacking_squares(self, board):
        moves = self.get_moves(board)
        # return the diagonal moves 
        return [i for i in moves if i.x != self.x]