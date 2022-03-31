from ..utils.constants import LIGHT_SPEED

class HataOkumuraModel:
    def __init__(self, result, tx_power_dbm: float):
        self.result = result
        pass

    @staticmethod
    def calculate_loss(tx_pos, rx_pos, line_of_sight: bool , frequency: float, wave_speed=LIGHT_SPEED):
        pass

    def calculate_receiving_power_dbm(self):
        pass