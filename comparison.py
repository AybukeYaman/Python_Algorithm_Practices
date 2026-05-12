import numpy as np
import random
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

LB, UB, DIM = -10, 10, 3
POP_SIZE = 30
GENERATIONS = 50
RUNS = 30
rho = 0.5

def fitness(s):
    return sum(x**2 for x in s)

def run_ga():
    history = []
    population = [np.random.uniform(LB, UB, DIM).tolist() for _ in range(POP_SIZE)]
    for gen in range(GENERATIONS):
        scored = sorted([(ind, fitness(ind)) for ind in population], key=lambda x: x[1])
        history.append(scored[0][1])
        best = [s[0] for s in scored[:10]]
        children = []
        while len(children) < POP_SIZE - 10:
            p1, p2 = random.choice(best), random.choice(best)
            child = [(p1[i]+p2[i])/2 for i in range(DIM)]
            idx = random.randint(0, DIM-1)
            child[idx] += random.uniform(-1, 1)
            children.append(child)
        population = best + children
    return history

def attack(soldier, king, commander, weight):
    rand = random.random()
    s, k, c = np.array(soldier), np.array(king[0]), np.array(commander[0])
    return (s + 2*rho*(c - k) + rand*(weight*k - s)).tolist()

def defence(soldier, king, commander, army, weight):
    rand = random.random()
    s, k, c = np.array(soldier), np.array(king[0]), np.array(commander[0])
    r = np.array(random.choice(army))
    return (s + 2*rho*(k - r) + rand*weight*(c - s)).tolist()

def run_wso():
    history = []
    army = [np.random.uniform(LB, UB, DIM).tolist() for _ in range(POP_SIZE)]
    for i in range(GENERATIONS):
        scored = sorted([(army[j], fitness(army[j])) for j in range(len(army))], key=lambda x: x[1])
        king, commander = scored[0], scored[1]
        history.append(king[1])
        for j in range(len(army)):
            soldier = army[j]
            new_pos = attack(soldier, king, commander, 2) if random.random() > 0.5 else defence(soldier, king, commander, army, 2)
            if fitness(new_pos) < fitness(soldier):
                army[j] = new_pos
        worst_idx = max(range(len(army)), key=lambda j: fitness(army[j]))
        army[worst_idx] = np.random.uniform(LB, UB, DIM).tolist()
    return history

# 1. Convergence - tek run
ga_conv = run_ga()
wso_conv = run_wso()

# 2. Tutarlılık - 30 run
ga_finals = []
wso_finals = []
ga_times = []
wso_times = []

for _ in range(RUNS):
    t0 = time.time()
    h = run_ga()
    ga_times.append(time.time() - t0)
    ga_finals.append(h[-1])

    t0 = time.time()
    h = run_wso()
    wso_times.append(time.time() - t0)
    wso_finals.append(h[-1])

# Grafik
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('GA vs WSO - Karşılaştırma', fontsize=16)

# 1. Convergence
ax = axes[0, 0]
ax.plot(ga_conv, 'b-', label='GA')
ax.plot(wso_conv, 'r-', label='WSO')
ax.set_title('1. Convergence Hızı')
ax.set_xlabel('İterasyon')
ax.set_ylabel('En İyi Fitness')
ax.set_yscale('log')
ax.legend()

# 2. Final Fitness
ax = axes[0, 1]
ax.bar(['GA', 'WSO'], [np.mean(ga_finals), np.mean(wso_finals)], color=['blue', 'red'])
ax.set_title('2. Final Fitness (30 run ortalaması)')
ax.set_ylabel('Fitness Değeri')
ax.set_yscale('log')

# 3. Tutarlılık - Boxplot
ax = axes[1, 0]
ax.boxplot([ga_finals, wso_finals], labels=['GA', 'WSO'])
ax.set_title('3. Tutarlılık (30 run)')
ax.set_ylabel('Final Fitness')
ax.set_yscale('log')

# 4. Hesaplama Süresi
ax = axes[1, 1]
ax.bar(['GA', 'WSO'], [np.mean(ga_times), np.mean(wso_times)], color=['blue', 'red'])
ax.set_title('4. Hesaplama Süresi (ortalama)')
ax.set_ylabel('Saniye')

plt.tight_layout()
plt.show()