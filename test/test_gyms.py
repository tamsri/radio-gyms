import os
from unittest import TestCase
from radio_gyms.gyms import LocationGym
from radio_gyms.utils import mWTodBm
from time import time

POZNAN_SCENE_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestGyms(TestCase):
    def test_location_gym(self):
        gym = LocationGym(POZNAN_SCENE_PATH, ue_n = 100, generator_seed = 1232134123)
        start = time()
        gym.step()
        avg_rec = gym.avg_rec
        states = gym.states
        print(f'avg_rec: {avg_rec} mW')
        print(f'avg_rec: {mWTodBm(avg_rec)} dBm')
        print(f'state: {states[0]}')
        end = time()
        print(f"takes {end-start} secs")
