import pygame
from config import *
from agent import Agent
from environment import Environment
from evaluator import Evaluator
from genetic import GeneticAlgorithm
from neural import NeuralNetwork
import numpy as np

import time
import pygame
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    NUM_GENERATIONS = 15
    POP_SIZE = 30  # her jenerasyonda 30 birey
    START_SEEKER_POS = (2 * TILE, 2 * TILE)
    START_HIDER_POS  = (15 * TILE, 8 * TILE)

    nn = NeuralNetwork()
    ga_seekers = GeneticAlgorithm(mutation_rate=0.1, elite_fraction=0.2)
    ga_hiders  = GeneticAlgorithm(mutation_rate=0.1, elite_fraction=0.2)
    evaluator  = Evaluator()

    # === Başlangıç popülasyonu ===
    seekers = [Agent("seeker", START_SEEKER_POS) for _ in range(POP_SIZE)]
    hiders  = [Agent("hider",  START_HIDER_POS)  for _ in range(POP_SIZE)]

    for s in seekers:
        s.weights = np.random.uniform(-1, 1, nn.num_weights)
    for h in hiders:
        h.weights = np.random.uniform(-1, 1, nn.num_weights)

    # === Ana döngü ===
    for gen in range(NUM_GENERATIONS):
        print(f"\n=== Nesil {gen+1}/{NUM_GENERATIONS} ===")
        gen_start = time.time()

        # Fitness sıfırla
        for a in seekers + hiders:
            a.fitness = 0.0

        # Her ajan kendi oyununu oynasın
        for i in range(POP_SIZE):
            # Seekers[i] vs Hiders[i] birebir maç gibi (istenirse random da yapılabilir)
            s = seekers[i]
            h = hiders[i]

            env = Environment([s], [h])


            evaluator.run_episode(env)

            # Pygame event kuyruğunu boşalt (donmayı önler)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return
            pygame.event.pump()

        # Fitness değerleri toplanmış durumda
        seeker_best, seeker_avg = ga_seekers.population_stats(seekers)
        hider_best,  hider_avg  = ga_hiders.population_stats(hiders)
        print(f"[SEEKERS]  En iyi: {seeker_best:.2f} | Ortalama: {seeker_avg:.2f}")
        print(f"[HIDERS]   En iyi: {hider_best:.2f} | Ortalama: {hider_avg:.2f}")

        # GA evrimi (yeni popülasyonlar döner)
        seekers = ga_seekers.evolve(seekers)
        hiders  = ga_hiders.evolve(hiders)

        # Süre hesapla
        gen_time = time.time() - gen_start
        print(f"Nesil {gen+1} tamamlandı — Süre: {gen_time:.2f} saniye")

        # İstersen her 5 nesilde görselleştir
        if gen % 5 == 0 or gen == NUM_GENERATIONS - 1:
            demo_env = Environment([seekers[0]], [hiders[0]])
            visualize(demo_env, screen, clock, evaluator)

    print("\n🎯 Eğitim tamamlandı!")


def visualize(env, screen, clock, evaluator):
    env.reset()
    running = True
    steps = 0

    while running and env.phase != "done":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        steps += 1
        env.update_phase()


        for seeker in env.seekers:
            if not seeker.alive:
                continue
            target = evaluator.closest_alive_hider(seeker, env.hiders)
            if not target:
                continue
            inputs = evaluator.build_inputs(seeker, target, env)
            direction = evaluator.nn.act(inputs, seeker.weights)
            seeker.move(direction, env)
            seeker.catch(target)

        for hider in env.hiders:
            if not hider.alive:
                continue
            nearest = evaluator.closest_alive_seeker(hider, env.seekers)
            if not nearest:
                continue
            inputs = evaluator.build_inputs(hider, nearest, env)
            direction = evaluator.nn.act(inputs, hider.weights)
            hider.move(direction, env)


        env.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
