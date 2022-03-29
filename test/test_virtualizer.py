import os
from time import sleep
import numpy as np
from unittest import TestCase
from radio_gyms.visualizers import Window
from radio_gyms.engines.ray_tracer.tracer import Tracer
from radio_gyms.utils.converters import outdoor_traced_result_to_line as OutdoorResultToLines
from radio_gyms.simulations import OldtownWalk

POZNAN_OBJ_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestVirtualizer(TestCase):

    def test_result_display(self):
        return
        window = Window()
        tracer = Tracer(POZNAN_OBJ_PATH)
        tx_pos = np.array([0, 5, 0])
        lines = []
        for i in range(1):
            while True:
                rx_pos = (np.random.rand(3)*2-1)*100
                rx_pos[1] = 1.2
                if tracer.is_outdoor(rx_pos):
                    break
            result = tracer.trace_outdoor(tx_pos, rx_pos)
            lines = lines + OutdoorResultToLines(result, tx_pos, rx_pos)
        window.line_sets = lines
        window.load_obj_to_scene(POZNAN_OBJ_PATH)
        for i in range(1000):
            window.render()
            window.dispatch_events()
            print(i)

    def test_visual_oldtown(self):
        window = Window()
        window.load_obj_to_scene(POZNAN_OBJ_PATH)
        tracer = Tracer(POZNAN_OBJ_PATH, ref_max=1)
        simulation = OldtownWalk(tracer, 1, 5)
        for i in range(1000):
            simulation.update(3)
            results = simulation.get_results()
            window.line_sets = []
            for result in results:
                result_lines = OutdoorResultToLines(result, result['tx_pos'], result['rx_pos'])
                window.line_sets += result_lines
            window.render()
            window.dispatch_events()
