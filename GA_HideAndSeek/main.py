import pygame, random, math
from agent import Agent
from genetic import selection, crossover, mutate
from config import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



WIDTH = len(MAP_GRID[0]) * GRID_SIZE
HEIGHT = len(MAP_GRID) * GRID_SIZE

def draw_map(surface):
    for y, row in enumerate(MAP_GRID):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(surface, (70, 70, 70), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def line_blocked(a, b):
    x1, y1 = int(a.x // GRID_SIZE), int(a.y // GRID_SIZE)
    x2, y2 = int(b.x // GRID_SIZE), int(b.y // GRID_SIZE)
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        if MAP_GRID[y1][x1] == "#":
            return True
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return False

def evaluate(hiders, seekers):
    for h in hiders:
        if not h.alive:
            continue
        h.fitness += 1
        min_distance = min(math.hypot(h.x - s.x, h.y - s.y) for s in seekers)
        h.fitness += 0.01 * min_distance
    for s in seekers:
        if not s.alive:
            continue
        for h in hiders:
            if not h.alive:
                continue
            dx = h.x - s.x
            dy = h.y - s.y
            distance = math.hypot(dx, dy)
            vision_radius = VISION_RADIUS * (0.8 + s.genes[4] * 0.4)
            vision_angle = s.view_angle
            if distance < vision_radius and not line_blocked(s, h):
                angle_to_hider = math.degrees(math.atan2(dy, dx))
                diff = (angle_to_hider - s.angle + 180) % 360 - 180
                if abs(diff) < vision_angle / 2:
                    h.alive = False
                    h.color = (100, 100, 100)
                    s.fitness += 10
                    h.fitness -= 10
                    break

def run_single_simulation(genes=None, draw_visual=False):
    seeker = Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), "seeker", genes)
    hiders = [Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), "hider") for _ in range(NUM_HIDERS)]
    seeker.fitness = 0
    time_counter = 0
    while time_counter < MAX_TIME and any(h.alive for h in hiders):
        clock.tick(FPS)
        time_counter += 1
        seeker.move(MAP_GRID)
        for h in hiders:
            h.move(MAP_GRID)
        evaluate(hiders, [seeker])
        if draw_visual:
            screen.fill((30, 30, 30))
            draw_map(screen)
            for a in hiders + [seeker]:
                a.draw(screen)
            remaining_time = (MAX_TIME - time_counter) // FPS
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Time: {remaining_time}", True, (255, 255, 255))
            screen.blit(text, (10, 10))
            pygame.display.flip()
    return seeker.fitness

def main():
    generation = 0
    running = True
    seekers = [Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), "seeker") for _ in range(POPULATION_SIZE)]
    while running and generation < GENERATIONS:
        print(f"Generation {generation + 1}")
        for i, seeker in enumerate(seekers):

            seeker.fitness = run_single_simulation(seeker.genes, True)
            print(f"Seeker {i+1}/{POPULATION_SIZE} fitness: {seeker.fitness:.2f}")
        best_seekers = selection(seekers)
        avg_fitness = sum(s.fitness for s in seekers) / len(seekers)
        print(f"Avg fitness: {avg_fitness:.2f} | Best: {best_seekers[0].fitness:.2f}")
        new_seekers = []
        for _ in range(POPULATION_SIZE):
            if len(best_seekers) >= 2:
                p1, p2 = random.sample(best_seekers, 2)
                genes = mutate(crossover(p1, p2))
            else:
                genes = mutate(best_seekers[0].genes.copy())
            new_seekers.append(Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), "seeker", genes))
        seekers = new_seekers
        generation += 1
    pygame.quit()

if __name__ == "__main__":
    main()
