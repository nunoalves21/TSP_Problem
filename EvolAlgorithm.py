# -*- coding: utf-8 -*-

from Popul import Popul

class EvolAlgorithm:
    
    def __init__ (self, popsize, numits, noffspring, indsize):
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize
        
    def initPopul(self, indsize):
        self.popul = Popul(self.popsize, indsize)
        
    def iteration(self):
        parents = self.popul.selection(self.noffspring)
        offspring = self.popul.recombination(parents, self.noffspring)
        self.evaluate(offspring)
        self.popul.reinsertion(offspring)
    
    def evaluate(self, indivs):   #faz a ligação ao problema    #se substituirmos esta função conseguimos adaptar o algoritmo evol a qualquer problema com "resolução" binária
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():
                if x == 1: fit += 1.0    #conta quantos 1's temos
            ind.setFitness(fit)    #guarda o fitness no indivíduo
        return None
    
    def run(self):           #é o pipeline do algoritmo toodo
        self.initPopul(self.indsize)
        self.evaluate(self.popul.indivs)
        self.bestsol = []
        self.bestfit = 0.0
        for i in range(self.numits+1):      #garannte que ficamos com a melhor solução encontrada
            self.iteration()
            bs, bf = self.popul.bestSolution()    #dá individuo com melhor solução e qual foi o melhor fitness
            if bf > self.bestfit:
                self.bestfit = bf
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.popul.bestFitness())
        print("BestFitFound:", self.bestfit)
        #self.bestsol, self.bestfit = self.popul.bestSolution()


def test():
    ea = EvolAlgorithm(100, 2000, 50, 1000) #100 -> tamanho da pop;
    ea.run()


if __name__ == "__main__":  
    test()
