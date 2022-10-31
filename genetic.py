# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:11:41 2022

@author: alixp
"""
# from importlib.machinery import SourceFileLoader
# b = SourceFileLoader("board", "C:/Users/alixp/OneDrive/Bureau/CSULB/classes/CECS 551 Advanced AI/AlgoG_HillCliming/board.py").load_module()

import time
import random
import board as b



class Genetic:
    def __init__(self, n_queen = 5 , n_states = 8):
        self.n_queen = n_queen
        self.population = list()
        self.len_pop = n_states
        self.generation = 1
        self.best = list()
        
        
        for i in range(n_states):
            self.population.append(b.Board(n_queen))
            
    def Random(self, percent):
        return random.randint(0,percent*len(self.population)-1)
            
    def Selection(self,i):
        parent1 = self.population[i]
        parent2 = self.population[i+1]
        return parent1, parent2
    
    def Crossover(self, b1, b2):
        #choose random characteristic to keep from each parents
        k = random.randint(1,self.n_queen-1)
        
        for i in range(k):
             b1_index = b1.get_map()[i].index(1)
             b2_index = b2.get_map()[i].index(1)
             b1.flip(i,b1_index)
             b1.flip(i,b2_index)
            
        return b1
    
    def Mutation(self, b):
        #25% of chance to have a mutation
        p = random.randint(1,100)
        
        if p<=25 :
            i = random.randint(0,self.n_queen-1)
            b_index = b.get_map()[i].index(1)
            b.flip(i,b_index)
            
            j = random.randint(0,self.n_queen-1)
            b.flip(i,j)
            
        return b
    
    def CollectPop(self, tup_pop):
        new_pop = list()
        for i in tup_pop :
            new_pop.append(i[0])
        return new_pop
    
    def Fitness(self):
        costs = list()
        for individual in self.population :
            costs.append((individual, individual.get_fitness()))
        
        return sorted(costs, key = lambda tup : tup[1])
        
        #initialize a list of best individuals
        best_individus = sorted(self.best, key = lambda tup : tup[1])
        
        for i in range(iteration):
            
            print("\n--- ITERATION", i+1,"---\n")
            
            new_generation = list()
            
            # Sort the population by ascending cost  
            self.population = self.CollectPop(self.Fitness())
                        
            
            if len(best_individus)<=0 : 
                # Initialization of the list
                self.best.add((self.population[0],self.population[0].get_fitness()))
                self.best.add((self.population[1],self.population[1].get_fitness()))
            else :
                if self.population[0].get_fitness() < best_individus[0][1] :
                    print("ajout d'un best individu :", self.population[0],"cost :",self.population[0].get_fitness())
                    self.best.add((self.population[0], self.population[0].get_fitness()))
    
            print("BEST INDIVIDUALS", self.best)
            for i in list(self.best):
                i[0].show_map()
                print('cost',i[1])
                print('cost Reel',i[0].get_fitness())
                
            
            
            # print('\nSORT POPULATION') ---ok
            # print(self.Fitness())
            
            # print('\nCURRENT POPULATION') 
            # print(self.population) #---ok
            # for i in self.population :
            #     print(i.get_fitness())
            #     i.show_map()
            
            
            print("\nBEST COST",  self.population[0].get_fitness())
            
            # stop condition
            if self.population[0].get_fitness() == 0 :
                return self.population[0].show_map()
            
            else :
                
                for i in range(self.len_pop):
                    if i < 0.25*self.len_pop :
                        # we keep the 25% best individuals of the population
                        next_board = sorted(self.best, key = lambda tup : tup[1])[i][0]
                        
                    else :
                        b1, b2 = self.Selection(i-2)
                        # print("PARENT'S SELECTION :")
                        # print("\nparent b1", b1)
                        # b1.show_map()
                        # print("parent b2", b2)
                        # b2.show_map()
                        # next_board = self.Crossover(b1, b2)
                        # Apply a potential mutation (25% chance)
                        next_board = self.Mutation(next_board)
                        
                        
                    # print("next child",i+1,next_board,'cost :',next_board.get_fitness() )
                    # next_board.show_map()
                    # print("cost :",next_board.get_fitness())
                    new_generation.append(next_board)
                
               
                
                self.population = new_generation 
                
                # Sort the population by ascending cost  
                self.population = self.CollectPop(self.Fitness())
            
                # print('\nNEW GENERATION')
                # print(self.population)
                # for i in self.population :
                #     print(i.get_fitness())
                #     i.show_map()
               
                self.generation += 1
            
        return sorted(self.best, key = lambda tup : tup[1])[0][0]
            
    def AlgoG(self, iteration = 1000):
                
        for i in range(iteration):
            
            new_generation = list()
            
            # Sort the population by ascending cost  
            self.population = self.CollectPop(self.Fitness())
            
           
            if len(self.best) == 0 or self.population[0].get_fitness() < self.best[0][1] :
                if len(self.best) != 0 :
                    del self.best[0]
                self.best.append([self.population[0],self.population[0].get_fitness()])
            
            # trier best
            self.best = sorted(self.best, key = lambda tup : tup[1])
            

            # stop condition
            if self.best[0][1] == 0 :
                return i+1, self.best[0]
            
            else :
                for i in range(int(self.len_pop/2)):
                    b1, b2 = self.Selection(i)
                    next_board = self.Crossover(b1, b2)
                    # Apply a potential mutation (25% chance)
                    next_board = self.Mutation(next_board)
                    new_generation.append(next_board)
                    next_board = self.Crossover(b2, b1)
                    # Apply a potential mutation (25% chance)
                    next_board = self.Mutation(next_board)
                    new_generation.append(next_board)
                    
                self.population = new_generation 
                
                # Sort the population by ascending cost  
                self.population = self.CollectPop(self.Fitness())
                
                self.generation += 1
            
        return i+1, self.best[0]
            

        
        for i in range(iteration):
            
            print("\n--- ITERATION", i+1,"---\n")
            new_generation = list()
            
            # Sort the population by ascending cost  
            self.population = self.CollectPop(self.Fitness())
            
            # add the best two individuals to a set of best
            best_individus = sorted(self.best, key = lambda tup : tup[1])
            
            if len(best_individus)<=0 : 
                # Initialization
                self.best.add((self.population[0],self.population[0].get_fitness()))
                self.best.add((self.population[1],self.population[1].get_fitness()))
            else :
                if self.population[0].get_fitness() < best_individus[0][1] :
                    self.best.add((self.population[0],self.population[0].get_fitness()))
    
            print("BEST INDIVIDUALS", self.best)
            
            
            # print('\nSORT POPULATION') ---ok
            # print(self.Fitness())
            
            # print('\nCURRENT POPULATION') 
            # print(self.population) #---ok
            # for i in self.population :
            #     print(i.get_fitness())
            #     i.show_map()
            
            
            print("\nBEST COST",  self.population[0].get_fitness())
            
            # stop condition
            if self.population[0].get_fitness() == 0 :
                return self.population[0].show_map()
            
            else :
                
                for i in range(self.len_pop):
                    if i < 0.25*self.len_pop :
                        # we keep the 25% best individuals of the population
                        next_board = sorted(self.best, key = lambda tup : tup[1])[i][0]
                        
                    else :
                        b1, b2 = self.Selection()
                        # print("PARENT'S SELECTION :")
                        # print("\nparent b1", b1)
                        # b1.show_map()
                        # print("parent b2", b2)
                        # b2.show_map()
                        next_board = self.Crossover(b1, b2)
                        # Apply a potential mutation (25% chance)
                        next_board = self.Mutation(next_board)
                        
                        
                    # print("next child",i+1,next_board,'cost :',next_board.get_fitness() )
                    # next_board.show_map()
                    # print("cost :",next_board.get_fitness())
                    new_generation.append(next_board)
                
               
                
                self.population = new_generation 
                
                # Sort the population by ascending cost  
                self.population = self.CollectPop(self.Fitness())
            
                # print('\nNEW GENERATION')
                # print(self.population)
                # for i in self.population :
                #     print(i.get_fitness())
                #     i.show_map()
               
                self.generation += 1
            
        return sorted(self.best, key = lambda tup : tup[1])[0][0]
if __name__ == '__main__':
    start_time = time.time()   
    algoG = Genetic(5,8)
    it, result = algoG.AlgoG()
    print("Running time : %s ms" % round((time.time() - start_time)*1000,2))
    # print("--- ITERATION %s ---" %it)
    result[0].show_map()
    # print("cost",result[1])
