from typing import Tuple
import numpy as np

class Transmitter:
    position: Tuple[float, float, float]
    transmit_power_dbm: float = 0

    def __init__(self, position: Tuple[float, float, float], transmit_power_dbm: float):
        self.position = position
        self.transmit_power_dbm = transmit_power_dbm

    def set_tx_power(self, transmit_power_dbm):
        self.transmit_power_dbm = transmit_power_dbm
