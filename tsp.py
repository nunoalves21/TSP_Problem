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
        lowest_distance = ((self.cities[0][0]-self.cities[1][0])**2 ) + ((self.cities[0][1]-self.cities[1][1])**2 )
        for i in range(0, nr_cities-1):
            for j in range(i+1, nr_cities):
                distance_matrix[i][j] = ((self.cities[i][0]-self.cities[j][0])**2) + ((self.cities[i][1]-self.cities[j][1])**2)
                distance_matrix[j][i] = ((self.cities[i][0] - self.cities[j][0]) ** 2) + ((self.cities[i][1] - self.cities[j][1]) ** 2)
                if distance_matrix[i][j] < lowest_distance:
                    lowest_distance = distance_matrix[i][j]
        return distance_matrix

    def mutation1(self, path, iterations = 1_000):
        best_distance = self.calculate_path_distance(path)
        final_path = path
        for i in range(iterations):
            a, b = random.sample(range(0,len(path)-1), 2)
            distance_remove = self.calc_distance_to_remove_add(final_path, a, b)
            new_distance = best_distance - distance_remove
            new_path = final_path.copy()
            new_path[b], new_path[a] = new_path[a], new_path[b]
            distance_add = self.calc_distance_to_remove_add(new_path, a, b)
            distance = new_distance + distance_add
            print(f'{distance:,}')
            if distance < best_distance:
                best_distance = distance
                final_path = new_path
        return final_path, f'{best_distance:,}'

    def mutation2(self, path, iterations = 1_000):
        best_distance = self.calculate_path_distance(path)
        final_path = path
        for i in range(iterations):
            a, b = random.sample(range(0, len(path)-1), 2)
            new_path = final_path.copy()
            new_path[b], new_path[a] = new_path[a], new_path[b]
            distance = self.calculate_path_distance(new_path)
            print(f'{distance:,}')
            if distance < best_distance:
                best_distance = distance
                final_path = new_path
        return final_path, f'{best_distance:,}'



def test1():
    # start = time.time()
    #
    # qatar = cities("qa194.tsp", make_init_path=True)
    # #print(qatar.cities)
    # print(qatar.calculate_path_distance(qatar.init_path))
    # print(qatar.mutation2(qatar.init_path, 1_000_000))
    #
    # print("it took", time.time() - start, "seconds.")

    #teste às populações
    qatar = cities("qa194.tsp")
    population = qatar.make_population(1)
    for path in population:
        print(qatar.calculate_path_distance(path))
    print(qatar.mutation2(population[0], 1_000_000))

def test2():
    qatar = cities("qa194.tsp")
    qatar.make_population(20)
    #print(qatar.population)
    print(qatar.offspring())


if __name__ == '__main__':
    #test1()
    test2




