from typing import List, Tuple

import numpy as np

from ..utils import VecDistance, RefAngle, VecNorm, VecAngle, SortPointsFromPlaneY, dBmTomW, mWTodBm
from ..utils.constants import LIGHT_SPEED


class TheoreticalOutdoorModel:
    """
    Theoretical Outdoor model consist of free-space loss, reflection loss, and knife-edge diffraction.
    This theoretical outdoor model can be used for ultra-high frequency up to 100 GHz.

    The ray tracing result can be calculated for loss and signal propagation delay
    """
    result = None

    def __init__(self, result, tx_power_dbm: float):
        self.result = result
        self.tx_power_dBm = tx_power_dbm

    @staticmethod
    def calculate_free_space_loss(tx_pos, rx_pos, frequency, wave_speed=LIGHT_SPEED):
        tx_pos = np.array(tx_pos)
        rx_pos = np.array(rx_pos)
        distance = VecDistance(tx_pos, rx_pos)
        wave_length = wave_speed / frequency
        space_loss = (4 * np.pi * distance / wave_length) ** 2
        return 10 * np.log10(space_loss)

    @staticmethod
    def calculate_single_reflection_loss(tx_pos, rx_pos, ref_pos, frequency,
                                         tx_medium_permittivity=1,
                                         ref_medium_permittivity=5.31,
                                         polar='TM',
                                         wave_speed=LIGHT_SPEED):
        tx_pos = np.array(tx_pos)
        rx_pos = np.array(rx_pos)
        ref_pos = np.array(ref_pos)
        # calculate coefficient
        assert polar == 'TM' or polar == 'TE'

        angle_1 = RefAngle(tx_pos, ref_pos, rx_pos)
        angle_2 = np.arcsin(np.sqrt(tx_medium_permittivity) * np.sin(angle_1) / np.sqrt(ref_medium_permittivity))
        bias = np.sqrt(np.abs(tx_medium_permittivity / ref_medium_permittivity) * np.sin(angle_1))
        if bias >= 1:
            coefficient = 1
        else:
            sqrt_n1 = np.sqrt(tx_medium_permittivity)
            sqrt_n2 = np.sqrt(ref_medium_permittivity)
            cos_1 = np.cos(angle_1)
            cos_2 = np.cos(angle_2)
            if polar == 'TM':
                coefficient = (sqrt_n2 * cos_1 - sqrt_n1 * cos_2) / (sqrt_n2 * cos_1 + sqrt_n1 * cos_2)
            elif polar == 'TE':
                coefficient = (sqrt_n1 * cos_1 - sqrt_n2 * cos_2) / (sqrt_n1 * cos_1 + sqrt_n2 * cos_2)
            else:
                raise TypeError("invalid polar")
        # calculate loss
        distance = VecDistance(tx_pos, ref_pos) + VecDistance(ref_pos, rx_pos)
        wave_length = wave_speed / frequency
        loss = (4 * np.pi * distance / (coefficient * wave_length)) ** 2
        return 10 * np.log10(loss)

    @staticmethod
    def calculate_knife_edge_diffraction(tx_pos, rx_pos, frequency: float, edges: List, wave_speed=LIGHT_SPEED):
        tx_pos = np.array(tx_pos)
        rx_pos = np.array(rx_pos)
        edges = [np.array(edge) for edge in edges]

        def calculate_v(left_pos, right_pos, edge_pos):
            tx_to_rx_dir = VecNorm(right_pos - left_pos)
            rx_to_tx_dir = -tx_to_rx_dir
            tx_to_edge_dir = VecNorm(edge_pos - left_pos)
            rx_to_edge_dir = VecNorm(edge_pos - right_pos)
            angle_tx = VecAngle(tx_to_edge_dir, tx_to_rx_dir)
            angle_rx = VecAngle(rx_to_edge_dir, rx_to_tx_dir)
            wave_length = wave_speed / frequency
            r_1 = VecDistance(left_pos, edge_pos)
            r_2 = VecDistance(edge_pos, right_pos)
            s_1 = np.cos(angle_tx) * r_1
            s_2 = np.cos(angle_rx) * r_2
            h = np.sin(angle_tx) * r_1
            return h * np.sqrt((2 * (s_1 + s_2)) / (wave_length * r_1 * r_2))

        def calculate_c(v: float):
            return 6.9 + 20 * np.log10(np.sqrt((v - 0.1) ** 2 + 1) + v - 0.1)

        def calculate_correction(near_tx_pos, center_pos, near_rx_pos, near_tx_c_, center_c_, near_rx_c_):
            tx_pos_on_y = np.copy(tx_pos)
            tx_pos_on_y[1] = 0
            near_tx_on_y = np.copy(near_tx_pos)
            near_tx_on_y[1] = 0
            center_on_y = np.copy(center_pos)
            center_on_y[1] = 0
            near_rx_on_y = np.copy(near_rx_pos)
            near_rx_on_y[1] = 0
            rx_pos_on_y = np.copy(rx_pos)
            rx_pos_on_y[1] = 0
            d1 = VecDistance(tx_pos_on_y, near_tx_on_y)
            d2 = VecDistance(near_tx_on_y, center_on_y)
            d3 = VecDistance(center_on_y, near_rx_on_y)
            d4 = VecDistance(near_rx_on_y, rx_pos_on_y)

            cos_1 = np.sqrt((d1 * (d3 + d4)) / ((d1 + d2) * (d2 + d3 + d4)))
            cos_2 = np.sqrt((d4 * (d1 + d2)) / ((d3 + d4) * (d2 + d3 + d1)))

            correct_1 = (6 - center_c_ + near_tx_c_) * cos_1
            correct_2 = (6 - center_c_ + near_rx_c_) * cos_2
            return correct_1 + correct_2

        def sort_edge_by_v(unsorted_edges):
            return sorted(unsorted_edges, key=lambda edge: calculate_v(tx_pos, rx_pos, edge))

        def single_edge_loss(single_edge):
            v = calculate_v(tx_pos, rx_pos, single_edge)
            diff_loss = calculate_c(v)
            return diff_loss

        def double_edge_loss(double_edges):
            near_tx_edge_i = double_edges[0]
            near_tx_v_i = calculate_v(tx_pos, rx_pos, near_tx_edge_i)
            near_rx_edge_i = double_edges[1]
            near_rx_v_i = calculate_v(tx_pos, rx_pos, near_rx_edge_i)
            if near_tx_v_i > near_rx_v_i:
                main_c = calculate_c(near_tx_v_i)
                support_c = calculate_c(calculate_v(near_tx_edge_i, rx_pos, near_rx_edge_i))
            else:
                main_c = calculate_c(near_rx_v_i)
                support_c = calculate_c(calculate_v(tx_pos, near_rx_edge_i, near_tx_edge_i))
            diff_loss = main_c + support_c
            return diff_loss

        def more_edge_loss(more_edges):
            if len(more_edges) == 3:
                near_tx_edge = sorted_edges[0]
                center_edge = sorted_edges[1]
                near_rx_edge = sorted_edges[2]
            else:
                top_edges = sort_edge_by_v(sorted_edges)[:3]
                sorted_top_edge = SortPointsFromPlaneY(tx_pos, top_edges)
                near_tx_edge = sorted_top_edge[0]
                center_edge = sorted_top_edge[1]
                near_rx_edge = sorted_edges[2]

            near_tx_v = calculate_v(tx_pos, rx_pos, near_tx_edge)
            center_v = calculate_v(tx_pos, rx_pos, center_edge)
            near_rx_v = calculate_v(tx_pos, rx_pos, near_rx_edge)
            max_v = min([near_tx_v, center_v, near_rx_v])
            if near_tx_v == max_v:
                main_c = calculate_c(near_tx_v)
                support_c_1 = calculate_c(calculate_v(near_tx_edge, near_rx_edge, center_edge))
                support_c_2 = calculate_c(calculate_v(center_edge, rx_pos, near_rx_edge))
            elif near_rx_v == max_v:
                main_c = calculate_c(near_rx_v)
                support_c_1 = calculate_c(calculate_v(tx_pos, center_edge, near_tx_edge))
                support_c_2 = calculate_c(calculate_v(near_tx_edge, near_rx_edge, center_edge))
            else:
                main_c = calculate_c(center_v)
                support_c_1 = calculate_c(calculate_v(tx_pos, center_edge, near_tx_edge))
                support_c_2 = calculate_c(calculate_v(center_edge, rx_pos, near_rx_edge))
            if np.isnan(support_c_1):
                support_c_1 = 0
            if np.isnan(support_c_2):
                support_c_2 = 0
            near_tx_c = calculate_c(near_tx_v)
            center_c = calculate_c(center_v)
            near_rx_c = calculate_c(near_rx_v)
            total_correct = calculate_correction(near_tx_edge, center_edge, near_rx_edge,
                                                 near_tx_c, center_c, near_rx_c)
            diff_loss = main_c + support_c_1 + support_c_2 - total_correct
            return diff_loss

        edge_n = len(edges)

        loss = TheoreticalOutdoorModel.calculate_free_space_loss(tx_pos, rx_pos, frequency, wave_speed)
        sorted_edges = SortPointsFromPlaneY(tx_pos, edges)
        if edge_n == 1:
            single_loss = single_edge_loss(edges[0])
            loss += single_loss
        elif edge_n == 2:
            loss += double_edge_loss(sorted_edges)
        elif edge_n >= 3:
            loss += more_edge_loss(sorted_edges)
        return loss

    def calculate_max_received_power(self, frequency: float = 2.4e9, wave_speed=LIGHT_SPEED) -> float:
        tx_pos = self.result['tx_pos']
        rx_pos = self.result['rx_pos']
        receive_power_dbms = []
        free_space_loss = TheoreticalOutdoorModel.calculate_free_space_loss(tx_pos, rx_pos,
                                                                            frequency, wave_speed)

        if self.result['direct']:
            receive_power_dbm = self.tx_power_dBm - free_space_loss
            receive_power_dbms.append(receive_power_dbm)
        else:
            knife_edges = self.result['roof_edges']
            diffraction_loss = TheoreticalOutdoorModel.calculate_knife_edge_diffraction(tx_pos,
                                                                                        rx_pos,
                                                                                        frequency,
                                                                                        knife_edges,
                                                                                        wave_speed)
            receive_power_dbm = self.tx_power_dBm - diffraction_loss
            receive_power_dbms.append(receive_power_dbm)

        for ref_pos in self.result['reflections']['single']:
            reflected_loss = TheoreticalOutdoorModel.calculate_single_reflection_loss(tx_pos,
                                                                                      rx_pos,
                                                                                      ref_pos,
                                                                                      frequency,
                                                                                      wave_speed=wave_speed)
            reflected_received_power_dbm = self.tx_power_dBm - reflected_loss
            receive_power_dbms.append(reflected_received_power_dbm)

        received_power_mw = 0
        for receive_power_dbm in receive_power_dbms:
            received_power_mw += dBmTomW(receive_power_dbm)
        return mWTodBm(received_power_mw)

    @staticmethod
    def calculate_signal_delay(tx_pos, rx_pos, points=[], wave_speed=LIGHT_SPEED):
        tx_pos = np.array(tx_pos)
        rx_pos = np.array(rx_pos)
        points = [np.array(point) for point in points]
        distance = 0
        if len(points) == 0:
            distance += VecDistance(tx_pos, rx_pos)
        else:
            left_pos = tx_pos
            for i in range(len(points)):
                right_pos = points[i]
                distance += VecDistance(left_pos, right_pos)
                left_pos = points[i]
            right_pos = rx_pos
            distance += VecDistance(left_pos, right_pos)
        delay = distance / wave_speed
        return delay

    def calculate_signal_impulses(self, freq: float = 2.4e9,
                                  wave_speed: float = LIGHT_SPEED) -> List[Tuple[float, float]]:
        impulses = []
        tx_pos = self.result['tx_pos']
        rx_pos = self.result['rx_pos']
        if self.result['direct']:
            rev_power_dbm = self.tx_power_dBm - self.calculate_free_space_loss(tx_pos, rx_pos, freq, wave_speed)
            rev_delay = self.calculate_signal_delay(tx_pos, rx_pos)
            impulse = {'strength': rev_power_dbm,
                       'delay': rev_delay}
            impulses.append(impulse)
        else:
            knife_edges = self.result['roof_edges']
            diffraction_loss = TheoreticalOutdoorModel.calculate_knife_edge_diffraction(tx_pos,
                                                                                        rx_pos,
                                                                                        freq,
                                                                                        knife_edges,
                                                                                        wave_speed=wave_speed)
            rev_power_dbm = self.tx_power_dBm - diffraction_loss
            rev_delay = self.calculate_signal_delay(tx_pos, rx_pos, knife_edges)
            impulse = {'strength': rev_power_dbm,
                       'delay': rev_delay}
            impulses.append(impulse)
        for ref_pos in self.result['reflections']['single']:
            reflected_loss = TheoreticalOutdoorModel.calculate_single_reflection_loss(tx_pos,
                                                                                      rx_pos,
                                                                                      ref_pos,
                                                                                      freq,
                                                                                      wave_speed=wave_speed)
            rev_power_dbm = self.tx_power_dBm - reflected_loss
            rev_delay = self.calculate_signal_delay(tx_pos, rx_pos, [ref_pos])
            impulse = {'strength': rev_power_dbm,
                       'delay': rev_delay}
            impulses.append(impulse)
        return impulses
