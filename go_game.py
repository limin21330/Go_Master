import pygame
import sys
from go_board import GoBoard

# Initialize pygame
pygame.init()

# Set up display
size = width, height = 800, 800
black = 0, 0, 0
white = 255, 255, 255
yellow = 255, 255, 0  # 新增黄色背景颜色

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Go Game')

# Set up the board
board_size = 19
board = GoBoard(board_size)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            board.handle_click(x, y)

    screen.fill(yellow)  # 将背景颜色填充为黄色
    board.draw(screen)
    pygame.display.flip()
