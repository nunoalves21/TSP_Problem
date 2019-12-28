# -*- coding: utf-8 -*-

from Indiv import Indiv
from random import random
import pandas as pd

class Popul:     #é um conjunto de individups com tamanho fixado

    def __init__(self, popsize, indivsize, distances_matrix):
        self.popsize = popsize         #tamanho da pop
        self.indivsize
        self.distances = distances_matrix
        self.initRandomPop(self.popsize)    

    def fitness_ranked_df(self, population):
        cols = [i for i in range(0, len(population[0]))]
        cols.append("Fitness")
        for indiv in population:
            indiv.append(self.calculate_path_distance(indiv))

        rank = pd.DataFrame(data=population, columns=cols)
        rank_sorted = rank.sort_values(by="Fitness", ascending=False)
        return rank_sorted

    def initRandomPop(self, pop_size):
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
            path = Indiv(comb)       
            while len(path.get_size()) != len(self.cities):
                pos = path[-1]
                min_dist = math.inf
                new_pos = 0
                for i in range(len(self.distances[pos])):
                    if self.distances[pos][i] < min_dist and i not in path:
                        min_dist = self.distances[pos][i]
                        new_pos = i
                path.append(new_pos)
            path.append(path.cities[0])
            population.append(path)

        self.population = self.fitness_ranked_df(population)


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
        
    
    
