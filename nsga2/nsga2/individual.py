"""Module with main parts of NSGA-II algorithm.
It contains individual definition"""

class Individual(object):
    """Represents one individual"""
    
    def __init__(self):
        self.rank = None
        self.crowding_distance = None
        self.dominated_solutions = set()
        self.features = None
        self.objectives = None
        self.dominates = None
        
        # self-defined parameters
        self.vardim = None
        self.bound = None
        self.hos_opt = None
        self.grid_dens = None
        self.avedis_ratio = None
        self.outliers_ratio = None
        
    def set_objectives(self, objectives):
        self.objectives = objectives
        
