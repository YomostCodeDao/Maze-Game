import pygame
import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1] * width for _ in range(height)]
        self.start_x, self.start_y = 1, 1
        self.end_x, self.end_y = width - 2, height - 2
        self.generate_maze()
        self.grid[self.start_y][self.start_x] = 0
        self.grid[self.end_y][self.end_x] = 0
        self.path = []
        self.obstacles = set()
        self.create_obstacles()
        self.load_images()
        self.rewards = set()
        self.create_rewards()

    def load_images(self):
        cell_size = 20
        self.obstacle_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/iconbom.png"), (cell_size, cell_size))
        self.reward_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/phanthuong.jpg"), (cell_size, cell_size))
        self.end_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/dautay.jpg"), (cell_size, cell_size))
        self.wall_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/hangrao.jpg"), (cell_size, cell_size))

    def create_rewards(self):
        reward_count = 0
        while reward_count < 10:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.grid[y][x] == 0 and (x, y) not in self.rewards and not self.has_adjacent_reward(x, y):
                self.rewards.add((x, y))
                reward_count += 1

    def has_adjacent_reward(self, x, y):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (dx != 0 or dy != 0) and (x + dx, y + dy) in self.rewards:
                    return True
        return False
    
    def create_obstacles(self):
        obstacle_count = 0
        while obstacle_count < 20:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.grid[y][x] == 1 and (x, y) != (self.start_x, self.start_y) and (x, y) != (self.end_x, self.end_y) and self.is_far_from_obstacles(x, y):
                self.obstacles.add((x, y))
                obstacle_count += 1

    def is_far_from_obstacles(self, x, y):
        min_distance = 5
        for obstacle in self.obstacles:
            obstacle_x, obstacle_y = obstacle
            distance = abs(x - obstacle_x) + abs(y - obstacle_y)
            if distance < min_distance:
                return False
        return True

    def generate_maze(self):
        for x in range(self.width):
            self.grid[0][x] = 1
            self.grid[self.height - 1][x] = 1
        for y in range(self.height):
            self.grid[y][0] = 1
            self.grid[y][self.width - 1] = 1
        
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)] if 0 < x + dx < self.width - 1 and 0 < y + dy < self.height - 1]
            unvisited_neighbors = [neighbor for neighbor in neighbors if self.grid[neighbor[1]][neighbor[0]] == 1]
            if unvisited_neighbors:
                nx, ny = random.choice(unvisited_neighbors)
                self.grid[ny][nx] = 0
                self.grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

    def display_maze(self, screen, ai):
        cell_size = 20
        START_COLOR = (204, 229, 255)
        END_COLOR = (0, 255, 0)
        PLAYER_PATH_COLOR = (255, 0, 0)
        AI_PATH_COLOR = (204, 229, 255)
        OBSTACLE_COLOR = (0, 0, 0)
        REWARD_COLOR = (255, 215, 0)
        WALL_COLOR = (128, 128, 128)
        EMPTY_COLOR = (255, 255, 255)
        VISITED_COLOR = (204, 229, 255)

        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

                if (x, y) == (self.start_x, self.start_y):
                    pygame.draw.rect(screen, START_COLOR, rect)
                elif (x, y) == (self.end_x, self.end_y):
                    screen.blit(self.end_image, rect.topleft)
                elif (x, y) in self.path:
                    pygame.draw.rect(screen, PLAYER_PATH_COLOR, rect)
                elif (x, y) in ai.path:
                    pygame.draw.rect(screen, AI_PATH_COLOR, rect)
                elif (x, y) in self.obstacles:
                    screen.blit(self.obstacle_image, rect.topleft)
                elif (x, y) in self.rewards:
                    screen.blit(self.reward_image, rect.topleft)
                elif self.grid[y][x] == 1:
                    screen.blit(self.wall_image, rect.topleft)
                else:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect)

        path_color = VISITED_COLOR
        if ai.x == self.end_x and ai.y == self.end_y:
            for step in ai.path:
                x, y = step
                pygame.draw.rect(screen, path_color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
        else:
            for step in self.path:
                x, y = step
                pygame.draw.rect(screen, path_color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors
