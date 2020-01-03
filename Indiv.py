# -*- coding: utf-8 -*-

from random import sample, shuffle
import math

class Indiv:        #path
    
    def __init__(self, indivsize, distances_matrix, pos = False, path = [], fitness = False, random = True):
        self.indivsize = indivsize #nr de cidades de cada caminho
        self.distances = distances_matrix #matriz de dinstancias
        if pos: #Cria caminho (path) a partir das distancias mais curtas de cidade em cidade
            # a partir das primeiras 2 cidades.
            self.path = path
            self.initIndiv()
        else: #Se nao o caminho e definido pela lista path
            self.path = path
        if random:
            self.initRandomIndiv()
        if fitness:# atribui valor de fitness nao sendo preciso calcular
            self.fitness = fitness
        else:
            self.fitness = self.calculate_path_distance()
        self.elite = False #marcacao do individuo caso este esteja
        # na lista de individuos com melhor fitness a passar para proxima geracao

    def get_path(self):
        '''
        retorna a lista de cidades do caminho
        '''
        return self.path

    def get_fitness(self):
        '''
        retorna a distancia final do caminho
        '''
        return self.fitness

    def set_elite(self, value):
        '''
        define a marcacao de elitismo
        '''
        self.elite = value

    def append_city(self, city):
        '''
        adiciona cidade ao caminho
        '''
        self.path.append(city)

    def initIndiv(self):
        '''
        Inicia um novo caminho, percorrendo a matriz de distancias.
        Este adiciona ao caminho a cidade mais proxima da anterior,
        sem repetir.
        '''
        while len(self.path) != self.indivsize:
            pos = self.path[-1]
            min_dist = math.inf
            new_pos = 0
            for i in range(len(self.distances[pos])):
                if self.distances[pos][i] < min_dist and i not in self.path:
                    min_dist = self.distances[pos][i]
                    new_pos = i
            self.path.append(new_pos)

    def initRandomIndiv(self):
        pos_0 = sample(range(self.indivsize), 1)
        existing_positions = [pos_0]
        self.path.append(pos_0)
        while len(self.path) != self.indivsize:
            found = False
            while not found:
                new_pos = sample(range(self.indivsize), 1)
                if new_pos not in existing_positions:
                    existing_positions.append(new_pos)
                    self.path.append(new_pos)
                    found = True

    def calculate_path_distance(self):
        '''
        Fncao calcula a distancia (fitness) do caminho
        '''
        path_distance = 0
        for i in range(len(self.path)-1):
            path_distance += self.distances[self.path[i]][self.path[i+1]]
        path_distance += self.distances[self.path[-1]][self.path[0]]
        return path_distance

    def get_random_pos(self):
        '''
        Funcao gera 2 pontos aleatorios no caminho
        '''
        a, b = 0, 0
        x = 1
        while x == 1 or x == -1:  # para os casos em que calha um a seguir ao outro (não faz sentido trocar)
            a, b = sorted(sample(range(0, self.indivsize), 2))
            x = a - b
        return a,b

    def mutation(self):
        '''
        Funcao gera mutacoes no caminho.
        Este testa 40 mutacoes para tentar obter um caminho melhor.
        Se encontrar uma solucao melhor que a anterior, retorna um novo individuo
        com o novo caminho.
        Se nao obter um caminho melhor o resultado depende da marcacao de elitismo.
        Se o individuo nao estiver marcado como elite, retorna um novo individuo com o mesmo
        caminho.
        Se este estiver marcado como elite, gera um novo individuo, cujo o inicio do caminho
        e dado pelos ultimos 2 cidades aleatorios testados na mutacao.
        '''
        count = 0
        while count < 40:
            count += 1
            a, b = self.get_random_pos()
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
        if self.elite:
            return Indiv(self.indivsize,self.distances, True, [a, b], False)
        else:
            return Indiv(self.indivsize, self.distances, False, self.path, False)

    def crossover(self, indiv2):
        a, b = self.get_random_pos()
        offsprings= [[-1 for i in range(0,self.indivsize+1)] for j in range(0,2)]
        parents = (self.path, indiv2.get_path())
        # Step 1
        offsprings[0][a:b+1] = parents[1][a:b]
        offsprings[1][a:b+1] = parents[0][a:b]

        # Step 2
        parents_check_0 = parents[0][0:a] + parents[0][b:]
        parents_check_1 = parents[1][0:a] + parents[1][b:]
        parents_fill_0 = parents[0][a:b]
        parents_fill_1 = parents[1][a:b]

        for i in range(0, self.indivsize):
            if i < a or i >= b:
                if parents[0][i] in parents_check_1:
                    offsprings[0][i] = parents[0][i]
                else:
                    parents_fill_1.append(parents[0][i])

                if parents[1][i] in parents_check_0:
                    offsprings[1][i] = parents[1][i]
                else:
                    parents_fill_0.append(parents[1][i])
        # Step 3
        i = 0
        while len(parents_fill_0) > 0 or len(parents_fill_1) > 0:
            if i ==len(offsprings):
                break
            if i < a or i >= b:
                #print(i)
                if parents[0][i] == -1:
                    if parents_fill_0[0] in offsprings[0]:
                        parents_fill_0.pop(0)
                    else:
                        offsprings[0][i] = parents_fill_0.pop(0)
                elif parents[1][i] == -1:
                    if parents_fill_1[0] in offsprings[1]:
                        parents_fill_1.pop(0)
                    else:
                        offsprings[1][i] = parents_fill_1.pop(0)
            i += 1
        offsprings[0] = Indiv(self.indivsize, self.distances, False, offsprings[0], False)
        offsprings[1] = Indiv(self.indivsize, self.distances, False, offsprings[1], False)
        return offsprings
