# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:11:16 2019

@author: fatih
"""
 
from random import randint
import random
import numpy as np
import pandas as pd
import math
import pdb
import operator
import functools

counter = 0

# Number of individuals in each generation

b_i = pd.read_csv('batchange.csv')
B = b_i.to_numpy()
B = B[~np.isnan(B)]


r_i = pd.read_csv('route.csv')
R = r_i.to_numpy()
R = R[~np.isnan(R)]


l_i = pd.read_csv('loopnr.csv')
L = l_i.to_numpy()
L = L[~np.isnan(L)]


coef_i = pd.read_csv('coef.csv')
coef = coef_i.to_numpy()

rega = 70.12012477
regb = -0.002160699
regc = -0.214444407


POPULATION_SIZE = 200

maxgen = 1000

GENES = [0,1]

TARGET = 10000

trnmt = 5

X = np.zeros(shape=(len(B)))

charge = np.zeros(shape=(len(B)))

lorder = np.zeros(shape=(len(B)))

nKi = np.zeros(shape=(len(B)))

def round5(x, base=5):
    return base * math.floor(x/base)

def selection(population):
    tournament = (random.choice(population) for i in range(trnmt))
    tournament = sorted(tournament, key = lambda x:x.fitness, reverse = True)
    return tournament

class Individual(object):
    '''
    Class representing individual in population
    '''
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()
        self.nKi = nKi
        
        
    @classmethod
    def mutated_genes(self):
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        global TARGET
        gnome_len = len(B)*len(coef)
        return [self.mutated_genes() for _ in range(gnome_len)]
    
    def mate(self, par2):
        '''
        Perform mating and produce new offspring
        '''

        child_chromosome = []
        q = 0
        
        matecount = 0
        
        for i, j in zip(self.chromosome, par2.chromosome):
            matecount += 1
            if matecount % len(coef) == 1:
                prob = random.random()
               
            if prob < ((1-mrate)/2):
                child_chromosome.append(i)

            elif prob < (1-mrate):
                child_chromosome.append(j)

            else:
                child_chromosome.append(self.mutated_genes())
            
            
        for k in range(len(child_chromosome)):
            if R[int(math.floor(k/len(coef)))] == 1:
                child_chromosome[k] = 0
        
        return Individual(child_chromosome)

    def cal_fitness(self):
        
        fitness = 0
        weight = 0
        minch =[]
        addition = []
        remain = []

        for i in range(len(B)):
            charge[i] = 0
            
        nKromozom = list(map(int,self.chromosome))
        nK = np.asarray(nKromozom)
        
        for i in range(len(B)):
            nKi[i] = 0
                
        for i in range(len(B)):
            for j in range(len(coef)):
                nKi[i] += nK[i*len(coef)+j]*(2**coef[j])
        
        for i in range(len(B)):
            if i == 0:
                lorder[i] = 1
            else:
                if L[i] == L[i-1]:
                    lorder[i] = lorder[i-1] + 1
                else:
                    lorder[i] = 1
        
        n = 1
        while n <= int(max(L)):
            mi = 0
            for i in range(len(B)):
                if mi > B[i] and n == L[i]:
                    mi = B[i]
            minch.append(mi)
            n += 1
            
        for i in range(len(minch)):
            addition.append(round5(minch[i])/(-5))
        
        temp = 0
        n = 1
        while n <= int(max(L)):
            temp = max(minch[n-1]*(-1) - sum(B[i] for i in range(len(B)) if L[i] == n),0)
            n += 1
            remain.append(temp)
            
        for i in range(len(remain)):
            remain[i] = max(round5(remain[i]*(-1))/(-5),0)
        
        for i in range(len(B)):
            for j in range(len(B)):
                if L[i] == L[j] and j >= i:
                    charge[j] += nKi[i]*5
        
        for i in range(len(B)):
            X[i] = min(B[i] + charge[i], 100)
            
        for i in range(len(B)):    
            if X[i] < 0:
                fitness += (0-X[i])*200
        
        for i in range(len(B)):
            fitness += ((nKi[i]**2)*rega + (nKi[i]-charge[i])*regb + regc)*nKi[i]/50
            
        #for i in range(len(remain)):
        #    fitness += remain[i]*25
            
        for i in range(len(B)):
            if nKi[i] > 0:
                fitness += 500
                
        for i in range(len(remain)):
            if remain[i] > 0:
                fitness += remain[i]*25
                
        for i in range(len(B)):
            if R[i] == 1:
                if nK[i] > 0:
                    fitness += nK[i]*100
                
        #for i in range(len(B)):
        #    if charge[i] + B[i] > 100:
        #        fitness += 2000
            

        return fitness
        

def main():
    global POPULATION_SIZE
    global generation
    global minfitness
    global mrate
    global counter
    mrate = 0.2
    #current generation 
    generation = 1
    minfitness = 50000
    found = False
    population = []

    for _ in range(POPULATION_SIZE):
                #belirlenmiş bşl çözümü
                gnome = Individual.create_gnome()
                
    population.append(Individual(gnome))

    while not found:
       
        population = sorted(population, key = lambda x:x.fitness)

        if population[0].fitness <= 0:
            found = True
            break
        
        if generation == maxgen:
            found = True
            break
        
        if population[0].fitness < minfitness:
            counter = 0
        else:
            counter += 1
        
        if population[0].fitness <= minfitness:
                minfitness = population[0].fitness
        
        if counter == 25:
            mrate = 0.2
        
        print("Generation: {}\Kromozom: {}\tFitness: {} Charge: {}".\
              format(generation,
              population[0].chromosome,
              population[0].fitness,
              population[0].nKi*5))

                                 
        new_generation = []
        
        mrate -= (0.2/10000)
        
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])
        
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            
            parent1 = selection(population)[0]
            parent2 = selection(population)[0]
            
            child = parent1.mate(parent2)
        
    
        new_generation.append(child)
        population = new_generation     

        generation += 1

    print("Generation: {}\Kromozom: {}\tFitness: {}".\
          format(generation,
          population[0].chromosome,
          population[0].fitness))

if __name__ == '__main__':
    main()