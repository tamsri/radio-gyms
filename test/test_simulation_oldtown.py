import os
from unittest import TestCase

from radio_gyms.engines import Tracer
from radio_gyms.simulations import OldtownWalk

POZNAN_OBJ_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestOldtownWalkSimulation(TestCase):
    def test_impulse(self):
        tracer = Tracer(POZNAN_OBJ_PATH)
        simulation = OldtownWalk(tracer, 1, 30)

        simulation.update(1)
        result = simulation.get_impulse_list()
        print(result)
