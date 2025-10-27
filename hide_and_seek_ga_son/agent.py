import pygame
import math
import random
import numpy as np
from config import *


class Agent:
    def __init__(self , agent_type ,start_pos):
        self.agent_type = agent_type
        self.color = BLUE if agent_type == "seeker" else RED
        self.x, self.y = start_pos
        self.alive = True
        self.num_catches = 0
        self.fitness = 0
        self.number_of_collisions = 0
        self.weights = []

    def move(self , direciton ,env):
        dx,dy = direciton
        nx = self.x + dx * SPEED
        ny = self.y + dy * SPEED

        if not env.is_wall(nx, self.y):
            self.x = nx
        else:
            hit_wall = True
        if not env.is_wall(self.x, ny):
            self.y = ny
        else:
            hit_wall = True
        self.number_of_collisions += 1


    def catch(self, other):
        if self.agent_type == "seeker" and other.alive:
            if self.distance_to(other) < TILE * 0.5:
                other.alive = False
                self.num_catches += 1
                return True
        return False

    def distance_to(self, other):
        return math.hypot(other.x - self.x, other.y - self.y)

    # --- ÇİZİM ---
    def draw(self, screen):
        color = self.color if self.alive else (100, 100, 100)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 8)