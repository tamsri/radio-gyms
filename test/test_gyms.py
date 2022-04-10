import os
from unittest import TestCase
from radio_gyms.gyms import LocationGym
from radio_gyms.utils import mWTodBm
from time import time

POZNAN_SCENE_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestGyms(TestCase):
    def test_location_gym(self):
        gym = LocationGym(POZNAN_SCENE_PATH, ue_n = 10, generator_seed = 1232134123)
        for i in range(10):
            start = time()
            gym.step()
            reward = gym.get_reward()
            end = time()
            print(f'reward: {reward:.2f}, duration: {(end-start):.2f}s')
            gym.render()
            
