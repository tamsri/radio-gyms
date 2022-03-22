from typing import List


def outdoor_traced_result_to_line(result, tx_pos, rx_pos) -> List[List]:
    lines = []
    if result['direct']:
        line = {'points': [tx_pos, rx_pos], 'color': [0, 0.8, 0, 1]}
        lines.append(line)
    else:
        if len(result['roof_edges']) > 0:
            line = {'points': [tx_pos] + result['roof_edges'] + [rx_pos], 'color': [0.2, 0.2, 0.2, 1]}
            lines.append(line)


    if 'reflections' in result:
        if 'single' in result['reflections']:
            for reflect_point in result['reflections']['single']:
                line = {'points': [tx_pos, reflect_point, rx_pos], 'color': [0, 0, 0.7, 1.0]}
                # lines.append(line)
        if 'double' in result['reflections']:
            for reflect_points in result['reflections']['double']:
                line = {'points': [tx_pos] + reflect_points + [rx_pos], 'color': [0.2, 0, 0.75, 1.0]}
                lines.append(line)
    return lines
