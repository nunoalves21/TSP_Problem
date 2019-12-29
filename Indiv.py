# -*- coding: utf-8 -*-

from random import sample, random, shuffle
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

    def get_random_pos(self):
        a, b = 0, 0
        x = 1
        while x == 1 or x == -1:  # para os casos em que calha um a seguir ao outro (não faz sentido trocar)
            a, b = sorted(sample(range(0, self.indivsize), 2))
            x = a - b
        return a,b


    def mutation(self):
        count = 0
        while True:
            count += 1
            a,b = self.get_random_pos()
            new_path = self.path.copy()
            new_path.insert(0, self.path[-1])
            new_path.append(self.path[0])

            if a == 0 and b == self.indivsize-1:
                distance = self.fitness.copy()
                city1_a = self.path[a + 1]
                city1_b = new_path[b - 1]
                city_a, city_b = self.path[a], self.path[b]
                distance -= (self.distances[city1_a][city_a] + self.distances[city1_b][city_b])
                distance += (self.distances[city1_b][city_a] + self.distances[city1_a][city_b])

                new_path = self.path.copy()
                new_path[a] = city_b
                new_path[b] = city_a

            else:
                city1_a, city2_a = new_path[a], new_path[a+2]
                city1_b, city2_b = new_path[b], new_path[b + 2]
                city_a, city_b = new_path[a + 1], new_path[b + 1]

                distance = self.fitness.copy()

                distance -= (self.distances[city1_a][city_a] + self.distances[city_a][city2_a])
                distance -= (self.distances[city1_b][city_b] + self.distances[city_b][city2_b])

                distance += (self.distances[city1_b][city_a] + self.distances[city_a][city2_b])
                distance += (self.distances[city1_a][city_b] + self.distances[city_b][city2_a])

                new_path = self.path.copy()
                new_path[a] = city_b
                new_path[b] = city_a
            if distance < self.fitness:
                return Indiv(self.indivsize, self.distances, False, new_path, distance)
            elif count == 40:
                return Indiv(self.indivsize, self.distances, False, self.path, False)




    # def getGenes(self):
    #     return self.genes
    #
    # def initRandom(self, size):
    #     self.genes = []
    #     for i in range(size):
    #         self.genes.append(randint(0,1))
    #
    #
    # def mutation(self):
    #     s = len(self.genes)
    #     pos = randint(0,s-1)      #escolhe uma posição qualquer
    #     if self.genes[pos] == 0: self.genes[pos] = 1     #faz a mutação
    #     else: self.genes[pos] = 0                       #faz a mutação
    #
    # def crossover(self, indiv2):
    #     return self.one_pt_crossover(indiv2)
    #
    # def one_pt_crossover(self, indiv2):   #self é um individuo o indiv2 será o outro
    #     offsp1 = []
    #     offsp2 = []
    #     s = len(self.genes)
    #     pos = randint(0,s-1)        #escolhe posição de corte
    #     for i in range(pos):          #do zero à posição vai preenchendo
    #         offsp1.append(self.genes[i])
    #         offsp2.append(indiv2.genes[i])
    #     for i in range(pos, s):
    #         offsp2.append(self.genes[i])
    #         offsp1.append(indiv2.genes[i])
    #     return Indiv(s, offsp1), Indiv(s, offsp2)