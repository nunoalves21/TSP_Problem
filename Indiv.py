# -*- coding: utf-8 -*-

from random import randint, random, shuffle
import math

class Indiv:        #path
    
    def __init__(self, indivsize, distances_matrix, pos = False, path = [], fitness = False):
        self.indivsize = indivsize
        self.distances = distances_matrix
        if pos:
            self.path = [pos[0], pos[1]]
            self.initIndiv()
        else:
            self.path = path
        if fitness:
            self.fitness = fitness
        else:
            self.fitness = self.calculate_path_distance()

    def get_path(self):
        return self.path

    def get_fitness(self):
        return self.fitness

    def append_city(self, city):
        self.path.append(city)

    def initIndiv(self):
        while len(self.path) != self.indivsize:
            pos = self.path[-1]
            min_dist = math.inf
            new_pos = 0
            for i in range(len(self.distances[pos])):
                if self.distances[pos][i] < min_dist and i not in self.path:
                    min_dist = self.distances[pos][i]
                    new_pos = i
            self.path.append(new_pos)

    def calculate_path_distance(self):    #fitness
        path_distance = 0
        for i in range(len(self.path)-1):
            path_distance += self.distances[self.path[i]][self.path[i+1]]
        path_distance += self.distances[self.path[-1]][self.path[0]]
        return path_distance

    def mutation(self):
        a, b = random.sample(range(0, self.indivsize), 2)











        best_distance = self.calculate_path_distance(self.path)
        final_path = self.path
        for i in range(iterations):
            a, b = random.sample(range(0, len(self.path) - 1), 2)
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
        return Indiv(self.indivsize, self.distances, False, final_path)

    
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





    
    def getGenes(self):
        return self.genes
    
    def initRandom(self, size):
        self.genes = []
        for i in range(size):
            self.genes.append(randint(0,1))


    def mutation(self):
        s = len(self.genes)
        pos = randint(0,s-1)      #escolhe uma posição qualquer
        if self.genes[pos] == 0: self.genes[pos] = 1     #faz a mutação
        else: self.genes[pos] = 0                       #faz a mutação
    
    def crossover(self, indiv2):
        return self.one_pt_crossover(indiv2)
    
    def one_pt_crossover(self, indiv2):   #self é um individuo o indiv2 será o outro
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0,s-1)        #escolhe posição de corte
        for i in range(pos):          #do zero à posição vai preenchendo
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        return Indiv(s, offsp1), Indiv(s, offsp2)