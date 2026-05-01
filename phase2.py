from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import random

data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

print("Veri yüklendi:", X_train.shape)


"""depth=3 if sayısı soru sayısı yani (3 iris çiçek türü var)"""
"""estimatıors=10  10 tane karar ağacı yani 10 tane alt küme şeklinde yeniden değerlendirir"""
"""if-else in strict constraintlerine esneklik verir-kapsamlı değerlendirme"""
"""over-fitting i önleme"""
model = RandomForestClassifier(n_estimators=10, max_depth=3)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)

print("Model doğruluğu:", score)

def create_individuals():
    n_estimators=random.randint(10,200)
    max_depth=random.randint(1,20)
    individual=[n_estimators,max_depth]
    return individual
"""Her bir individual [n_estimators, max_depth]"""

print("Birey:",create_individuals())

population=[]
def create_population():
    for i in range(20):
        population.append(create_individuals())
    return population        
"""20li individual listesi random"""

print("20lik popülasyon listesi", create_population())

def fitness(individual):
    model = RandomForestClassifier(n_estimators=individual[0], max_depth=individual[1])
    """modeli kur"""
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    """doğruluk = score   fit = modeli eğit"""
    return score

print("O bireyin doğruluğunu ölç:", fitness((187,10)))

def select_best(population):
    best=[]
    for i in range(len(population)):
        best.append((population[i],fitness(population[i])))
        sortedList=sorted(best, key=lambda x:x[1], reverse=True)
    return sortedList[:10]


print("modele göre 20 bireyin doğruluğu:",select_best(population))  


def crossover(indv1,indv2):
    child=[indv1[0], indv2[1]]
    return child


print("2 individualin çocuğu:",crossover((5,10),(20,40)))  

def mutate(individual):
    index=random.randint(0,1)
    mutatedInd=[]
    if index == 0:
        individual[0]=random.randint(10,200)
    else:
        individual[1]=random.randint(1,20)
    return individual 

print("Mutate olmuş bir individual:",mutate([180,50]))

def genetic_algorithm():
    pop=create_population()
    best=select_best(pop)

    for i in range(10):
        indv1=random.choice(best)[0]
        indv2=random.choice(best)[0]
        child=crossover(indv1,indv2)
        child=mutate(child)
        pop.append(child)
        best=select_best(pop)

    return select_best(pop)[0]

print("En iyi bireyi döndür genetik algo:",genetic_algorithm())