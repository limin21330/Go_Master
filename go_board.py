import pygame
import time

class GoBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.cell_size = 40
        self.margin = 20
        self.current_player = 'black'

    def draw(self, screen):
        board_color = (222, 184, 135)  # 棋盘颜色
        screen.fill(board_color)
        
        # 绘制棋盘线条
        for i in range(self.size):
            start_pos = (self.margin + i * self.cell_size, self.margin)
            end_pos = (self.margin + i * self.cell_size, self.margin + (self.size - 1) * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)
            start_pos = (self.margin, self.margin + i * self.cell_size)
            end_pos = (self.margin + (self.size - 1) * self.cell_size, self.margin + i * self.cell_size)
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)
        
        # 绘制星位
        star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for r, c in star_points:
            x = self.margin + c * self.cell_size
            y = self.margin + r * self.cell_size
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 5)
        
        # 绘制棋子
        for row in range(self.size):
            for col in range(self.size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                if self.board[row][col] is not None:
                    color = (0, 0, 0) if self.board[row][col] == 'black' else (255, 255, 255)
                    pygame.draw.circle(screen, color, (x, y), self.cell_size // 2 - 2)

    def handle_click(self, x, y):
        row = (y - self.margin) // self.cell_size
        col = (x - self.margin) // self.cell_size
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] is None:
            if self.confirm_placement(row, col):
                self.animate_stone_placement(row, col)
                self.board[row][col] = self.current_player
                self.remove_captured_stones(row, col)
                self.current_player = 'white' if self.current_player == 'black' else 'black'

    def confirm_placement(self, row, col):
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 36)
        text = font.render("Confirm placement? (Y/N)", True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False

    def animate_stone_placement(self, row, col):
        screen = pygame.display.get_surface()
        color = (0, 0, 0) if self.current_player == 'black' else (255, 255, 255)
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        for radius in range(1, self.cell_size // 2 - 1, 2):
            screen.fill((222, 184, 135))
            self.draw(screen)
            pygame.draw.circle(screen, color, (x, y), radius)
            pygame.display.flip()
            time.sleep(0.01)

    def remove_captured_stones(self, row, col):
        opponent = 'white' if self.current_player == 'black' else 'black'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == opponent:
                if not self.has_liberty(r, c, opponent):
                    self.capture_group(r, c, opponent)

    def has_liberty(self, row, col, color):
        visited = set()
        return self._has_liberty(row, col, color, visited)

    def _has_liberty(self, row, col, color, visited):
        if (row, col) in visited:
            return False
        visited.add((row, col))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] is None:
                    return True
                if self.board[r][c] == color and self._has_liberty(r, c, color, visited):
                    return True
        return False

    def capture_group(self, row, col, color):
        to_capture = [(row, col)]
        captured = set()
        while to_capture:
            r, c = to_capture.pop()
            if (r, c) not in captured:
                captured.add((r, c))
                self.board[r][c] = None
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == color:
                        to_capture.append((nr, nc))
