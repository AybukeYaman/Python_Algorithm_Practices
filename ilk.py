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


def random_route(cities):
    route=cities.copy()
    random.shuffle(route)
    return route

def hundred_shortest_route():
    newcities=[]   
    for i in range(100):
         random=random_route(cities)
         final=total_distance(random)
         newcities.append(final)
    return min(newcities) 
"""finalde sade tek ve en küçük olan rotayı döndürüyor """



population=[]
def create_population():
   for i in range(100):
       route=random_route(cities)
       dist=total_distance(route)
       population.append((route,dist))
   return population   
"""BU ILK KISMI burada da daha olabilecek rota arıyoruz 100 rotayı da görerek /daha zengin veri seti"""
    

def select_best(population):
  sortedList=[]
  sortedList=sorted(population, key=lambda x: x[1])     
  return sortedList[:20]
"""BU IKINCI KISMI ilk 20 elemanı al demek zaten küçükten büyüğe sıralanıyor"""


print("Mesafe", distance(cities[0], cities[1]))
print("Total Distance:", total_distance(cities))
print("Random Route:", random_route(cities))
print("En kısa rota mesafesi:", hundred_shortest_route())
print("En kısa 100 rota: ", create_population())
print("En iyi 20 rota: ", select_best(create_population()))