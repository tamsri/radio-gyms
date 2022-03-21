from unittest import TestCase
from radio_gyms.visualizers.window import VisualizerWindow

class TestVirtualizer(TestCase):

    def test_window(self):
        window = VisualizerWindow()
        line = { 'points': [ [0, 15, 0],
                            [-70.80, 7.04, 15.22],
                            [-30, 1.5, 45] ],
                 'color': [1, 0, 0, 1]}
        window.line_sets.append(line)
        window.run()

    def test_result_display(self):
        pass