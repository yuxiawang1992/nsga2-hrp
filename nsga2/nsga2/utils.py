"""NSGA-II related functions"""
# -*- coding: utf-8 -*-
import functools
from nsga2.population import Population
import random
import time

class NSGA2Utils(object):
    
    def __init__(self, problem, vardim, num_of_generations,num_of_individuals, mutation_prob, num_of_genes_to_mutate, num_of_tour_particips):
        
        self.problem = problem
        self.vardim = vardim
        self.max_generation = num_of_generations
        self.num_of_individuals = num_of_individuals
        self.mutation_prob = mutation_prob
        self.number_of_genes_to_mutate = num_of_genes_to_mutate
        self.num_of_tour_particips = num_of_tour_particips
        
    def fast_nondominated_sort(self, population):
        population.fronts = []
        population.fronts.append([]) 
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()
            
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)
                    
    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])
    
    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0
            
            for m in range(len(front[0].objectives)):
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num-1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num-1]):
                    front[index].crowding_distance = (front[index+1].crowding_distance - front[index-1].crowding_distance) / (self.problem.max_objectives[m] - self.problem.min_objectives[m])
                
    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
    
    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generateIndividual()
            '''have been calculate when generate the individual, to see if i was wrong'''
            #self.problem.calculate_objectives(individual)
            population.population.append(individual)
            
        return population
    
    def create_children(self, population,ith_generation):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while (parent1.features == parent2.features).all():
                parent2 = self.__tournament(population)
            print("-------finished tournament ------  "+ time.strftime("%H:%M:%S"))
            child1, child2 = self.__crossover(parent1, parent2)
            print("-------finished crossover ------  "+ time.strftime("%H:%M:%S"))
            self.__mutate(child1,ith_generation)
            self.__mutate(child2,ith_generation)
            print("-------finished mutation  ------  "+ time.strftime("%H:%M:%S"))
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            print("-------finished calculate objectives ------  "+ time.strftime("%H:%M:%S"))
            children.append(child1)
            children.append(child2)

        return children
    
    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        genes_indexes = range(len(child1.features))
        half_genes_indexes = random.sample(genes_indexes, 1)
        #######have been altered by wyx  single point crossover #############
        for i in genes_indexes:
            if (i > half_genes_indexes):
                child1.features[i] = individual2.features[i]
                child2.features[i] = individual1.features[i]
            else:
                child1.features[i] = individual1.features[i]
                child2.features[i] = individual2.features[i]
        return child1, child2

    def __mutate(self, child,ith_generation):
        #######have been altered by wyx, before it is a 0-1 mutation, now it is a interger mutation######
        genes_to_mutate = random.sample(range(0, len(child.features)), self.number_of_genes_to_mutate)
        for gene in genes_to_mutate:
            r = random.random()
            if (r < self.mutation_prob):
                theta = random.random()
                if (theta>0.5):
                    child.features[gene] = int( child.features[gene] - 
                    (child.features[gene] - self.problem.bound[0,gene])*(1-random.random()**(1-ith_generation/self.max_generation)))
                else:
                    child.features[gene] = int( child.features[gene] + 
                    (self.problem.bound[0,gene] - child.features[gene])*(1-random.random()**(1-ith_generation/self.max_generation)))
        
    def __tournament(self, population):
        participants = random.sample(population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or self.crowding_operator(participant, best) == 1:
                best = participant

        return best
