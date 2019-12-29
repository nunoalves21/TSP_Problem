# -*- coding: utf-8 -*-

from Indiv import Indiv
from random import random
from random import sample
import pandas as pd
import math

class Popul:     #é um conjunto de individups com tamanho fixado

    def __init__(self, popsize, indivsize, distances_matrix):
        self.popsize = popsize         #tamanho da pop
        self.indivsize = indivsize
        self.distances = distances_matrix
        self.initRandomPop(self.popsize)    

    def pop_sorted(self, population):
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
        population = []
        existing_combinations = []
        combination = []
        for i in range(pop_size):
            found = False
            while not found:
                combination = sample(range(self.indivsize-1), 2)
                if combination not in existing_combinations:
                    existing_combinations.append(combination)
                    found = True
            ind = Indiv(self.indivsize, self.distances, combination)
            population.append(ind)

        self.population = self.pop_sorted(population)

    def generate_offspring(self, method, elitism = False, nr_offspring=self.popsize):
        if elitism:
            nr_elits = int((nr_offspring)*0.25)
            nr_offspring -= nr_elits
            offspring = self.population[0:nr_elits+1]
        else:
            offspring = []
        if method.lower() == "mutation":
            offspring += self.pop_mutate(nr_offspring)
        elif method.lower() == "crossover":
            offspring += self.pop_crossover(nr_offspring)
        elif method.lower() == "mixed":
            nr_mutations = int(nr_offspring*0.33)
            nr_offspring -= nr_mutations
            offspring += self.pop_mutate(nr_mutations)
            offspring += self.pop_crossover(nr_offspring)
        return self.pop_sorted(offspring)

    def pop_mutate(self, nr_offspring):
        offspring = []
        for inv in self.population:
            offspring.append(inv.mutation)
        return offspring

    def pop_crossover(self, nr_offspring):
        pass


    def getFitnesses(self):    #manipulação dos valores de aptidão
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
        
    
    
