import random
import math

# 10 şehir oluşturduk
cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]

#random seçilen 2 şehir için distance verir
def distance(city1,city2):
    dist = math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2 )  
    return dist


#route bir şehirler listesi
#sırayla şehiler arası mesafe toplam
def total_distance(route):
    toplam=0
    for i in range(len(route)-1):
        toplam+= distance(route[i], route[i+1])
    return toplam

print("Mesafe", distance(cities[0], cities[1]))
print("Total Distance:", total_distance(cities))