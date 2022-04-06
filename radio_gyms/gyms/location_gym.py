import numpy as np 
from .base import RadioGym
from ..engines import Tracer
from ..simulations import OldtownWalk

class LocationGym(RadioGym):
    '''
    LocationGym simulates outdoor UEs uniformly generrated in an outdoor area.
    '''

    def __init__(self, scene_path: str,  ue_n = 100, generator_seed = 0,):
        super().__init__()
        self.tracer = Tracer(scene_path)
        self.simulation = OldtownWalk(self.tracer, 2, ue_n, generator_seed)
        self.simulation.pedestrian_position_limit = {
            'min_x': self.tracer.min_bound[0],
            'max_x': self.tracer.max_bound[0],
            'min_y': 0.5,
            'max_y': 1.8,
            'min_z': self.tracer.min_bound[2],
            'max_z': self.tracer.min_bound[2],
        }
        self.simulation.cell_position_limit = {
            'min_x': self.tracer.min_bound[0],
            'max_x': self.tracer.max_bound[0],
            'min_y': 2,
            'max_y': 7,
            'min_z': self.tracer.min_bound[2],
            'max_z': self.tracer.min_bound[2],
        }
        self.avg_rec = -1
    
    def calculate_avg_rec_power(self):
        results = self.simulation.get_results()
        return results

    def step():
        pass

    def render():
        pass

    def reset():
        pass

    def action(tx_pos):
        pass

    def get_states():
        pass
        
    def get_reward():
        pass

