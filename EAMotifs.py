# -*- coding: utf-8 -*-

from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
#from MyMotifs import MyMotifs

def createMatZeros (nl, nc):
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename,"dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)        

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize, maxvalue, [])
        
    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)   
            
    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestfit)

class EAMotifsReal (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename,"dna")
        indsize = len(self.motifs.alphabet) * self.motifs.motifSize
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)        
    
    def initPopul(self, indsize):
        self.popul = PopulReal(self.popsize, indsize, 0.0, 1.0, [])
      
    def evaluate(self, indivs):
        for i in range(len(indivs)):
            pass
            # s - solution to be evaluated - vector s
            # fit = self.motifs.score(s)
            ind.setFitness(fit)   
            
    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestfit)     
     
def test1():
    ea = EAMotifsInt (100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()

def test2():
    ea = EAMotifsReal (100, 500, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()
    
    
test1()
