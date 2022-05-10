from typing import List
import numpy as np
from ..engines import Tracer
from ..utils import VecDistance
from ..models import TheoreticalOutdoorModel

class LocationPredictionGym():
    '''
    
    '''

    def __init__(self, scene_path: str, cell_pos, generator_seed= 0):
        super().__init__()
        self.scene_path = scene_path
        self.tracer = Tracer(scene_path, ref_max=1)
        assert self.tracer.is_outdoor(cell_pos)
        self.cell_pos = cell_pos
        self.generator = np.random.default_rng(generator_seed)
        self.ue_limit =  {
            'min_x': self.tracer.min_bound[0],
            'max_x': self.tracer.max_bound[0],
            'min_y': 1.5,
            'max_y': 1.8,
            'min_z': self.tracer.min_bound[2],
            'max_z': self.tracer.max_bound[2],
        }
        self.ue_pos = self.random_outdoor(self.ue_limit)

    def random_outdoor(self, limit):
        outdoor = False
        while not outdoor:
            random_x = self.generator.uniform(low=limit['min_x'],
                                         high=limit['max_x'], size=1)[0]
            random_y = self.generator.uniform(low=limit['min_y'],
                                         high=limit['max_y'], size=1)[0]
            random_z = self.generator.uniform(low=limit['min_z'],
                                         high=limit['max_z'], size=1)[0]
            new_position = np.array([random_x, random_y, random_z])
            if self.tracer.is_outdoor(new_position):
                self.ue_pos = new_position
                outdoor = True
        return new_position

    def get_state(self, window=5):
        traced_result = self.tracer.trace_outdoor(self.cell_pos, self.ue_pos)
        model = TheoreticalOutdoorModel(traced_result, tx_power_dbm=15)
        impulses = model.calculate_signal_impulses()
        impulses.sort(key=lambda i: i['delay'])
        return impulses

    def predict(self, predicted_location: List)->float:
        distance = VecDistance(predicted_location, self.ue_pos)
        return distance

    def reset(self):
        self.ue_pos = self.random_outdoor(self.ue_limit)