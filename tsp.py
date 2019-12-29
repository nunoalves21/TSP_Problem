import numpy as np
import random
import time
import math


from Popul import Popul

class tsp:
    def __init__(self, namefile = '', pop_size = 20):
        self.cities = {}
        self.read_file(namefile)
        self.distances = self.calculate_distances()
        self.indivsize = len(self.cities.keys())
        self.population = Popul(pop_size, self.indivsize, self.distances)

    def read_file(self, file):
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
        nr_cities = len(set(self.cities.keys()))
        distance_matrix = np.array(np.ones((nr_cities,nr_cities)) * np.inf)
        for i in range(0, nr_cities-1):
            for j in range(i+1, nr_cities):
                distance_matrix[i][j] = math.sqrt((self.cities[i][0]-self.cities[j][0])**2) + ((self.cities[i][1]-self.cities[j][1])**2)
                distance_matrix[j][i] = math.sqrt((self.cities[i][0] - self.cities[j][0]) ** 2) + ((self.cities[i][1] - self.cities[j][1]) ** 2)
        return distance_matrix


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
    qatar = tsp("qa194.tsp", 1)
    for indiv in qatar.population.indivs:
        #print(indiv.fitness)
        l = [indiv]
        best_fit = indiv.fitness
        for i in range(20_000):
            mutated_ind = l.pop().mutation()
            if mutated_ind.fitness < best_fit:
                best_fit = mutated_ind.fitness
                best_path = mutated_ind.get_path()
            print('iteration: ', i, '\t fitness:', mutated_ind.fitness)
            l.append(mutated_ind)
        print('Best Path found:', best_path)
        print('Best Fitness found:', best_fit)


if __name__ == '__main__':
    #test1()
    test2()




