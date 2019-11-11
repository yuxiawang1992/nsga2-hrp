import os
import matplotlib.pyplot as pyplot

class Plotter():
    def __init__(self, problem):
        self.directory = 'plots'
        self.problem = problem

    
    def plot_population_best_front(self,vardim,iteration, population, generation_number):
        filename = "{}/generation{}-{}-{}.png".format(self.directory, str(vardim),str(iteration),str(generation_number))
        self.__create_directory_if_not_exists()
        computed_pareto_front = population.fronts[0]
        self.__plot_front(computed_pareto_front, filename)
        #------below it is to write out each generation's best front number-----
        f1 = open("D:\\PythonCode\\NSGA-II\\txt\\"+str(vardim)+'-'+str(iteration)+'-'+str(generation_number)+'-'+'pareto_front.txt','w')
        f1.write("num,avedis_ratio,outliers_ratio,obj1,obj2,rank,crowding_dis"+'\n')
        
        for i in xrange(len(population.fronts[0])):
            f1.write(str(i)+','+str(population.fronts[0][i].avedis_ratio)+','+str(population.fronts[0][i].outliers_ratio)+','+\
            str(population.fronts[0][i].objectives[0])+','+str(population.fronts[0][i].objectives[1])+','+str(population.fronts[0][i].rank)+','+\
            str(population.fronts[0][i].crowding_distance))
            
            for j in xrange(len(population.fronts[0][i].hos_opt)):
                f1.write(','+str(population.fronts[0][i].hos_opt[j]))
                
            for j in range(len(population.fronts[0][i].features)):
                f1.write(','+str(population.fronts[0][i].features[j]))
            
            f1.write('\n')
            
        f1.close()
        
        f2 = open("D:\\PythonCode\\NSGA-II\\txt\\"+str(vardim)+'-'+str(iteration)+'-'+str(generation_number)+'-'+'grid_dens.txt','w')
        f2.write("grid_id")
        for i in xrange(len(population.fronts[0])):
            f2.write(','+'dens_'+str(i))
        f2.write('\n')
        
        for j in xrange(len(population.fronts[0][0].grid_dens)):
            f2.write(str(j))
            for i in xrange(len(population.fronts[0])):
                f2.write(','+str(population.fronts[0][i].grid_dens[j]))
            f2.write('\n')
                
        f2.close()  
        

    def plot_x_y(self, x, y, x_label, y_label, title, filename):
        filename = "{}/{}.png".format(self.directory, filename)
        self.__create_directory_if_not_exists()
        figure = pyplot.figure()
        axes = figure.add_subplot(111)
        axes.plot(x, y, 'r')
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.set_title(title)
        pyplot.savefig(filename)
        pyplot.close(figure)

    def __create_directory_if_not_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def __plot_front(self, front, filename):
        figure = pyplot.figure()
        axes = figure.add_subplot(111)

        computed_f1 = map(lambda individual: individual.objectives[0], front)
        computed_f2 = map(lambda individual: individual.objectives[1], front)
        axes.plot(computed_f1, computed_f2, 'g.')
        
        ###############have been altered , no plot of the perfect pareto front##############
        #perfect_pareto_front_f1, perfect_pareto_front_f2 = self.problem.perfect_pareto_front()
        #axes.plot(perfect_pareto_front_f1, perfect_pareto_front_f2, 'r.')

        axes.set_xlabel('f1')
        axes.set_ylabel('f2')
        axes.set_title('Computed Pareto front')
        pyplot.savefig(filename)
        pyplot.close(figure)


