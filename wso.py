import numpy as np
import random

# Problem boyutu
DIM = 3
# Asker sayısı
N_SOLDIERS = 30
# Arama uzayı sınırları
#LB-lowerbound   UB-upperbound
LB = -10
UB = 10

def create_soldier():
   position =np.random.uniform(LB,UB,DIM)
   #bu alt ve üst sınırlarda 3 sayı üret
   return position.tolist()

print("Asker Pozisyonu:", create_soldier())

def create_army():
   army=[]
   for i in range(30):
      soldier=create_soldier()
      army.append(soldier)
   return army  


print("Ordu:", create_army())

def fitness(soldier_Coordinates):
   x=soldier_Coordinates[0]
   y=soldier_Coordinates[1]
   z=soldier_Coordinates[2]
   return (x*x)+(y*y)+(z*z)

soldier= create_soldier()
print("Asker ne kadar uygun (fitness):", fitness(create_soldier()))


def select_best():
   best=[]
   army=create_army()
   for i in range(len(army)):
      fit=fitness(army[i])
      best.append((army[i],fit))
   return best

def select_leaders():
   best=select_best()
   listed=sorted( best, key=lambda x: x[1])     
   king=listed[0]
   commander=listed[1]
   leaders=[king,commander]
   return leaders

leaders = select_leaders()
print("King:", leaders[0])
print("Commander:", leaders[1])

rho = 0.5
def attack(soldier, king, commander, weight):
    rand = random.random()
    soldier = np.array(soldier)
    king = np.array(king[0])
    commander = np.array(commander[0])
    new_pos = soldier + 2*rho*(commander - king) + rand*(weight*king - soldier)
    return new_pos.tolist()

leaders = select_leaders()
army = create_army()
print("Attack sonrası:", attack(army[0], leaders[0], leaders[1], 2))

def defence(soldier,king,commander,army,weight):
    random_soldier = np.array(random.choice(army))
    rand = random.random()
    soldier = np.array(soldier)
    king = np.array(king[0])
    commander = np.array(commander[0])
    new_position= soldier+2*rho*(king-random_soldier)+ rand*weight*(commander-soldier)
    return new_position.tolist()

print("Defence sonrası:", defence(army[0], leaders[0], leaders[1], army, 2))

def relocate_weak(army):
    best = []
    for i in range(len(army)):
        best.append((army[i], fitness(army[i])))
    sortedList = sorted(best, key=lambda x: x[1])
    worst_idx = army.index(sortedList[-1][0])
    army[worst_idx] = np.random.uniform(LB, UB, DIM).tolist()
    return army

print("En Zayıf Askeri Yeniden Pozisyonla:",relocate_weak(army))

def wso():
    army = create_army()
    for i in range(100):
        best = [(army[j], fitness(army[j])) for j in range(len(army))]
        listed = sorted(best, key=lambda x: x[1])
        king = listed[0]
        commander = listed[1]
        
        for j in range(len(army)):
            soldier = army[j]
            rand = random.random()
            if rand > 0.5:
                new_pos = attack(soldier, king, commander, 2)
            else:
                new_pos = defence(soldier, king, commander, army, 2)
            
            if fitness(new_pos) < fitness(soldier):
                army[j] = new_pos
        relocate_weak(army)
    best = [(army[j], fitness(army[j])) for j in range(len(army))]
    return sorted(best, key=lambda x: x[1])[0]

print("WSO Sonucu:", wso())