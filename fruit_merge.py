import pygame
import random
import sys
from enum import Enum
from collections import deque

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRID_COLS = 4
GRID_ROWS = 5
CELL_SIZE = WINDOW_WIDTH // GRID_COLS
PANEL_HEIGHT = WINDOW_HEIGHT - (GRID_ROWS * CELL_SIZE)

class FruitType(Enum):
    BLUEBERRY = 1
    JERUK = 2
    APEL = 3
    SEMANGKA = 4
    DURIAN = 5

FRUIT_COLORS = {
    FruitType.BLUEBERRY: (75, 0, 130),      # Indigo
    FruitType.JERUK: (255, 165, 0),         # Orange
    FruitType.APEL: (0, 128, 0),            # Green
    FruitType.SEMANGKA: (220, 20, 60),      # Red
    FruitType.DURIAN: (184, 134, 11),       # Dark goldenrod
}

FRUIT_NAMES = {
    FruitType.BLUEBERRY: "Blueberry",
    FruitType.JERUK: "Jeruk",
    FruitType.APEL: "Apel",
    FruitType.SEMANGKA: "Semangka",
    FruitType.DURIAN: "Durian",
}

class Fruit:
    def __init__(self, fruit_type, row, col):
        self.type = fruit_type
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE + CELL_SIZE // 2
        self.y = PANEL_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2
        self.radius = 15 + (fruit_type.value - 1) * 5  # Growing size
        self.is_falling = True
        self.fall_speed = 5

    def draw(self, screen):
        pygame.draw.circle(screen, FRUIT_COLORS[self.type], (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)

    def update(self):
        if self.is_falling:
            target_y = PANEL_HEIGHT + self.row * CELL_SIZE + CELL_SIZE // 2
            if self.y < target_y:
                self.y += self.fall_speed
                if self.y >= target_y:
                    self.y = target_y
                    self.is_falling = False
            else:
                self.is_falling = False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fruit Merge")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 40)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        self.grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.fruits = []
        self.score = 0
        self.game_over = False
        self.next_fruit_timer = 0
        
        # Spawn first fruit
        self.spawn_fruit()

    def spawn_fruit(self):
        """Spawn a random fruit at the top"""
        if self.game_over:
            return
        
        # Try to find empty spot in top row
        empty_cols = [col for col in range(GRID_COLS) if self.grid[0][col] is None]
        
        if not empty_cols:
            self.game_over = True
            return
        
        col = random.choice(empty_cols)
        # Randomly choose a fruit (mostly smaller fruits)
        fruit_type = random.choices(
            [FruitType.BLUEBERRY, FruitType.JERUK, FruitType.APEL, FruitType.SEMANGKA, FruitType.DURIAN],
            weights=[50, 30, 15, 4, 1],
            k=1
        )[0]
        
        fruit = Fruit(fruit_type, 0, col)
        self.grid[0][col] = fruit
        self.fruits.append(fruit)

    def handle_click(self, pos):
        """Handle mouse click to move/select fruit"""
        x, y = pos
        
        if y < PANEL_HEIGHT:
            return
        
        row = (y - PANEL_HEIGHT) // CELL_SIZE
        col = x // CELL_SIZE
        
        if row < 0 or row >= GRID_ROWS or col < 0 or col >= GRID_COLS:
            return
        
        if self.grid[row][col] is not None:
            fruit = self.grid[row][col]
            # Try to move fruit down
            self.try_move_fruit(fruit, row, col)

    def try_move_fruit(self, fruit, row, col):
        """Try to move fruit down or to adjacent cells"""
        # Try to move down
        for new_row in range(row + 1, GRID_ROWS):
            if self.grid[new_row][col] is None:
                self.grid[row][col] = None
                self.grid[new_row][col] = fruit
                fruit.row = new_row
                fruit.is_falling = False
                fruit.y = PANEL_HEIGHT + new_row * CELL_SIZE + CELL_SIZE // 2
                return True
        
        # If can't move down, try moving to adjacent columns at current row
        for new_col in [col - 1, col + 1]:
            if 0 <= new_col < GRID_COLS and self.grid[row][new_col] is None:
                self.grid[row][col] = None
                self.grid[row][new_col] = fruit
                fruit.col = new_col
                fruit.x = new_col * CELL_SIZE + CELL_SIZE // 2
                return True
        
        return False

    def check_merges(self):
        """Check for possible merges"""
        merged = True
        while merged:
            merged = False
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    if self.grid[row][col] is not None:
                        fruit = self.grid[row][col]
                        # Check adjacent cells for same fruit type
                        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < GRID_ROWS and 0 <= new_col < GRID_COLS:
                                adjacent = self.grid[new_row][new_col]
                                if adjacent and adjacent.type == fruit.type and fruit.type != FruitType.DURIAN:
                                    # Merge fruits
                                    self.merge_fruits(fruit, adjacent, row, col, new_row, new_col)
                                    merged = True
                                    break
                        if merged:
                            break
                if merged:
                    break

    def merge_fruits(self, fruit1, fruit2, row1, col1, row2, col2):
        """Merge two fruits into a larger one"""
        # Remove both fruits
        self.grid[row1][col1] = None
        self.grid[row2][col2] = None
        self.fruits.remove(fruit1)
        self.fruits.remove(fruit2)
        
        # Create new fruit at fruit1's position
        new_type = FruitType(fruit1.type.value + 1)
        new_fruit = Fruit(new_type, row1, col1)
        self.grid[row1][col1] = new_fruit
        self.fruits.append(new_fruit)
        
        # Update score
        self.score += new_type.value * 10

    def apply_gravity(self):
        """Make fruits fall down"""
        for row in range(GRID_ROWS - 2, -1, -1):
            for col in range(GRID_COLS):
                fruit = self.grid[row][col]
                if fruit is not None:
                    # Try to move down
                    for new_row in range(row + 1, GRID_ROWS):
                        if self.grid[new_row][col] is None:
                            self.grid[row][col] = None
                            self.grid[new_row][col] = fruit
                            fruit.row = new_row
                            fruit.is_falling = True
                            break
                        else:
                            break

    def check_game_over(self):
        """Check if game is over (top row full)"""
        for col in range(GRID_COLS):
            if self.grid[0][col] is None:
                return False
        return True

    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Update fruit positions
        for fruit in self.fruits:
            fruit.update()
        
        # Spawn new fruit every 60 frames
        self.next_fruit_timer += 1
        if self.next_fruit_timer >= 120:
            self.spawn_fruit()
            self.next_fruit_timer = 0
        
        # Apply gravity
        self.apply_gravity()
        
        # Check for merges
        self.check_merges()
        
        # Check game over
        if self.check_game_over():
            self.game_over = True

    def draw(self):
        """Draw game"""
        self.screen.fill((240, 240, 240))
        
        # Draw panel
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, WINDOW_WIDTH, PANEL_HEIGHT))
        
        # Draw title
        title = self.font_large.render("Fruit Merge", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, PANEL_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        # Draw score
        score_text = self.font_medium.render(f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, PANEL_HEIGHT * 2 // 3))
        self.screen.blit(score_text, score_rect)
        
        # Draw grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = col * CELL_SIZE
                y = PANEL_HEIGHT + row * CELL_SIZE
                pygame.draw.rect(self.screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        # Draw fruits
        for fruit in self.fruits:
            fruit.draw(self.screen)
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_large.render("GAME OVER!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, game_over_rect)
            
            score_final = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_final_rect = score_final.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(score_final, score_final_rect)
            
            restart_text = self.font_small.render("Press SPACE to restart or Q to quit", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

    def restart(self):
        """Restart the game"""
        self.grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.fruits = []
        self.score = 0
        self.game_over = False
        self.next_fruit_timer = 0
        self.spawn_fruit()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.restart()
            
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
