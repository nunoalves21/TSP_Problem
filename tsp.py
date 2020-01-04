import numpy as np
import math
import tqdm
from Popul import Popul
import argparse

parser = argparse.ArgumentParser(prog="tsp.py",description="Travel Salesman problem with Evolutionary Algorithms")
parser.add_argument("-f", "--file",  action="store",help=".tsp file", default= "qa194.tsp")
parser.add_argument("-i", "--iter",  action="store",help="number of iterations", default= 10_000)
parser.add_argument("-p", "--pop_size",  action="store",help="Population size", default= 20)
parser.add_argument("-m", "--method",  action="store", choices=["mutation", "crossover", "mixed"], help="Method of evolutionary algorithm", default="mixed")
parser.add_argument("-e", "--elitistm", action="store", choices = [True, False], help="Run with elitism", default=False)
args = parser.parse_args()


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
        best_fitness = math.inf
        best_path = []
        for i in tqdm.trange(0, nr_iterations):
            if elitism:
                offspring, nr_offsprings = self.elitism()
            else:
                offspring = []
                nr_offsprings = self.population.popsize

            if method.lower() == "mutation":
                offspring += self.population.pop_mutate(nr_offsprings)
                self.population.set_population(offspring)

            elif method.lower() == "crossover":
                offspring += self.population.pop_crossover(nr_offsprings)
                self.population.set_population(offspring)

            elif method.lower() == "mixed":
                nr_mutations = int(self.population.get_indivsize()*0.33)
                nr_offsprings -= nr_mutations
                offspring += self.population.pop_mutate(nr_mutations)
                offspring += self.population.pop_crossover(nr_offsprings, True)
                self.population.set_population(offspring)
            top = self.population.pop_sorted(self.population.indivs)[0]
            if top.get_fitness() < best_fitness:
                best_fitness = top.get_fitness()
                best_path = top.get_path()
        print(best_fitness)
        print(best_path)

def run():
    qatar = tsp(args.file, args.pop_size)
    qatar.run(args.iter, args.method, args.elitistm)


if __name__ == '__main__':
    qatar = tsp("qa194.tsp", 194)
    qatar.run(3_000, "mutation", True)