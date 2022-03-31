import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, min_bound, max_bound, terrain_map=None):
        self.terrain_map = terrain_map
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.rx_pos = []
        self.tx_pos = []
        self.lines = []

    def render_top(self):
        x_min, x_max = self.min_bound[0], self.max_bound[0]
        z_min, z_max = self.min_bound[2], self.max_bound[2]
        assert x_min < x_max
        assert z_min < z_max
        if self.terrain_map is not None:
            display_map = self.terrain_map.pivot('x', 'z', 'height')
            display_map = display_map.T
            plt.imshow(display_map, cmap='inferno', interpolation='nearest', extent=[x_min, x_max,
                                                                                     z_min, z_max])
            plt.colorbar()
            plt.axis('off')
        rx_x = []
        rx_z = []
        tx_x = []
        tx_z = []
        for rx in self.rx_pos:
            rx_x.append(rx[0])
            rx_z.append(rx[2] * -1)
        for tx in self.tx_pos:
            tx_x.append(tx[0])
            tx_z.append(tx[2] * -1)
        for line in self.lines:
            color = line['color']
            points = line['points']
            first_point = points[0]
            for line_point in points[1:]:
                second_point = line_point
                x_1, z_1 = first_point[0], first_point[2] * -1
                x_2, z_2 = second_point[0], second_point[2] * -1
                plt.plot([x_1, x_2], [z_1, z_2], color=color)

                first_point = line_point
        plt.scatter(rx_x, rx_z, c='blue')
        plt.scatter(tx_x, tx_z, c='red')
        plt.xlim(x_min, x_max)
        plt.ylim(z_min, z_max)
        plt.show()

    @staticmethod
    def load_scene(scene_path: str):
        pass

    @staticmethod
    def load_result(self, result):
        pass

    @staticmethod
    def display_scene_top(data_frame):
        display_map = data_frame.pivot('x', 'z', 'height')
        display_map = display_map.T
        plt.imshow(display_map, cmap='inferno', interpolation='nearest')
        plt.colorbar()
        plt.axis('off')
