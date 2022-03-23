from unittest import TestCase
from radio_gyms.models import TheoreticalOutdoorModel as model


class TestModelOutdoor(TestCase):
    def test_free_space_loss(self):
        wave_speed = 3e8
        test_set = [
            {'tx':  [0, 5, 0], 'rx': [34, 1.5, -59], 'freq': 2.3e9, 'expect': 76.35},
            {'tx': [0, 5, 0], 'rx': [24, 1.5, 0], 'freq': 2.3e9, 'expect': 67.3719},
            {'tx': [0, 5, 0], 'rx': [42, 1.5, -9], 'freq': 2.3e9, 'expect': 72.3650},
            {'tx': [0, 5, 0], 'rx': [-5, 1.5, 16], 'freq': 2.3e9, 'expect': 64.3487}
        ]
        for test in test_set:
            calculated_loss_db = model.calculate_free_space_loss(test['tx'], test['rx'],
                                                                 test['freq'], wave_speed)
            self.assertAlmostEqual(test['expect'], calculated_loss_db, 2)

    def test_reflection_loss(self):
        wave_speed = 3e8
        freq = 2.3e9
        test_set = [
            {'tx': [0, 5, 0], 'rx': [34, 1.5, -59],
             'ref': [36.1217, 2.834910, -30.0909],
             'polar': 'TE',
             'freq': freq,
             'expect': 81.093},
            {'tx': [0, 5, 0], 'rx': [34, 1.5, -59],
             'ref': [26.1838, 0.010512, -45.4366],
             'polar': 'TE',
             'freq': freq,
             'expect': 77.170},
            {'tx': [0, 5, 0], 'rx': [24, 1.5, 0],
             'ref': [64.1040, 2.846930, 0.0000],
             'polar': 'TE',
             'freq': freq,
             'expect': 88.1103}
        ]
        for test in test_set:
            ref_loss_db = model.calculate_single_reflection_loss(test['tx'], test['rx'],
                                                                 test['ref'], test['freq'],
                                                                 tx_medium_permittivity=1.0003,
                                                                 ref_medium_permittivity=5.3,
                                                                 wave_speed=wave_speed, polar=test['polar'])
            self.assertAlmostEqual(test['expect'], ref_loss_db, 1)