import random, math
from config import *

class Agent:
    def __init__(self, x, y, agent_type, genes=None):
        self.x = x
        self.y = y
        self.agent_type = agent_type
        self.angle = random.uniform(0, 360)
        self.fitness = 0
        self.alive = True
        self.color = (0, 255, 0) if agent_type == "hider" else (255, 0, 0)

        if genes is None:
            self.genes = [
                random.uniform(0.0, 1.0),   # move_speed
                random.uniform(-1.0, 1.0),  # turn_rate
                random.uniform(0.2, 1.0),   # view_angle
                random.uniform(0.0, 1.0),   # risk_tendency
                random.uniform(0.0, 1.0),   # aggressiveness
                random.uniform(0.0, 1.0)    # curiosity
            ]
        else:
            self.genes = genes

        self.speed = 2 + self.genes[0] * 3
        self.turn_rate = self.genes[1] * 10
        self.view_angle = 60 + self.genes[2] * 120

    def can_move(self, new_x, new_y, grid):
        gx = int(new_x // GRID_SIZE)
        gy = int(new_y // GRID_SIZE)
        if 0 <= gy < len(grid) and 0 <= gx < len(grid[0]):
            return grid[gy][gx] != "#"
        return False

    def move(self, grid):
        if not self.alive:
            return

        if random.random() < self.genes[5]:
            self.angle += random.uniform(-45, 45)

        if self.agent_type == "seeker":
            self.angle += self.turn_rate * self.genes[4]
        else:
            if random.random() < self.genes[3] * 0.5:
                self.angle += 180

        rad = math.radians(self.angle)
        nx = self.x + math.cos(rad) * self.speed
        ny = self.y + math.sin(rad) * self.speed

        if self.can_move(nx, ny, grid):
            self.x, self.y = nx, ny

        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self, screen):
        import pygame, math
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

        if self.agent_type == "seeker":
            radius = VISION_RADIUS
            half_angle = self.view_angle / 2
            left_angle = math.radians(self.angle - half_angle)
            right_angle = math.radians(self.angle + half_angle)
            x1 = self.x + math.cos(left_angle) * radius
            y1 = self.y + math.sin(left_angle) * radius
            x2 = self.x + math.cos(right_angle) * radius
            y2 = self.y + math.sin(right_angle) * radius

            fov_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(fov_surface, (255, 255, 0, 40),
                                [(self.x, self.y), (x1, y1), (x2, y2)])
            screen.blit(fov_surface, (0, 0))
