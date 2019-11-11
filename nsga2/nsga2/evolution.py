"""Module with main parts of NSGA-II algorithm.
Contains main loop"""

from nsga2.utils import NSGA2Utils
from nsga2.population import Population
import time

class Evolution(object):
    
    def __init__(self, problem, vardim, iteration, num_of_generations, num_of_individuals, mutation_prob, num_of_genes_to_mutate, num_of_tour_particips):
        self.utils = NSGA2Utils(problem, vardim, num_of_generations,num_of_individuals, mutation_prob, num_of_genes_to_mutate, num_of_tour_particips)
        self.population = None
        self.vardim = vardim
        self.iteration = iteration
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
    
    def register_on_new_generation(self, fun):
        self.on_generation_finished.append(fun)
        
    def evolve(self):
        
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population,1)
        returned_population = None 
        print("-----------create the initial children----------- "+ time.strftime("%H:%M:%S"))
        for i in range(self.num_of_generations):
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            print("-----------fast nondominated sort-----------  "+ time.strftime("%H:%M:%S"))
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
                
            sorted(self.population.fronts[front_num], cmp=self.utils.crowding_operator)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population
            self.population = new_population
            print("-------------created the new children------------  "+ time.strftime("%H:%M:%S"))
            children = self.utils.create_children(self.population,i)
            print("-------------finished the new children------------  "+ time.strftime("%H:%M:%S"))
            for fun in self.on_generation_finished:
                fun(self.vardim,self.iteration,returned_population, i)
        return returned_population.fronts[0]
                
                
            
            
