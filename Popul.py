# -*- coding: utf-8 -*-

from Indiv import Indiv
from random import random
from random import sample, shuffle
import pandas as pd
import math

class Popul: #é um conjunto de individups com tamanho fixado

    def __init__(self, popsize, indivsize, distances_matrix):
        self.popsize = popsize #tamanho da pop
        self.indivsize = indivsize #nr de cidades cada indiviudo tem
        self.distances = distances_matrix #matriz de distancias entre as cidades
        #self.initRandomPos(self.popsize) #Inicia uma instancia aleatoria da populacao
        self.initRandomPopWithRandomIndiv(self.popsize)

    def getIndiv(self, index):
        '''
        Retorna individuo da lista de populacoes
        '''
        return self.indivs[index]

    def get_indivsize(self):
        return self.indivsize

    def pop_sorted(self, population):
        '''
        Ordena uma lista de individuos
        Funcao coloca cada individuo num dicionario cujo fitness
        (distancia total) e a chave. As chaves sao ordenadas e retornadas
        numa lista de individuos
        '''
        fitness_sort = {}
        for i in range(0, self.popsize):
            if population[i].get_fitness() not in fitness_sort.keys():
                fitness_sort[float(population[i].get_fitness())] = [i]
            else:
                fitness_sort[population[i].get_fitness()].append(i)
        sorted_list = []
        for i in sorted(fitness_sort.keys()):
            for j in fitness_sort[i]:
                sorted_list.append(population[j])
        return sorted_list

    def initRandomPos(self, pop_size):
        '''
        Funcao inicia uma populacao aleatoria de individuos com
        tamanho pop_size
        '''
        combination = []
        indivs = []  # Lista de individuos da populacao
        existing_combinations = []  # Lista que guarda os pontos de partida de cada ind
        for i in range(pop_size):
            found = False
            while not found:
                combination = sample(range(self.indivsize), 2)  # primeiras 2 cidades
                if combination not in existing_combinations:
                    existing_combinations.append(combination)
                    found = True
            # Criacao de novo individuo
            indiv = Indiv(self.indivsize, self.distances, True, [combination[0], combination[1]])
            indivs.append(indiv)

        # Atribuicao de lista de individuos da populacao, ordenada do melhor para pior fitness
        self.indivs = self.pop_sorted(indivs)

    def initRandomPopWithRandomIndiv(self, pop_size):
        indivs = []
        for i in range(pop_size):
            indiv = Indiv(self.indivsize, self.distances, True, [], False, random=True)
            indivs.append(indiv)
        self.indivs = self.pop_sorted(indivs)

        #Atribuicao de lista de individuos ordenada da populacao
        self.indivs = self.pop_sorted(indivs)

    def set_population(self, population):
        '''
        Funcao que define a lista de individuos
        '''
        self.indivs = population

    # def generate_offspring(self, method, elitism = False):
    #     elif method.lower() == "crossover":
    #         offspring += self.pop_crossover(self.popsize)
    #     elif method.lower() == "mixed":
    #         nr_mutations = int(self.popsize*0.33)
    #         self.popsize -= nr_mutations
    #         offspring += self.pop_mutate(nr_mutations)
    #         offspring += self.pop_crossover(self.popsize)
    #     return self.pop_sorted(offspring)

    def pop_mutate(self, nr_offspring):
        '''
        Funcao que aplica mutacoes a cada individuo da populacao
        e retorna uma lista com os melhores individuos obtidos.
        O numero de individuos a retornar e dado por nr_offspring
        '''
        offspring = []
        for ind in self.indivs:
            offspring.append(ind.mutation())
        offspring = self.pop_sorted(offspring)
        return offspring[0:nr_offspring+1]

    def pop_crossover(self, nr_offspring):
        offspring = []
        population = self.pop_sorted(self.indivs)
        top_index = int(self.popsize/2)
        j = 0
        for i in range(top_index, self.popsize):
            offspring += population[i].crossover(population[j])
            if j < top_index-1:
                j += 1
            else:
                j = 0
        offspring = self.pop_sorted(offspring)
        return offspring[0:nr_offspring+1]

    def getFitnesses(self):
        '''
        Funcao que retorna uma lista com todos os fitnesses da populacao
        '''
        fitnesses = []
        for ind in self.indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses