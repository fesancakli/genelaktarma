import numpy as np
from neural import NeuralNetwork
from environment import Environment
from config import *

class Evaluator:
    def __init__(self):
        self.nn = NeuralNetwork()

    def run_episode(self, env):
        env.reset()
        steps = 0

        while env.phase != "done":
            steps += 1
            phase = env.phase
            env.update_phase()


            if phase == "hiding":

                for hider in env.hiders:
                    if not hider.alive:
                        continue
                    nearest = self.closest_alive_seeker(hider, env.seekers)
                    if not nearest:
                        continue
                    inputs = self.build_inputs(hider, nearest, env)
                    direction = self.nn.act(inputs, hider.weights)
                    hider.move(direction, env)


            elif phase == "seeking":
                for seeker in env.seekers:
                    if not seeker.alive:
                        continue
                    target = self.closest_alive_hider(seeker, env.hiders)
                    if not target:
                        continue
                    inputs = self.build_inputs(seeker, target, env)
                    direction = self.nn.act(inputs, seeker.weights)
                    seeker.move(direction, env)
                    seeker.catch(target)

                for hider in env.hiders:
                    if not hider.alive:
                        continue
                    nearest = self.closest_alive_seeker(hider, env.seekers)
                    if not nearest:
                        continue
                    inputs = self.build_inputs(hider, nearest, env)
                    direction = self.nn.act(inputs, hider.weights)
                    hider.move(direction, env)


        for seeker in env.seekers:
            alive_hiders = sum(1 for h in env.hiders if h.alive)
            seeker.fitness = (
                    seeker.num_catches * 500
                    - seeker.number_of_collisions * 5
                    - alive_hiders * 50
            )

        for hider in env.hiders:
            alive_steps = steps if hider.alive else (steps / 2)
            caught = 0 if hider.alive else 1
            hider.fitness = (
                    alive_steps * 5
                    - hider.number_of_collisions * 2
                    - caught * 200
            )

    def build_inputs(self, agent, target, env):
        dx = (target.x - agent.x) / WIDTH
        dy = (target.y - agent.y) / HEIGHT
        dist = np.hypot(dx, dy)
        walls = [
            env.is_wall(agent.x, agent.y - TILE),
            env.is_wall(agent.x, agent.y + TILE),
            env.is_wall(agent.x - TILE, agent.y),
            env.is_wall(agent.x + TILE, agent.y),
        ]
        return np.array([[dx, dy, dist] + [int(w) for w in walls]])

    def closest_alive_hider(self, seeker, hiders):
        alive = [h for h in hiders if h.alive]
        if not alive:
            return None
        return min(alive, key=lambda h: seeker.distance_to(h))

    def closest_alive_seeker(self, hider, seekers):
        alive = [s for s in seekers if s.alive]
        if not alive:
            return None
        return min(alive, key=lambda s: hider.distance_to(s))
