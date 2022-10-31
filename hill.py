# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:08:38 2022

@author: alixp
"""
import random
import time
import copy
# from importlib.machinery import SourceFileLoader
# b = SourceFileLoader("board", "C:/Users/alixp/OneDrive/Bureau/CSULB/classes/CECS 551 Advanced AI/AlgoG_HillCliming/test/board.py").load_module()
import board as b

class HillClimbing():
    
    def __init__(self, n_queens = 5, state = None):
        self.n_queens = n_queens
        self.state = state
        self.neighbors = set()
        self.best = state
        self.iteration = 0
       
        
    def WorstBoard(self) :
        worse = b.Board(self.n_queens)
        for i in range(self.n_queens):
            index1 = worse.get_map()[i].index(1)
            worse.flip(i,index1)
            worse.flip(i,0)
        return worse
    
    def Evaluate(self):
        if self.state.get_fitness == 0:
            return True
        return False
    
    def Best(self, state):
        if self.best.get_fitness() > state.get_fitness():
            self.best = state
            
    def Successor(self):
        successors = set()
        for i in range(self.n_queens) :
            for j in range(self.n_queens):
                n = copy.deepcopy(self.state)
                index1 = n.get_map()[i].index(1)
                if index1 != j :
                    n.flip(i,index1)
                    n.flip(i,j)
                    successors.add(n)
        self.neighbors = successors
        
            

    def RandomRestart(self):
        # print("I'm in random restart")
        self.state = b.Board(self.n_queens)
        self.SteepestAscentHC()
        
    def SteepestAscentHC(self):
              
        #Evaluate the initial state
        if self.Evaluate():
            return self.state
        
        current = copy.deepcopy(self.state)
        
        while self.Evaluate() != True and self.iteration < 1000:
            self.iteration += 1     
            
            # Create a board with a get_fitness worse than any neigbhors of self.state 
            SUCC = self.WorstBoard()
            
            # Find all possible neighbors of the current board
            self.Successor()
            
            # Generate the neighbors n of the current state
            for n in self.neighbors :
                self.Best(n)
                
            for n in self.neighbors :   
                if self.best.get_fitness() == self.state.get_fitness() : 
                    # Random restart
                    # self.RandomRestart()
                    self.state = b.Board(self.n_queens)
                    
                #if it is goal state return it
                if n.get_fitness() == 0 :
                    return n
                else :
                    # compare n to SUCC : if n is better set SUCC = n
                    if n.get_fitness() < SUCC.get_fitness():
                        SUCC = copy.deepcopy(n)
                    # compare SUCC to current : if SUCC is better set state = SUCC
                    if SUCC.get_fitness() < current.get_fitness():
                        self.state = SUCC
                    
        
            
        return self.RandomRestart()
            
        
    
    
if __name__ == '__main__':
    start_time = time.time()   
    Q5 = HillClimbing(5,b.Board(5))
    solution = Q5.SteepestAscentHC()
    print("Running time: %s ms" % round((time.time() - start_time)*1000,2))
    solution.show_map()