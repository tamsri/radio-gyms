import numpy as np

from numpy.typing import NDArray

from ..utils import VecNorm, VecDistance
from . import Receiver


class Pedestrian:
    receiver: Receiver = None
    position: NDArray = None
    speed = None
    destination = None
    walking = False

    def __init__(self, position, speed=1.4):
        self.position = np.array(position)
        self.speed = speed
        self.receiver = Receiver(position)

    def walk(self, delta_time):
        if not self.walking:
            return
        direction = VecNorm(self.destination - self.position)
        step_distance = self.speed * delta_time
        self.position = self.position + direction * step_distance
        self.receiver.position = self.position
        if VecDistance(self.position, self.destination) <= step_distance:
            self.walking = False
