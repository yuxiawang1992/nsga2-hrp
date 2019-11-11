
from nsga2 import seq
from nsga2.problems.problem_definitions import ProblemDefinitions

class HospitalDefinitions(ProblemDefinitions):

    def __init__(self):
        self.vardim = None
        self.bound = None
    
    def f1(self, individual):
        return individual.avedis_ratio

    def f2(self, individual):
        return individual.outliers_ratio
    
    def perfect_pareto_front(self):
        domain = seq(0, 1, 0.01)
        return domain, map(lambda x1: 1 - x1**2, domain)
