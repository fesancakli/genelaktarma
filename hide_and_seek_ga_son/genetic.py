import numpy as np
import random

class GeneticAlgorithm:
    def __init__(self, mutation_rate=0.1, elite_fraction=0.2):
        self.mutation_rate = mutation_rate
        self.elite_fraction = elite_fraction

    def select_parents(self, agents):
        fitnesses = np.array([a.fitness for a in agents], dtype=float)

        # 1️⃣ NaN, inf temizliği
        fitnesses = np.nan_to_num(fitnesses, nan=0.0, posinf=0.0, neginf=0.0)

        # 2️⃣ Eğer hepsi sıfır veya negatifse -> normalize etmeden eşit olasılık
        if np.all(fitnesses <= 0) or not np.isfinite(np.sum(fitnesses)) or np.sum(fitnesses) == 0:
            probabilities = np.ones_like(fitnesses) / len(fitnesses)
        else:
            # Negatifleri pozitif kaydır
            fitnesses -= np.min(fitnesses)
            total = np.sum(fitnesses)
            if total <= 0 or not np.isfinite(total):
                probabilities = np.ones_like(fitnesses) / len(fitnesses)
            else:
                probabilities = fitnesses / total

        # 3️⃣ Elitler
        elite_count = max(1, int(self.elite_fraction * len(agents)))
        elite_indices = np.argsort(fitnesses)[-elite_count:]
        elites = [agents[i] for i in elite_indices]

        # 4️⃣ Parent sayısını garanti et
        parent_count = max(2, len(agents) - elite_count)
        parents = random.choices(agents, weights=probabilities, k=parent_count)

        return elites, parents

    def crossover(self, w1, w2):
        point = random.randint(1, len(w1) - 1)
        return np.concatenate([w1[:point], w2[point:]])

    def mutate(self, weights):
        for i in range(len(weights)):
            if random.random() < self.mutation_rate:
                weights[i] += np.random.normal(0, 0.3)
        return np.clip(weights, -1, 1)

    def evolve(self, agents):
        elites, parents = self.select_parents(agents)
        new_weights = [e.weights.copy() for e in elites]

        while len(new_weights) < len(agents):
            p1, p2 = random.sample(parents, 2)
            child = self.crossover(p1.weights, p2.weights)
            child = self.mutate(child)
            new_weights.append(child)

        for agent, w in zip(agents, new_weights):
            agent.weights = w.copy()

    def population_stats(self, agents):
        fitnesses = np.array([a.fitness for a in agents], dtype=float)
        return np.max(fitnesses), np.mean(fitnesses)
