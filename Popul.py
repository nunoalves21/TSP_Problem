# -*- coding: utf-8 -*-

from Indiv import Indiv
from random import random
from random import sample
import pandas as pd
import math

class Popul: #é um conjunto de individups com tamanho fixado

    def __init__(self, popsize, indivsize, distances_matrix):
        self.popsize = popsize #tamanho da pop
        self.indivsize = indivsize #nr de cidades cada indiviudo tem
        self.distances = distances_matrix #matriz de distancias entre as cidades
        self.initRandomPop(self.popsize) #Inicia uma instancia aleatoria da populacao

    def getIndiv(self, index):
        '''
        Retorna individuo da lista de populacoes
        '''
        return self.indivs[index]

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

    def initRandomPop(self, pop_size):
        '''
        Funcao inicia uma populacao aleatoria de individuos com
        tamanho pop_size
        '''
        combination = []
        indivs = [] #Lista de individuos da populacao
        existing_combinations = [] #Lista que guarda os pontos de partida de cada ind
        for i in range(pop_size):
            found = False
            while not found:
                combination = sample(range(self.indivsize), 2) #primeiras 2 cidades
                if combination not in existing_combinations:
                    existing_combinations.append(combination)
                    found = True
            #Criacao de novo individuo
            indiv = Indiv(self.indivsize, self.distances, True, [combination[0], combination[1]])
            indivs.append(indiv)

        #Atribuicao de lista de individuos da populacao, ordenada do melhor para pior fitness
        self.indivs = self.pop_sorted(indivs)

    def initRandomPopWithRandomIndiv(self, pop_size):
        indivs=[]
        for i in range(pop_size):
            indiv = Indiv(self.indivsize, self.distances, True, [], False, random=True)
            indivs.append(indiv)
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
        pass

    def getFitnesses(self):
        '''
        Funcao que retorna uma lista com todos os fitnesses da populacao
        '''
        fitnesses = []
        for ind in self.indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses
        
    def bestFitness(self):     #dá a melhor solução
        return max(self.getFitnesses())

    def bestSolution(self):      #dá o indivíduo que tem a melhor solução (solução propriamente dita)
        fitnesses = self.getFitnesses()
        bestf = fitnesses[0]
        bestsol = 0
        for i in range(1,len(fitnesses)):
            if fitnesses[i] > bestf:
                bestf = fitnesses[i]
                bestsol = i
        return self.getIndiv(bestsol), bestf
    
    def selection(self, n):       #faz a seleção e chama a roleta
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses()))
        #fitnesses = list(self.getFitnesses())      #podemos usar esta ou a de cima
        for i in range(n):
            sel = self.roulette(fitnesses)      #faz a rouleta com a lista (para selecionar um conjunto de individuos)
            fitnesses[sel] = 0.0      #passa a zero para não ser escolhido novamente (confirmar como)
            res.append(sel)
        return res
    
    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1
    
    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res
    
    def recombination(self, parents, noffspring):    #seriação de novos individuos a partir das mutações e cross overs
        offspring = []
        new_inds = 0  #para avançar um indice sempre que vai buscar os pais
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]    #vai buscar os pais
            parent2 = self.indivs[parents[new_inds+1]]  #vai buscar os pais
            offsp1, offsp2 = parent1.crossover(parent2)    #dois descendentes com cross over
            offsp1.mutation()       #faz mutação
            offsp2.mutation()       #faz mutação
            offspring.append(offsp1)   #adiciona à lista final de individuos
            offspring.append(offsp2)    #adiciona à lista final de individuos
            new_inds += 2
        return offspring    #lista com os novos individuos
       
    def reinsertion(self, offspring):       #criar a nova população com os descendentes criados mais a seleção (diapositivo4)
        tokeep = self.selection(self.popsize-len(offspring))   #individuos to keep
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:    #verifica se é para manter
                self.indivs[i] = offspring[ind_offsp]   #se não for
                ind_offsp += 1