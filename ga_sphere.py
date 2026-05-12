import numpy as np
import random

LB = -10
UB = 10
DIM = 3
POP_SIZE = 30
GENERATIONS = 100

def create_individual():
    return np.random.uniform(LB, UB, DIM).tolist()

def create_population():
    return [create_individual() for _ in range(POP_SIZE)]

def fitness(individual):
    return sum(x**2 for x in individual)

def select_best(population):
    scored = [(ind, fitness(ind)) for ind in population]
    return sorted(scored, key=lambda x: x[1])[:10]

def crossover(p1, p2):
    return [(p1[i] + p2[i]) / 2 for i in range(DIM)]

def mutate(individual):
    idx = random.randint(0, DIM-1)
    individual[idx] += random.uniform(-1, 1)
    individual[idx] = max(LB, min(UB, individual[idx]))
    return individual

def ga_sphere():
    population = create_population()
    
    for gen in range(GENERATIONS):
        best = select_best(population)
        children = []
        while len(children) < POP_SIZE - len(best):
            p1 = random.choice(best)[0]
            p2 = random.choice(best)[0]
            child = mutate(crossover(p1, p2))
            children.append(child)
        population = [b[0] for b in best] + children
    
    scored = [(ind, fitness(ind)) for ind in population]
    return sorted(scored, key=lambda x: x[1])[0]

print("GA Sonucu:", ga_sphere())