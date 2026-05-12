import numpy as np
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

LB, UB, DIM = -10, 10, 3
POP_SIZE = 30
GENERATIONS = 50
rho = 0.5

def fitness(s):
    return sum(x**2 for x in s)

# GA
def run_ga_frames():
    frames = []
    population = [np.random.uniform(LB, UB, DIM).tolist() for _ in range(POP_SIZE)]
    for gen in range(GENERATIONS):
        frames.append([p[:] for p in population])
        scored = sorted([(ind, fitness(ind)) for ind in population], key=lambda x: x[1])
        best = [s[0] for s in scored[:10]]
        children = []
        while len(children) < POP_SIZE - 10:
            p1, p2 = random.choice(best), random.choice(best)
            child = [(p1[i]+p2[i])/2 for i in range(DIM)]
            idx = random.randint(0, DIM-1)
            child[idx] += random.uniform(-1, 1)
            children.append(child)
        population = best + children
    return frames

# WSO
def attack(soldier, king, commander, weight):
    rand = random.random()
    s, k, c = np.array(soldier), np.array(king[0]), np.array(commander[0])
    return (s + 2*rho*(c - k) + rand*(weight*k - s)).tolist()

def defence(soldier, king, commander, army, weight):
    rand = random.random()
    s, k, c = np.array(soldier), np.array(king[0]), np.array(commander[0])
    r = np.array(random.choice(army))
    return (s + 2*rho*(k - r) + rand*weight*(c - s)).tolist()

def run_wso_frames():
    frames = []
    army = [np.random.uniform(LB, UB, DIM).tolist() for _ in range(POP_SIZE)]
    for i in range(GENERATIONS):
        frames.append([a[:] for a in army])
        scored = sorted([(army[j], fitness(army[j])) for j in range(len(army))], key=lambda x: x[1])
        king, commander = scored[0], scored[1]
        for j in range(len(army)):
            soldier = army[j]
            new_pos = attack(soldier, king, commander, 2) if random.random() > 0.5 else defence(soldier, king, commander, army, 2)
            if fitness(new_pos) < fitness(soldier):
                army[j] = new_pos
        worst_idx = max(range(len(army)), key=lambda j: fitness(army[j]))
        army[worst_idx] = np.random.uniform(LB, UB, DIM).tolist()
    return frames

ga_frames = run_ga_frames()
wso_frames = run_wso_frames()

fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title('GA')
ax1.set_xlim(LB, UB)
ax1.set_ylim(LB, UB)
ax1.set_zlim(LB, UB)

ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title('WSO')
ax2.set_xlim(LB, UB)
ax2.set_ylim(LB, UB)
ax2.set_zlim(LB, UB)

ga_scatter = ax1.scatter([], [], [], c='blue', s=20)
wso_scatter = ax2.scatter([], [], [], c='red', s=20)

iteration_text = fig.suptitle('İterasyon: 0')

def update(frame):
    ga_pop = np.array(ga_frames[frame])
    wso_pop = np.array(wso_frames[frame])

    ga_scatter._offsets3d = (ga_pop[:,0], ga_pop[:,1], ga_pop[:,2])
    wso_scatter._offsets3d = (wso_pop[:,0], wso_pop[:,1], wso_pop[:,2])

    iteration_text.set_text(f'İterasyon: {frame+1}')
    return ga_scatter, wso_scatter

ani = animation.FuncAnimation(fig, update, frames=GENERATIONS, interval=500, blit=False)
plt.tight_layout()
plt.show()