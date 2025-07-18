import pygame
from data.classes.Square import Square
from data.classes.pieces.Adaptive import *
from data.classes.pieces.Innate.Neutrophil import Neutrophil
from data.classes.pieces.Innate.Macrophage import Macrophage
from data.classes.pieces.Promotion import *

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 12
        self.tile_height = height // 12
        self.selected_piece = None
        self.turn = 'red'
        self.config = [
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "rm", "", "", "", "", "", "", "rm", "", ""],
            ["rn", "rn", "rn", "rn", "rn", "rn", "rn", "rn", "rn", "rn", "rn", "rn"],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            ["bn", "bn", "bn", "bn", "bn", "bn", "bn", "bn", "bn", "bn", "bn", "bn"],
            ["", "", "bm", "", "", "", "", "", "", "bm", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", ""],
            
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(12):
            for x in range(12):
                output.append(
                    Square(x,  y, self.tile_width, self.tile_height)
                )
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    # looking inside contents, what piece does it have
                    if piece[1] == 'n':
                        square.occupying_piece = Neutrophil(
                            (x, y), 'red' if piece[0] == 'r' else 'blue', self
                        )
                    elif piece[1] == 'm':
                        square.occupying_piece = Macrophage(
                            (x, y), 'red' if piece[0] == 'r' else 'blue', self
                        )
                    # elif piece[1] == 'N':
                    #     square.occupying_piece = Knight(
                    #         (x, y), 'white' if piece[0] == 'w' else 'black', self
                    #     )
                    # elif piece[1] == 'B':
                    #     square.occupying_piece = Bishop(
                    #         (x, y), 'white' if piece[0] == 'w' else 'black', self
                    #     )
                    # elif piece[1] == 'Q':
                    #     square.occupying_piece = Queen(
                    #         (x, y), 'white' if piece[0] == 'w' else 'black', self
                    #     )
                    # elif piece[1] == 'K':
                    #     square.occupying_piece = King(
                    #         (x, y), 'white' if piece[0] == 'w' else 'black', self
                    #     )
                    # elif piece[1] == 'P':
                    #     square.occupying_piece = Pawn(
                    #         (x, y), 'white' if piece[0] == 'w' else 'black', self
                    #     )

    def handle_click(self, mx, my):
        """Handle mouse clicks on the board
        
        Args:
            mx, my: Mouse position in screen coordinates
            
        Returns:
            bool: True if a move was made, False otherwise
        """
        # Convert screen coordinates to board coordinates (0-11)
        board_x = (mx - 200) // (self.width // 12)
        board_y = (my - 50) // (self.height // 12)  # 50px top margin
        
        # Check if click is outside the board
        if not (200 <= mx < 1000 and 
                50 <= my < 850):
            # Click outside the board, unselect any selected piece
            if self.selected_piece is not None:
                self.selected_piece = None
                return False
            return False
        
        # Ensure board coordinates are within valid range
        if not (0 <= board_x < 12 and 0 <= board_y < 12):
            return False
            
        clicked_square = self.get_square_from_pos((board_x, board_y))
        
        # If we have a selected piece, try to move it
        if self.selected_piece:
            # Try to make a move
            if self.selected_piece.move(self, clicked_square):
                # Move was successful
                self.selected_piece = None
                self.turn = 'blue' if self.turn == 'red' else 'red'
                return True
            
            # If click is on another piece of the same color, select it instead
            if (clicked_square.occupying_piece and 
                clicked_square.occupying_piece.color == self.turn and
                clicked_square.occupying_piece != self.selected_piece):
                self.selected_piece = clicked_square.occupying_piece
            # If click is on an empty square or opponent's piece, keep the current selection
            
            return False
        
        # If no piece is selected, try to select one
        if clicked_square.occupying_piece and clicked_square.occupying_piece.color == self.turn:
            self.selected_piece = clicked_square.occupying_piece
            
        return False
    
    def draw(self, display, offset=(0, 0)):
        """Draw the board and pieces with an optional offset"""
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display, offset)