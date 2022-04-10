from kiwisolver import strength
import numpy as np

from radio_gyms.utils.constants import MAX_FLT, MIN_FLT

from ..utils.notebook import is_notebook

from ..models.theoretical import TheoreticalOutdoorModel 
from .base import RadioGym
from ..engines import Tracer
from ..simulations import OldtownWalk
from ..utils import dBmTomW

class LocationGym(RadioGym):
    '''
    LocationGym simulates outdoor UEs uniformly generrated in an outdoor area.
    '''

    def __init__(self, scene_path: str,  ue_n = 100, generator_seed = 0):
        super().__init__()
        self.tracer = Tracer(scene_path, ref_max=1)
        self.simulation = OldtownWalk(self.tracer, 2, ue_n, generator_seed, pre_gen=False)
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
            'min_y': 9,
            'max_y': 9,
            'min_z': self.tracer.min_bound[2],
            'max_z': self.tracer.min_bound[2],
            'min_tx': 17,
            'max_tx': 17
        }
        self.simulation.generate_equipment()
        self.update_result()

        self.avg_rec = -1
        self.rec_power_list = []
        self.states = None

    def update_result(self):
        self.results = self.simulation.get_results()

    def calculate_environment(self):
        results = self.results
        avg_rev_power = 0
        rec_power_list = []
        states = []
        def get_important_impulse(in_impulses):
            min_delay = MAX_FLT
            important_impulse = None
            for a_impulse in in_impulses:
                if a_impulse['delay'] < min_delay:
                    important_impulse = a_impulse
            return  {
                'strength': important_impulse['strength'],
                'delay': important_impulse['delay']
            }
        for result in results:
            model = TheoreticalOutdoorModel(result, tx_power_dbm=15)
            rev_power = model.calculate_max_received_power()
            impulses = model.calculate_signal_impulses()
            state = get_important_impulse(impulses)
            states.append(state)
            rec_power_list.append(rev_power)
            avg_rev_power += dBmTomW(rev_power)
        avg_rev_power /= len(result)
        return avg_rev_power, rec_power_list, states

    def step(self):
        self.simulation.update(1)
        self.update_result()
        self.avg_rec, self.rec_power_list, self.states = self.calculate_environment()

    def render(self):
        if is_notebook():
            print("should plot here")
        else:
            print("should run window here")

    def reset(self):
        self.simulation.cells = []
        self.simulation.pedestrians = []
        self.simulation.generate_equipment()

    def action(self, control):
        current_pos = self.simulation.cell_n[0].position

        if control['foward_x']:
            current_pos[0] += 1
        elif control['backward_x']:
            current_pos[0] -= 1
        elif control['forward_z']:
            current_pos[2] += 1
        elif control['backward_z']:
            current_pos[2] -= 1

        if self.simulation.tracer.is_outdoor(current_pos):
            self.simulation.cells[0].move(current_pos)

    def get_states(self):
        return self.states
        
    def get_reward(self):
        # TODO: [] Calculate reward

        pass

