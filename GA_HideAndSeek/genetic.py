import random
from config import *

def selection(population):
    sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=True)
    selected = sorted_pop[:max(2, len(population)//2)]  # en az 2 eleman seç
    return selected


def crossover(p1, p2):
    point = random.randint(1, len(p1.genes) - 1)
    return p1.genes[:point] + p2.genes[point:]

def mutate(genes):
    for i in range(len(genes)):
        if random.random() < MUTATION_RATE:
            genes[i] += random.uniform(-0.1, 0.1)
            genes[i] = max(-1, min(1, genes[i]))  # sınır içinde tut
    return genes

