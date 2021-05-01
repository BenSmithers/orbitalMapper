from basic_gui import Window

from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QBrush, QColor

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt 

import sys
import numpy as np
from math import pi, cos, sin, sqrt

from body import Bodies
from projection import proj_angles

from MultiHex.clock import Time
from trajectory import calculate_traj, get_cost

import time

class main_window(QMainWindow):
    """
    This is the main class for the window itself 
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)

        self.ui = Window()
        self.ui.setupUi(self)

        #self.scene = Interface(self.ui.graphicsView)
        #self.ui.graphicsView.setMouseTracking(True)
        #self.ui.graphicsView.setScene( self.scene )

        
        self._bodies = Bodies
        for entry in Bodies.keys():
            self.ui.focusSelect.addItem(str(entry)) 

        # R, zenith, azimuth 
        self.time = Time(minute = 12, hour=5, month=11,year=2300)

        self.scale = 1.5e8

        self.update_figure()

        self.ui.focusSelect.currentIndexChanged.connect(self.update_figure)

    def update_figure(self):
        foc = self.ui.focusSelect.currentText()
        focus_point = self._bodies[foc].get_pos(float(self.time))

        previous = np.linspace(0,20, 30)
        focus_trail = np.transpose([self._bodies[foc].get_pos(float(self.time -Time(day=dbefore))) for dbefore in previous])

        self.scale = self._bodies[foc].f_scale

        self.ui.ax.clear()
        for entry in self._bodies.keys():
            planet = self._bodies[entry]
            loc = planet.get_pos(float(self.time)) - focus_point

            self.ui.ax.plot(loc[0], loc[1], ms=planet.ms,marker="o", color=planet.color)

            if foc == planet._parent:
                places = np.transpose([planet.get_pos(float(self.time-Time(day=dbefore))) for dbefore in previous]) - focus_trail            
                self.ui.ax.plot(places[0], places[1], color=planet.color, ls='--')

 
        self.ui.ax.set(facecolor='k')

        self.ui.ax.set_xlim([-self.scale,self.scale])
        self.ui.ax.set_ylim([-self.scale,self.scale])
        
        print("integrate!")
        start = time.time()
        p_earth = self._bodies["earth"].get_pos(self.time)
        v_earth = self._bodies["earth"].approx_v(self.time)

        a_vec = self._bodies["mercury"].get_pos(self.time)-p_earth
        a_vec *= (1e-2)/sqrt(np.dot(a_vec,a_vec))

        times = np.linspace(0 , 50, 30)*24*60 # in minutes! 
        traj = calculate_traj(times, p_earth,v_earth, a_vec) 
        end = time.time()
        print("Took {} seconds".format(end-start))
        
        traj = np.transpose(traj)
        self.ui.ax.plot(traj[0], traj[1], color="white", ls='--')

        close = get_cost(float(self.time), p_earth, v_earth, a_vec, times[5], -a_vec, times[-1], "mercury")
        #print(close)       
        #close = np.transpose(close)
        self.ui.ax.plot(close[0][0], close[0][1], color="pink", marker='o')
        traj = np.transpose(close[1])
        self.ui.ax.plot(traj[0], traj[1], color='pink', ls='--')


app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    app_instance.show()
    sys.exit(app.exec_())
