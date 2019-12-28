import numpy as np
import random
import time
import math

class cities:
    def __init__(self, namefile = ''):
        self.cities = {}
        self.distances = None
        self.read_file(namefile)
        self.calculate_distances()

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
        self.distances = distance_matrix

    def calc_rank_population(self, population):
        import pandas as pd
        cols = [i for i in range(0, len(population[0]))]
        cols.append("Fitness")
        for indiv in population:
            indiv.append(self.calculate_path_distance(indiv))

        rank = pd.DataFrame(data=population, columns=cols)
        rank_sorted = rank.sort_values(by="Fitness", ascending=False)
        return rank_sorted

    def make_population(self, pop_size):
        population = []
        existing_combinations = []
        combination = []
        for i in range(pop_size):
            found = False
            while not found:
                combination = random.sample(range(len(self.cities)), 2)
                if combination not in existing_combinations:
                    existing_combinations.append(combination)
                    found = True
            path = [combination[0], combination[1]]
            while len(path) != len(self.cities):
                pos = path[-1]
                min_dist = math.inf
                new_pos = 0
                for i in range(len(self.distances[pos])):
                    if self.distances[pos][i] < min_dist and i not in path:
                        min_dist = self.distances[pos][i]
                        new_pos = i
                path.append(new_pos)
            path.append(path[0])
            population.append(path)

        population = self.calc_rank_population(population)

        self.population = population


    def top_paths(self, top=-1):
        if top == -1:
            top = int(len(self.population)*0.25)
        return self.population.iloc[0:top]

    def offspring(self, top=-1):
        offspring = []
        offspring_fitness = []
        top_offspring = self.top_paths(top)
        for i in range(0,len(top_offspring)):
            offspring.append(top_offspring.iloc[i].tolist()[:-1])
            offspring_fitness.append(top_offspring.iloc[i].tolist()[-1:])


        return offspring


    def calculate_path_distance(self, path):
        path_distance = 0
        for i in range(len(path)-1):
            path_distance += self.distances[path[i]][path[i+1]]
        path_distance += self.distances[path[-1]][path[0]]
        return path_distance


    def calc_distance_to_remove_add(self, path, city1, city2):
        if city1 == 0 and city2 == len(path)-1:
            distance = self.distances[path[city1]][path[city1 + 1]] + self.distances[path[city2]][path[city2 - 1]]
        elif city1 == len(path)-1 and city2 == 0:
            distance = self.distances[path[city1]][path[city1 - 1]] + self.distances[path[city2]][path[city2 + 1]]
        elif city1 == 0:
            distance = self.distances[path[city1]][path[city1 + 1]] + \
                       self.distances[path[city2]][path[city2 - 1]] + self.distances[path[city2]][path[city2 + 1]]
        elif city2 == 0:
            distance = self.distances[path[city1]][path[city1 - 1]] + self.distances[path[city1]][path[city1 + 1]] + \
                         self.distances[path[city2]][path[city2 + 1]]
        elif city1 == len(path)-1:
            distance = self.distances[path[city1]][path[city1 - 1]] + \
                        self.distances[path[city2]][path[city2 - 1]] + self.distances[path[city2]][path[city2 + 1]]
        elif city2 == len(path)-1:
            distance = self.distances[path[city1]][path[city1 - 1]] + self.distances[path[city1]][path[city1 + 1]] + \
                       self.distances[path[city2]][path[city2 - 1]]
        else:
            distance = self.distances[path[city1]][path[city1 - 1]] + self.distances[path[city1]][path[city1 + 1]] + \
                   self.distances[path[city2]][path[city2 - 1]] + self.distances[path[city2]][path[city2 + 1]]
        return distance

    def mutation(self, path, iterations = 1_000):
        best_distance = self.calculate_path_distance(path)
        final_path = path
        print(len(path))
        for i in range(iterations):
            a, b = random.sample(range(0, len(path) - 1), 2)
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




