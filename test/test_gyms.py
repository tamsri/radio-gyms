import os
from unittest import TestCase
from radio_gyms.gyms import LocationGym
from time import time

POZNAN_SCENE_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestGyms(TestCase):
    def test_location_gym(self):
        gym = LocationGym(POZNAN_SCENE_PATH, ue_n = 11, generator_seed = 1232134123)
        start = time()
        print(f'avg_rec: {gym.calculate_avg_rec_power()} mW')
        end = time()
        print(f"takes {end-start} seconds")
