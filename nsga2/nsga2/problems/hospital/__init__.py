# -*- coding: utf-8 -*-
"""Module with definition of Hospital problem interface"""

from nsga2.individual import Individual
from nsga2.problems import Problem
import myHospitalObjection
import functools
import numpy as np

class Hospital(Problem):

    def __init__(self,hospital_definitions,vardim,bound,hos_opt):
        self.hos_definitions = hospital_definitions
        self.max_objectives = [None, None]
        self.min_objectives = [None, None]
        self.problem_type = None
        
        # self-defined parameters
        self.vardim = vardim
        self.bound = bound
        self.hos_opt = hos_opt
		
    def __dominates(self, individual2, individual1):
        worse_than_other = self.hos_definitions.f1(individual1) <= self.hos_definitions.f1(individual2) and self.hos_definitions.f2(individual1) <= self.hos_definitions.f2(individual2)
        better_than_other = self.hos_definitions.f1(individual1) < self.hos_definitions.f1(individual2) or self.hos_definitions.f2(individual1) < self.hos_definitions.f2(individual2)
        return worse_than_other and better_than_other

    
    def generateIndividual(self):
        
        individual = Individual()
        individual.vardim = self.vardim
        individual.bound = self.bound
        individual.hos_opt = self.hos_opt
                
        ##-----------------初始化待优化的医院---------------##
        '''初始化随机生成染色体（多个基因的list），长度为个体的维度'''
        len = self.vardim
        rnd = np.random.random(size=len) #n维0-1之间的向量
        individual.features = np.zeros(len) #长尾为n的0维向量
        #在上限、下限之间生成染色体的值
        for i in xrange(0, len):
            individual.features[i] = int(self.bound[0, i] + (self.bound[1, i] - self.bound[0, i]) * rnd[i])
        #计算目标函数值
        self.calculate_objectives(individual)
        #进行支配非支配的计算
        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        return individual

    def calculate_objectives(self, individual):
        ##------------------start to calculate objectives--------------------##
        ave_dis, outliers, grid_dens = myHospitalObjection.objFunction(individual)
        #按照比例计算
        individual.avedis_ratio = ave_dis/4813.47756651
        individual.outliers_ratio = float(outliers)/23
        individual.grid_dens = grid_dens
        
        ##------------------end to calculate objectives ---------------------##
        individual.objectives = []
        individual.objectives.append(self.hos_definitions.f1(individual))
        individual.objectives.append(self.hos_definitions.f2(individual))
        for i in range(2):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
	
	