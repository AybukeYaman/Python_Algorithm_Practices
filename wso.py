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