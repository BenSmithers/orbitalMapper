from basic_gui import Window

from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QBrush, QColor

import sys
import json
import numpy as np
from math import pi, cos, sin

from body import Body
from projection import proj_angles

from MultiHex.clock import Time

class main_window(QMainWindow):
    """
    This is the main class for the window itself 
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)

        self.ui = Window()
        self.ui.setupUi(self)

        self.scene = Interface(self.ui.graphicsView)
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )
#        self.ui.graphicsView.

        f = open("objects.json",'r')
        data = json.load(f)
        f.close()

        self._bodies = {}
        for entry in data.keys():
            self._bodies[entry] = Body(data[entry], self._bodies) 
        
        
        self.pen = QPen()
        self.brush = QBrush()
        self.brush.setStyle(1)

        # R, zenith, azimuth 
        self._camera_pos = np.array([150e6, pi/2,pi/4])
        self.time = Time(minute = 12, hour=5, month=7,year=2300)

        self._drawn = {}

        self.root_size = (674/2, 560/2)
        self.update_figure()

        self._rot_scale=0.01

        self.ui.left.pressed.connect(self.button_left)
        self.ui.right.pressed.connect(self.button_right)
        self.ui.up.pressed.connect(self.button_tilt_f)
        self.ui.down.pressed.connect(self.button_tilt_b)

        self.ui.left.released.connect(self.button_release)
        self.ui.right.released.connect(self.button_release)
        self.ui.down.released.connect(self.button_release)
        self.ui.up.released.connect(self.button_release)

        self.timer = QTimer()
        self._counter = 0

    def button_release(self):
        self.timer.stop()

    def button_left(self):
        self.timer.timeout.connect(self.rot_left)
        self.timer_go()
    def button_right(self):
        self.timer.timeout.connect(self.rot_right)
        self.timer_go()
    def button_tilt_f(self):
        self.timer.timeout.connect(self.tilt_f)
        self.timer_go()
    def button_tilt_b(self):
        self.timer.timeout.connect(self.tilt_b)
        self.timer_go()

    def timer_go(self):
        self.counter = 0
        self.timer.start(10)

    def rot_left(self):
        self._camera_pos[2]-=self._rot_scale
        self.update_figure()
    def rot_right(self):
        self._camera_pos[2]+=self._rot_scale
        self.update_figure()
    def tilt_f(self):
        if self._camera_pos[1]>=0:
            self._camera_pos[1]-=self._rot_scale
        self.update_figure()
    def tilt_b(self):
        if self._camera_pos[1]<=pi:
            self._camera_pos[1]+=self._rot_scale
        self.update_figure()


    def update_figure(self):
        camera_cart = np.array([
                        self._camera_pos[0]*cos(self._camera_pos[2])*sin(self._camera_pos[1]),
                        self._camera_pos[0]*sin(self._camera_pos[2])*sin(self._camera_pos[1]),
                        self._camera_pos[0]*cos(self._camera_pos[1])
                        ])

        for entry in self._bodies.keys():
            planet = self._bodies[entry]
            loc = planet.get_pos(self.time)

            theta, phi = proj_angles(loc, camera_cart)

            phi -= pi 
        
           # print("{} Appears at: ".format(entry))
           # print("    {}".format(theta))
           # print("    {}".format(phi))

            self.pen.setColor(QColor(planet.color))
            self.brush.setColor(QColor(planet.color))
        
            x_pos = (phi/(3*pi/4)   - 1)*self.root_size[0]
            y_pos = (-theta/(pi/2) + 1)*self.root_size[1]

            if entry in self._drawn:
                self.scene.removeItem(self._drawn[entry])
            self._drawn[entry] = self.scene.addEllipse(x_pos, y_pos, planet.ms, planet.ms, self.pen, self.brush)

class Interface(QGraphicsScene):
    """
    This is the interaction interface 
    We process button presses and stuff like that 
    """
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.parent=parent
    
        primary = Qt.LeftButton
        secondary = Qt.RightButton

        
    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        print("x: {},y: {}".format(event.scenePos().x(), event.scenePos().y()))
        print(self.parent.width())
        print(self.parent.height())

    def mouseMoveEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        event.accept()
        print(event.key())

app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())
