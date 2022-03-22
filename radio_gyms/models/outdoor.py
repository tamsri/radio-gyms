from typing import List, Tuple

class TheoreticalOutdoorModel:
    """
    Theoretical Outdoor model consist of free-space loss, reflection loss, and knife-edge diffraction.
    This theoretical outdoor model can be used for ultra-high frequency up to 100 GHz.

    The ray tracing result can be calculated for loss and signal propagation delay
    """
    result = None

    def __init__(self, result):
        self.result = result

    def calculatePropagationLoss(self) -> float:
        pass

    def calculatePropagationLoss(self) -> List[Tuple[float, float]]:
        pass