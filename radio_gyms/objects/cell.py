from numpy.typing import NDArray
from . import Transmitter


class Cell:
    transmitter: Transmitter = None
    position: NDArray = None

    def __init__(self, position, transmit_power):
        self.transmitter = Transmitter(position, transmit_power)
