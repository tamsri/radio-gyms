from pyglet.window import Window, key
from pyglet.gl import glClearColor, glBegin, glEnd, GL_LINE_STRIP,\
    glVertex3f, glColor4f, glLineWidth, glMatrixMode, GL_PROJECTION,\
    glLoadIdentity, gluPerspective, GL_MODELVIEW, glTranslatef, glRotatef,\
    glEnable, GL_DEPTH_TEST, glDrawArrays, GL_TRIANGLES, glPushMatrix

import logging
from pywavefront import visualization, Wavefront, configure_logging

configure_logging(
    logging.ERROR,
    formatter=logging.Formatter('%(name)s-%(levelname)s: %(message)s')
)

class VisualizerWindow(Window):
    camera_position = None
    camera_rotation = None
    window_size = None
    resizable = False
    scene = []
    objects = []
    alive = False
    pressed_keys = {}
    zoom = 0
    clear_color = (0,0,0,1)
    line_sets = []
    scenes = []
    def __init__(self, title = "Radio Gyms", window_size = (600, 400),
                 camera_position=[0 , 0, -255],
                 camera_rotation=[33, -230, 0],
                 resizable=True,
                 background_color=[0,0,0,1],
                 zoom = 66):

        self.window_size = window_size
        self.camera_position = camera_position
        self.camera_rotation = camera_rotation
        self.resizable = resizable
        self.alive = True
        self.pressed_keys = {}
        self.zoom = zoom
        self.clear_color = background_color
        self.line_sets = []
        self.scenes = []

        super().__init__(width=window_size[0],
                         height=window_size[1],
                         resizable = resizable,
                         caption = title,
                         style=Window.WINDOW_STYLE_DIALOG)
        glClearColor(0.9, 0.9, 0.875, 1)

    def load_icon(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.alive = False
        self.pressed_keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        try:
            del self.pressed_keys[symbol]
        except:
            pass

    def load_obj_to_scene(self, file_path):
        scene = Wavefront(file_path)
        self.scenes.append(scene)

    @staticmethod
    def draw_line(line_info):
        points = line_info['points']
        color = line_info['color']
        glBegin(GL_LINE_STRIP)
        glColor4f(*color)
        for point in points:
            glVertex3f(*point)
        glEnd()
        glLineWidth(2)

    def key_updates(self):
        if key.W in self.pressed_keys:
            self.camera_position[2] += 1
        if key.S in self.pressed_keys:
            self.camera_position[2] -= 1
        if key.A in self.pressed_keys:
            self.camera_position[0] += 1
        if key.D in self.pressed_keys:
            self.camera_position[0] -= 1
        if key.LSHIFT in self.pressed_keys:
            self.camera_position[1] += 1
        if key.LCTRL in self.pressed_keys:
            self.camera_position[1] -= 1
        if key.Z in self.pressed_keys:
            self.camera_rotation[0] += 1
        if key.X in self.pressed_keys:
            self.camera_rotation[0] -= 1
        if key.Q in self.pressed_keys:
            self.camera_rotation[1] += 1
        if key.E in self.pressed_keys:
            self.camera_rotation[1] -= 1

    def on_close(self):
        self.alive = False

    def on_draw(self):
        self.render()

    def render(self):
        self.clear()
        self.key_updates()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.zoom, self.window_size[0] /
                       float(self.window_size[1]), .1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glLoadIdentity()
        glTranslatef(*self.camera_position)
        glRotatef(self.camera_rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.camera_rotation[1], 0.0, 1.0, 0.0)
        glRotatef(self.camera_rotation[2], 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        for scene in self.scenes:
            visualization.draw(scene)
        for lineInfo in self.line_sets:
            self.draw_line(lineInfo)
        self.flip()

    def run(self):
        while self.alive:
            event = self.dispatch_events()
            self.render()