# -*- coding: utf-8 -*-
from metrics.problems.hospital import HospitalMetrics
from plotter import Plotter
from nsga2.problems.hospital.hospital_definitions import HospitalDefinitions
from nsga2.problems.hospital import Hospital
from nsga2.evolution import Evolution
import numpy as np
import time

import profile 

def print_generation(vardim,iteration,population, generation_num):
    print("Iteration:{},Generation: {}".format(iteration,generation_num))

def print_metrics(vardim,iteration,population, generation_num):
    pareto_front = population.fronts[0]
    metrics = HospitalMetrics()
    hv = metrics.HV(pareto_front)
    hvr = metrics.HVR(pareto_front)
    print("HV: {}".format(hv))
    print("HVR: {}".format(hvr))

collected_metrics = {}
def collect_metrics(vardim,iteration,population, generation_num):
    pareto_front = population.fronts[0]
    metrics = HospitalMetrics()
    hv = metrics.HV(pareto_front)
    hvr = metrics.HVR(pareto_front)
    collected_metrics[generation_num] = hv, hvr


iteration = 20
for i in xrange(6,iteration):
    vardim  = 15
    print("----------started----------  "+str(vardim)+ '----'+time.strftime("%H:%M:%S"))
    num_of_generations = 50
    num_of_individuals = 10
    bound = np.tile([[0], [51]], vardim)
    ##-----------确定待优化的医院-----------------##
    '''每一个generation就生成一个新的优化对象，即在一次迭代的100次中目标对象是不变的'''
    '''
    # hos_opt_id_arr 存储需要优化的医院ID，顺序为晚高峰的拥堵指数降序排序
    hos_opt_id_arr = [113,122,11,47,46,6,1,62,26,94,27,48,29,35,71,96,\
                    156,50,32,112,132,84,56,49,136,134,75,31,57,36,54,59,\
                    114,13,40,14,66,5,63,107,176,133,180,97,162,123,0,67]
    '''
    # hos_opt_id_arr 存储需要优化的医院ID，traffic的前10以及road的前10，非重复数值16个
    hos_opt_id_arr = [1,6,11,26,27,29,35,46,47,62,71,84,94,113,122,132]
    #打乱数组顺序，随机洗牌，选取前P个作为候选点
    np.random.shuffle(hos_opt_id_arr)
    hos_opt = hos_opt_id_arr[0:vardim]
    
    hos_definitions = HospitalDefinitions()
    plotter = Plotter(hos_definitions)
    problem = Hospital(hos_definitions,vardim,bound,hos_opt)
    '''Evolution(self,problem, vardim, num_of_generations, num_of_individuals, mutation_prob, num_of_genes_to_mutate, num_of_tour_particips)'''
    evolution = Evolution(problem, vardim,i, num_of_generations,num_of_individuals,0.4,1,2)
    evolution.register_on_new_generation(plotter.plot_population_best_front)
    evolution.register_on_new_generation(print_generation)
    evolution.register_on_new_generation(print_metrics)
    evolution.register_on_new_generation(collect_metrics)
    pareto_front = evolution.evolve()
    
    plotter.plot_x_y(collected_metrics.keys(), map(lambda(hv, hvr): hvr, collected_metrics.values()), 
    'generation', 'HVR', 'HVR metric for Hospital relocation problem', str(vardim)+'-'+str(i)+'-'+'HVR')
    fout = open("D:\\PythonCode\\NSGA-II\\txt\\"+str(vardim)+'-'+str(i)+'-'+'metrics.txt','w')
    fout.write('generation,HV,HVR'+'\n')
    for order in xrange(len(collected_metrics)):
        fout.write(str(order)+','+str(collected_metrics[order][0])+','+str(collected_metrics[order][1])+'\n')
    fout.close()
 

       
print("----------finished----------  "+ time.strftime("%H:%M:%S"))
        