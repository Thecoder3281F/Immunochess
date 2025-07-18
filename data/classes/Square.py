import pygame
import sys
from utils.colours import BOARD_LIGHT, BOARD_DARK, HIGHLIGHT

class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = "light" if (x + y) % 2 == 0 else "dark"
        self.draw_color = BOARD_LIGHT if self.color == "light" else BOARD_DARK
        self.highlight_color = HIGHLIGHT
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )

        self.font = pygame.font.SysFont("Arial", 20)
        

    def get_coord(self):
        columns = "abcdefghijkl"
        return (columns[self.x], str(self.y + 1))
    
    def draw(self, display, offset=(0, 0)):
        # Create a new rect with the offset applied
        offset_rect = pygame.Rect(
            self.abs_x + offset[0],
            self.abs_y + offset[1],
            self.width,
            self.height
        )
        
        # Draw the square
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, offset_rect)
        else:
            pygame.draw.rect(display, self.draw_color, offset_rect)
            
        # Draw the piece if there is one
        if self.occupying_piece:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = offset_rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
