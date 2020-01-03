import numpy as np
import random
import time
import math
import tqdm


from Popul import Popul

class tsp:
    def __init__(self, namefile = '', pop_size = 20):
        self.cities = {} #dicionario com as coordenadas de cada cidade
        self.read_file(namefile)
        self.distances = self.calculate_distances() #Matriz de distancias
        self.indivsize = len(self.cities.keys()) #Nr de cidades
        self.population = Popul(pop_size, self.indivsize, self.distances) #Instancia de populacao

    def read_file(self, file):
        '''
        Funcao que le o ficheiro ".tsp" e guarda as coordenadas de cada cidade
        '''
        try:
            with open(file, "r") as file:
                store = False
                for line in file.readlines():
                    if line.startswith("EOF"):
                        store = False
                    if store:
                        city = line.split(" ")
                        self.cities[int(city[0])-1] = [float(city[1]), float(city[2])]
                    if line.startswith("NODE"):
                        store = True
        except:
            raise ValueError("Problem reading file")

    def calculate_distances(self):
        '''
        Funcao que calcula e retorna a matriz de distancia euclediana entre as cidades
        '''
        nr_cities = len(set(self.cities.keys()))
        distance_matrix = np.array(np.ones((nr_cities,nr_cities)) * np.inf)
        for i in range(0, nr_cities-1):
            for j in range(i+1, nr_cities):
                distance_matrix[i][j] = math.sqrt((self.cities[i][0]-self.cities[j][0])**2) + ((self.cities[i][1]-self.cities[j][1])**2)
                distance_matrix[j][i] = math.sqrt((self.cities[i][0] - self.cities[j][0]) ** 2) + ((self.cities[i][1] - self.cities[j][1]) ** 2)
        return distance_matrix


    def elitism(self):
        '''
        Funcao que guarda 25% dos melhores resultados para a proxima geracao e marca-os.
        Os individuos marcados, caso as funcoes evolucionarias nao produzam melhores resultados,
        estes individuos nao serao introduzidos em duplicado na proxima geracao.
        A funcao retorna um tuplo, cujo o primeiro elemento e uma lista com os melhores individuos
        e a segundo elemento o numero atualizado de inidividuos da proxima geracao.
        '''
        nr_elits = int((self.population.popsize) * 0.25)
        nr_offsprings = self.population.popsize - nr_elits
        offspring = self.population.indivs[0:nr_elits + 1]
        for ind in offspring:
            ind.set_elite(True) #Marcacao dos individuos
        return offspring, nr_offsprings



    def run(self, nr_iterations, method, elitism=False):
        '''
        Funcao que corre o algoritmo evolucionario, dado numero de interacoes
        e um determinado metodo.
        Os metodos podem ser:
        "mutation" realiza mutacoes aleatorias a cada elemento da populacao.
        "crossover" realiza
        "mixed" realiza os dois processos.
        Elitismo define se a funcao a cada iteracao guarda 25% dos melhores
        projenitores para a proxima descendencia.
        '''
        if method.lower() == "mutation":
            for i in tqdm.trange(0, nr_iterations):
                if elitism:
                    offspring, nr_offsprings = self.elitism()
                else:
                    offspring = []
                    nr_offsprings = self.population.popsize

                offspring += self.population.pop_mutate(nr_offsprings)
                self.population.set_population(offspring)


        best = self.population.pop_sorted(self.population.indivs)[0]
        print(best.get_fitness())
        print(best.get_path())








def test1():
    # start = time.time()
    #
    # qatar = cities("qa194.tsp", make_init_path=True)
    # #print(qatar.cities)
    # print(qatar.calculate_path_distance(qatar.init_path))
    # print(qatar.mutation2(qatar.init_path, 1_000_000))
    #
    # print("it took", time.time() - start, "seconds.")
    pass

def test2():
    qatar = tsp("qa194.tsp", 3)
    l=[]
    best_fit = 0
    best_path = 0
    for indiv in range(len(qatar.population.indivs)):
        if indiv == 0:
            l = [qatar.population.indivs[indiv]]
            best_fit = qatar.population.indivs[indiv].fitness
            best_path  = qatar.population.indivs[indiv].path
        for i in range(10_000):
            mutated_ind = l.pop().mutation()
            if mutated_ind.fitness < best_fit:
                best_fit = mutated_ind.fitness
                best_path = mutated_ind.get_path()
            print('iteration: ', i, '\t fitness:', mutated_ind.fitness)
            l.append(mutated_ind)
        print('Best Path found:', best_path)
        print('Best Fitness found:', best_fit)

def test3():
    qatar = tsp("qa194.tsp", 20)
    for j in range(0, 50):
        qatar.run(10_000, "mutation", False)

def test4():
    qatar = tsp("qa194.tsp", 20)
    best_fit = math.inf
    best_path = []
    for indiv in range(len(qatar.population.indivs)):





if __name__ == '__main__':
    #test1()
    #test2()
    test3()




