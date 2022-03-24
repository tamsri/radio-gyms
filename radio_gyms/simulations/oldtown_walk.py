import numpy as np

from typing import List

from ..engines import Tracer
from ..objects import Pedestrian, Cell
from ..models import TheoreticalOutdoorModel as OutdoorModel

class OldtownWalk:
    tracer: Tracer = None
    cells: List[Cell] = []
    pedestrians: List[Pedestrian] = []
    step: int = 0

    def __init__(self, tracer, cell_n, pedestrian_n):
        self.step = 0
        self.tracer = tracer
        self.pedestrian_position_limit = {
            'min_x': tracer.min_bound[0],
            'max_x': tracer.max_bound[0],
            'min_y': 0.5,
            'max_y': 1.8,
            'min_z': tracer.min_bound[2],
            'max_z': tracer.max_bound[2],
        }
        self.cell_position_limit = {
            'min_x': tracer.min_bound[0],
            'max_x': tracer.max_bound[0],
            'min_y': 2,
            'max_y': tracer.max_bound[1],
            'min_z': tracer.min_bound[2],
            'max_z': tracer.max_bound[2],
            'min_tx': 15,
            'max_tx': 20
        }
        self.cells, self.pedestrians = [], []
        self.generate_cell_randomly(pedestrian_n)
        self.generate_pedestrian_randomly(cell_n)

    def generate_cell_randomly(self, cell_n):
        for i in range(cell_n):
            position = self.random_outdoor_position(self.cell_position_limit)
            tx_power = np.random.uniform(low=self.cell_position_limit['min_tx'],
                                         high=self.cell_position_limit['max_tx'], size=1)[0]
            cell = Cell(position, tx_power)
            self.cells.append(cell)

    def generate_pedestrian_randomly(self, pedestrian_n):
        for i in range(pedestrian_n):
            position = self.random_outdoor_position(self.pedestrian_position_limit)
            pedestrian = Pedestrian(position)
            self.pedestrians.append(pedestrian)

    def random_outdoor_position(self, limit):
        outdoor = False
        while not outdoor:
            random_x = np.random.uniform(low=limit['min_x'],
                                         high=limit['max_x'], size=1)[0]
            random_y = np.random.uniform(low=limit['min_y'],
                                         high=limit['max_y'], size=1)[0]
            random_z = np.random.uniform(low=limit['min_z'],
                                         high=limit['max_z'], size=1)[0]
            new_position = np.array([random_x, random_y, random_z])
            if self.tracer.is_outdoor(new_position):
                outdoor = True
        return new_position

    def repurpose_pedestrian(self):
        for pedestrian in self.pedestrians:
            if not pedestrian.walking:
                found = False
                try_count = 0
                while not found:
                    try_count += 1
                    new_destination = self.random_outdoor_position(self.pedestrian_position_limit)
                    if self.tracer.direct_path(pedestrian.position, new_destination):
                        pedestrian.destination = new_destination
                        found = True
        return

    def update(self, delta_time):
        for pedestrian in self.pedestrians:
            pedestrian.walk(delta_time)

    def get_impulse_list(self):
        cell_results = []
        for cell_id, cell in enumerate(self.cells):
            tx_pos = cell.transmitter.position
            cell_result = {
                'id': cell_id,
                'pedestrians': []
            }
            for pedestrian_id, pedestrian in enumerate(self.pedestrians):
                rx_pos = pedestrian.receiver.position
                traced_result = self.tracer.trace_outdoor(tx_pos, rx_pos)
                model = OutdoorModel(traced_result, cell.transmitter.transmit_power_dbm)
                impulses = model.calculate_signal_impulses()
                max_rev_power = model.calculate_max_received_power()
                pedestrian_result = {
                    'id': pedestrian_id,
                    'impulses': impulses,
                    'rev_power': max_rev_power
                }
                cell_result['pedestrians'].append(pedestrian_result)
            cell_results.append(cell_result)
        return cell_results