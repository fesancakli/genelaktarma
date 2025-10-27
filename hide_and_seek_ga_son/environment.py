from config import *
import pygame
import numpy as np



class Environment:
    def __init__(self,seekers,hiders):
        self.seekers = seekers
        self.hiders = hiders
        self.agents = seekers + hiders
        self.phase = "hiding"
        self.steps = 0

    def is_wall(self, x, y):
        gx = int(x // TILE)
        gy = int(y // TILE)
        if gx < 0 or gy < 0 or gx >= WIDTH_TILES or gy >= HEIGHT_TILES:
            return True
        return MAP[gy][gx] == 1

    def update_phase(self):
        self.steps += 1
        if self.phase == "hiding" and self.steps >= HIDING_TIME:
            self.phase = "seeking"
        elif self.phase == "seeking" and self.steps >= TOTAL_TIME:
            self.phase = "done"

    def draw(self, screen):
        screen.fill(WHITE)

        for y in range(HEIGHT_TILES):
            for x in range(WIDTH_TILES):
                if MAP[y][x] == 1:
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        (x * TILE, y * TILE, TILE, TILE)
                    )

        for agent in self.agents:
            agent.draw(screen)

    def reset(self):
        self.steps = 0
        self.phase = "hiding"
        for agent in self.agents:
            agent.alive = True
            agent.num_catches = 0
            agent.number_of_collisions = 0
            agent.fitness = 0