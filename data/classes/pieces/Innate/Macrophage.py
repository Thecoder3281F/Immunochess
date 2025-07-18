# Macrophage.py

import pygame

from data.classes.Piece import Piece

class Macrophage(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = 'assets/' + color[0] + '_macrophage.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 15, board.tile_height - 15))
        self.notation = 'M'  # Using 'M' for Macrophage

    def get_possible_moves(self, board):
        output = []
        moves = [
            (1, 2),    # Right 1, Down 2
            (2, 1),     # Right 2, Down 1
            (2, -1),    # Right 2, Up 1
            (1, -2),    # Right 1, Up 2
            (-1, -2),   # Left 1, Up 2
            (-2, -1),   # Left 2, Up 1
            (-2, 1),    # Left 2, Down 1
            (-1, 2)     # Left 1, Down 2
        ]
        
        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            
            # Check if the new position is on the board
            if 0 <= new_pos[0] < 12 and 0 <= new_pos[1] < 12:
                output.append(board.get_square_from_pos(new_pos))
                
        return output
        
    def get_moves(self, board):
        output = []
        for square in self.get_possible_moves(board):
            if square.occupying_piece is not None:
                if square.occupying_piece.color == self.color:
                    continue  # Skip if it's our own piece
                else:
                    output.append(square)  # Can capture opponent's piece
                    continue
            output.append(square)  # Empty square is valid
        return output
        
    def attacking_squares(self, board):
        return self.get_moves(board)