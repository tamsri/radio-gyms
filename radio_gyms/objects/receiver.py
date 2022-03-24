from typing import Tuple
import numpy as np


class Receiver:
    position: Tuple[float, float, float]

    def __init__(self, position):
        self.position = position
