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

    def test_single_diffraction_loss(self):
        wave_speed = 3e8
        freq = 2.3e9
        test_set = [
            {
                'tx': [0,5,	0],
                'rx': [62, 1.5, -22],
                'freq': freq,
                'edge': [49.2605, 32.1573, -17.4795],
                'expect': 115.540
            },
            {
                'tx': [0, 5, 0],
                'rx': [45, 1.5, -36	],
                'freq': freq,
                'edge': [35.3552, 26.6196, -28.2842],
                'expect': 113.503
            },
            {
                'tx': [0, 5, 0],
                'rx': [61, 1.5, -19],
                'freq': freq,
                'edge': [51.8878, 31.8698, -16.1618],
                'expect': 115.229
            },
        ]
        for test in test_set:
            tx_pos = test['tx']
            rx_pos = test['rx']
            wave_freq = test['freq']
            edges = [test['edge']]
            expected_loss = test['expect']
            total_loss_db = model.calculate_knife_edge_diffraction(tx_pos, rx_pos,
                                                                   wave_freq, edges,
                                                                   wave_speed=wave_speed)
            self.assertAlmostEqual(expected_loss, total_loss_db, 2)

    def test_double_diffraction_loss(self):
        wave_speed = 3e8
        freq = 2.3e9
        test_set = [
            {
                'tx': [0, 5, 0],
                'rx': [20, 1.5, 0],
                'freq': freq,
                'edge': [
                    [10, 7, 0],
                    [15, 10, 0],
                ],
                'expect': 120.261
            },
        ]
        for test in test_set:
            tx_pos = test['tx']
            rx_pos = test['rx']
            wave_freq = test['freq']
            edges = test['edge']
            expected_loss = test['expect']
            total_loss_db = model.calculate_knife_edge_diffraction(tx_pos, rx_pos,
                                                                   wave_freq, edges,
                                                                   wave_speed=wave_speed)
            single_edge_loss = model.calculate_knife_edge_diffraction(tx_pos, rx_pos,
                                                                      wave_freq, [edges[0]],
                                                                      wave_speed=wave_speed)
            self.assertGreater(total_loss_db, single_edge_loss)
            self.assertAlmostEqual(expected_loss, total_loss_db, 2)

    def test_triple_diffraction_loss(self):
        wave_speed = 3e8
        freq = 2.3e9
        test_set = [
            {
                'tx': [0, 5, 0],
                'rx': [30, 1.5, 0],
                'freq': freq,
                'edge': [
                            [10, 7, 0],
                            [15, 10, 0],
                            [20, 7, 0]
                         ],
                'expect': 130.51
            },
        ]
        for test in test_set:
            tx_pos = test['tx']
            rx_pos = test['rx']
            edges = test['edge']
            freq = test['freq']
            expected_loss = test['expect']
            total_loss_db = model.calculate_knife_edge_diffraction(tx_pos, rx_pos,
                                                                   freq, edges,
                                                                   wave_speed=wave_speed)
            self.assertGreater(total_loss_db, 120.261)
            self.assertAlmostEqual(total_loss_db, expected_loss, 1)

    def test_signal_delay(self):
        test_set = [
            {
                'tx': [0, 0, 0],
                'rx': [0, 3e8, 0],
                'points': [],
                'expect': 1
            },
            {
                'tx': [0, 0, 0],
                'rx': [0, 6e8,0],
                'points': [[0, 3e8, 0], [0, 0e8, 0], [0, 3e8, 0]],
                'expect': 4
            }
        ]
        for test in test_set:
            tx_pos = test['tx']
            rx_pos = test['rx']
            points = test['points']
            expected = test['expect']
            delay = model.calculate_signal_delay(tx_pos, rx_pos, points, wave_speed=3e8)
            self.assertAlmostEqual(expected, delay, 0)