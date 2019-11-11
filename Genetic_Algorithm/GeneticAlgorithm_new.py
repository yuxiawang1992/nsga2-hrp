#Python 2.7.8
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 18:49:19 2016

@author: dell
"""

import numpy as np
from GAIndividual_new import GAIndividual
import random
import copy
import matplotlib.pyplot as plt
import time

class GeneticAlgorithm:

    '''
    类：遗传算法
    '''

    def __init__(self, sizepop, vardim, bound, MAXGEN, params,iteration,alpha):
        '''
        sizepop:种群的大小 population sizepop
        vardim: 变量的维数 dimension of variables
        bound: 变量的上下界 boundaries of variables
        MAXGEN: 终止条件，即最大的循环次数 termination condition
        param: 交叉率，变异率，以及alpha algorithm required parameters, it is a list which is consisting of crossover rate, mutation rate, alpha
        '''
        self.sizepop = sizepop
        self.MAXGEN = MAXGEN
        self.vardim = vardim
        self.bound = bound
        self.population = []
        self.fitness = np.zeros((self.sizepop, 1))
        self.trace = np.zeros((self.MAXGEN, 2))
        self.params = params
        self.iteration = iteration
        self.alpha = alpha

    def initialize(self):
        '''
        初始化种群
        '''
        for i in xrange(0, self.sizepop):
            ind = GAIndividual(self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)

    def evaluate(self):
        '''
        评估种群的适宜度
        '''
        for i in xrange(0, self.sizepop):
            self.population[i].calculateFitness(self.alpha)
            self.fitness[i] = self.population[i].fitness

    def solve(self):
        '''
        遗传算法的演化过程
        '''
        start_time = time.clock()
        self.t = 0
        self.initialize()
        self.evaluate()
        best = np.max(self.fitness) #最好的值为适宜度的最大值
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])
        self.avefitness = np.mean(self.fitness)
        self.trace[self.t, 0] =  self.best.fitness
        self.trace[self.t, 1] =  self.avefitness
        print("Generation %d: optimal function value is: %f; average function value is %f" % (
            self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while (self.t < self.MAXGEN - 1):
            self.t += 1            
            self.selectionOperation()
            self.crossoverOperation()
            self.mutationOperation() 
            self.evaluate()
            best = np.max(self.fitness)
            print('种群中最好的个体为--------：'+str(best))
            bestIndex = np.argmax(self.fitness)
            if best > self.best.fitness:
                self.best = copy.deepcopy(self.population[bestIndex])
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t, 0] = self.best.fitness
            self.trace[self.t, 1] = self.avefitness
            print("Generation %d: optimal function value is: %f; average function value is %f" % (
                self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
            #print("fitness is : %f ") %(self.best.fitness)
            #print("chronomose is : %s ") %(self.best.chrom)

        print("---------Optimal function value is: %f; " %
              self.trace[self.t, 0])
        print("----------Optimal solution is:"+str(self.best.chrom))
        print('-----------------------------------------------------')
        
        end_time = time.clock()
        time_used = end_time - start_time
        
        #存储输出结果,每一次输出三个表
        with open("E:\\0000\\optimize\\"+str(self.vardim)+'-'+str(self.alpha)+'-'+str(self.iteration)+'result.txt','w') as f1:
            f1.write("hos_opt,hos_can,objvalue,ave_dis,grid_outliers,time_used"+'\n')
            f1.write(str(self.best.opthos)+','+str(self.best.chrom)+','+ str(self.best.fitness)+ \
            ','+str(self.best.avedis)+','+str(self.best.outliers)+','+str(time_used)+'\n')
        with open("E:\\0000\\optimize\\"+str(self.vardim)+'-'+str(self.alpha)+'-'+str(self.iteration)+'grid_dens.txt','w') as f2:
            f2.write("grid_id,grid_dens"+'\n')
            for i in range(8748):
                f2.write(str(i)+','+str(self.best.grid_dens[i])+'\n')
        with open("E:\\0000\\optimize\\"+str(self.vardim)+'-'+str(self.alpha)+'-'+str(self.iteration)+'trace.txt','w') as f3:
            f3.write("iteration,best_fitness,ave_fitness"+'\n')
            for i in range(len(self.trace[:, 0])):
                f3.write(str(i)+','+str(self.trace[i,0])+','+str(self.trace[i,1])+'\n')
            
        #self.printResult()

    def selectionOperation(self):
        '''
        选择过程：产生一个随机数，选择适宜度在此随机数之间的后个个体
        selection operation for Genetic Algorithm
        轮盘赌（Roulette Wheel Selection）选择法
        '''
        newpop = []
        totalFitness = np.sum(self.fitness)
        accuFitness = np.zeros((self.sizepop, 1))

        sum1 = 0.
        for i in xrange(0, self.sizepop):
            accuFitness[i] = sum1 + self.fitness[i] / totalFitness
            sum1 = accuFitness[i]

        for i in xrange(0, self.sizepop):
            r = random.random()
            idx = 0
            for j in xrange(0, self.sizepop - 1):
                if j == 0 and r < accuFitness[j]:
                    idx = 0
                    break
                elif r >= accuFitness[j] and r < accuFitness[j + 1]:
                    idx = j + 1
                    break
            newpop.append(self.population[idx])
        self.population = newpop


    def crossoverOperation(self):
        '''
        交叉操作：产生两个随机数，获得种群中两个随机地个体
        如果随机概率小于交叉率，获得随机交叉点位置，根据变异率的大小确定是否变号
        crossover operation for genetic algorithm
        '''
        newpop = []
        for i in xrange(0, self.sizepop, 2):
            idx1 = random.randint(0, self.sizepop - 1)
            idx2 = random.randint(0, self.sizepop - 1)
            while idx2 == idx1:
                idx2 = random.randint(0, self.sizepop - 1)
            newpop.append(copy.deepcopy(self.population[idx1]))
            newpop.append(copy.deepcopy(self.population[idx2]))
            r = random.random()
            if r < self.params[0]:
                #print(self.population[idx1].chrom)
                crossPos = random.randint(1, self.vardim - 1)
                for j in xrange(crossPos, self.vardim):
                    temp =  newpop[i].chrom[j]
                    newpop[i].chrom[j] = newpop[i+1].chrom[j]
                    newpop[i+1].chrom[j] = temp
                    #newpop[i].chrom[j] = int(newpop[i].chrom[j] * self.params[2] + (1 - self.params[2]) * newpop[i + 1].chrom[j])
                    #newpop[i + 1].chrom[j] = int(newpop[i + 1].chrom[j] * self.params[2] + (1 - self.params[2]) * newpop[i].chrom[j])
            
        self.population = newpop

    def mutationOperation(self):
        '''
        变异操作：随机概率小于变异概率，获得随机变异点位置，在此判断随机概率大于0.5，则变异操作
        mutation operation for genetic algorithm
        '''
        newpop = []
        for i in xrange(0, self.sizepop):
            newpop.append(copy.deepcopy(self.population[i]))
            r = random.random()
            if r < self.params[1]:
                mutatePos = random.randint(0, self.vardim - 1)
                theta = random.random()
                if theta > 0.5:
                    newpop[i].chrom[mutatePos] = int(newpop[i].chrom[
                        mutatePos] - (newpop[i].chrom[mutatePos] - self.bound[0, mutatePos]) * (1 - random.random() ** (1 - self.t / self.MAXGEN)))
                else:
                    newpop[i].chrom[mutatePos] = int(newpop[i].chrom[
                        mutatePos] + (self.bound[1, mutatePos] - newpop[i].chrom[mutatePos]) * (1 - random.random() ** (1 - self.t / self.MAXGEN)))
        self.population = newpop


    def printResult(self):
        '''
        绘图函数
        plot the result of the genetic algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("fitness value")
        plt.title("Genetic algorithm for function optimization")
        plt.legend()
        plt.show()

        
if __name__ == "__main__":
    
    #可能时间不够，多次循环就这个了 
    for i in range(5):
        for vardim in range(11,21):
            for alpha in range(0,6):
                alpha = alpha * 0.1
                bound = np.tile([[0], [51]], vardim)
                if vardim <= 10 :
                    iteration = 50
                elif vardim >10 and vardim <= 15:
                    iteration = 100
                else:
                    iteration = 150
                ga = GeneticAlgorithm(10, vardim, bound, iteration, [0.9, 0.5, 0],i,alpha)
                ga.solve()
    
