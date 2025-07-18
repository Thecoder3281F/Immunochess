import pygame
import pygame.freetype  # For better text rendering

from data.classes.Board import Board
from utils.colours import WHITE, BLACK, LIGHT_GRAY, BLUE, RED

# Initialize pygame and font
pygame.init()
pygame.freetype.init()

# Constants
WINDOW_SIZE = (1200, 1000)
BOARD_SIZE = 800
SIDEBAR_WIDTH = 200

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('ImmunoChess')

# Load fonts
try:
    font = pygame.freetype.SysFont('Arial', 20)
    title_font = pygame.freetype.SysFont('Arial', 24, bold=True)
except:
    # Fallback if system font fails
    font = pygame.freetype.Font(None, 24)
    title_font = pygame.freetype.Font(None, 32)

# Initialize the board with the fixed size
board = Board(BOARD_SIZE, BOARD_SIZE)

def draw_turn_indicator(display, current_turn):
    """Draw the turn indicator in the right sidebar"""
    turn_text = "Red's Turn" if current_turn == 'red' else "Blue's Turn"
    text_color = BLACK
    bg_color = LIGHT_GRAY
    player_color = RED if current_turn == 'red' else BLUE
    
    # Draw sidebar background
    pygame.draw.rect(display, bg_color, (BOARD_SIZE + SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_SIZE[1]))
    
    # Draw turn indicator background
    indicator_rect = pygame.Rect(BOARD_SIZE + SIDEBAR_WIDTH + 20, 50, SIDEBAR_WIDTH - 40, 60)
    pygame.draw.rect(display, player_color, indicator_rect, border_radius=10)
    pygame.draw.rect(display, text_color, indicator_rect, 2, border_radius=10)
    
    # Draw turn text
    text_surface, text_rect = font.render(turn_text, text_color)
    text_x = indicator_rect.centerx - text_rect.width // 2
    text_y = indicator_rect.centery - text_rect.height // 2
    display.blit(text_surface, (text_x, text_y))

def draw(display, current_turn):
    """Draw the game state"""
    # Fill background
    display.fill(LIGHT_GRAY)
    
    # Draw left sidebar (for future use)
    pygame.draw.rect(display, LIGHT_GRAY, (0, 0, SIDEBAR_WIDTH, WINDOW_SIZE[1]))
    
    # Draw the board (centered with sidebars)
    board_rect = pygame.Rect(SIDEBAR_WIDTH, 50, BOARD_SIZE, BOARD_SIZE)
    display.blit(pygame.Surface((BOARD_SIZE, BOARD_SIZE)), (SIDEBAR_WIDTH, 50))
    board.draw(display, board_rect.topleft)
    
    # Draw turn indicator
    draw_turn_indicator(display, current_turn)
    
    # Draw game title in the left sidebar
    title_surface, title_rect = title_font.render('ImmunoChess', BLACK)
    display.blit(title_surface, (SIDEBAR_WIDTH // 2 - title_rect.width // 2, 30))
    
    pygame.display.update()


# def get_board_position(screen_pos):
#     """Convert screen position to board position"""
#     x, y = screen_pos
#     board_x = x - SIDEBAR_WIDTH
#     board_y = y - 50  # 50px top margin
    
#     # Check if the click is within the board
#     if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
#         return (board_x, board_y)
#     return None

if __name__ == '__main__':
    running = True
    current_turn = 'red'  # Start with red's turn
    
    while running:
        mx, my = pygame.mouse.get_pos()
        print(str(mx) + " " + str(my))

        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:  # Left mouse button
                    # Handle the click (selection and movement)
                    move_made = board.handle_click(mx, my)
                    if move_made:
                        current_turn = 'blue' if current_turn == 'red' else 'red'
        
        # Draw the game
        draw(screen, current_turn)
    
    pygame.quit()
    pygame.freetype.quit()


## TODO
"""
- other pieces' movements
- - Macrophage
- - Natural Killer
- undo move
- Add captured pieces display
- Add game status (check/checkmate)
"""