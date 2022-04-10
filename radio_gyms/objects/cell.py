from numpy.typing import NDArray
from . import Transmitter


class Cell:
    transmitter: Transmitter = None
    position: NDArray = None

    def __init__(self, position, transmit_power):
        self.position = position
        self.transmitter = Transmitter(position, transmit_power)
    
    def move(self, pos):
        self.position = pos
        self.transmitter.position = pos
