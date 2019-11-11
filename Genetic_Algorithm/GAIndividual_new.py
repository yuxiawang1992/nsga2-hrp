#Python 2.7.8
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 18:48:52 2016
遗传算法的个体
@author: dell
"""

import numpy as np
import myObjectionCache_new


class GAIndividual:

    '''
    遗传算法的个体，也就是染色体
    '''

    def __init__(self,  vardim, bound):
        '''
        vardim: 变量的维数
        bound: 变量的边界
        初始的适应度函数为0
        '''
        self.vardim = vardim
        self.bound = bound
        self.fitness = 0.
        self.avedis = 0.
        self.outliers = 0
        self.opthos = [0,0,0,0,0]
        self.grid_dens = [0]*8748

    def generate(self):
        '''
        为遗传算法生成一个随机地的染色体，长度为个体的维度
        '''
        len = self.vardim
        rnd = np.random.random(size=len) #n维0-1之间的向量
        self.chrom = np.zeros(len) #长尾为n的0维向量
        #在上限、下限之间生成染色体的值
        for i in xrange(0, len):
            self.chrom[i] = int(self.bound[0, i] + \
                (self.bound[1, i] - self.bound[0, i]) * rnd[i])

    def calculateFitness(self,alpha):
        '''
        计算染色体的适宜度，即计算目标函数的值
        '''
        '''
        self.fitness = ObjFunction.GrieFunc(
            self.vardim, self.chrom, self.bound)
        '''
        self.fitness, self.avedis, self.outliers, self.opthos, self.grid_dens = myObjectionCache_new.objFunction(self.vardim,self.chrom,self.bound,alpha)
