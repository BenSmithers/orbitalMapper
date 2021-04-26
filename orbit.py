from MultiHex.clock import Time, minutes_in_day
from MultiHex.core import Point3d as Point

from scipy.optimize import root
from math import sqrt, sin, cos,tan, pi, atan2, atan
import numpy as np

mu_sun = 1.327124e20

class Orbit:
    def __init__(self, json_entry, planet_list):
        if not isinstance(json_entry, dict):
            raise TypeError("Expected {}, got {}".format(dict, type(json_entry)))

        self._planet_list = planet_list

        json_entry = json_entry["orbit"]

        self._e = json_entry["eccentricity"] #unitless
        self._roote = sqrt(1-self._e**2)
        self._one_minus_e = sqrt(1-self._e)
        self._one_plus_e = sqrt(1+self._e)

        self._semimajor = json_entry["semimajor"] #km
        self._shift = self._e*self._semimajor

        self._inclination = json_entry["inclination"]*pi/180 #rad 
        self._rot_incl = np.array([[1,0,0],
                            [0,cos(self._inclination),-sin(self._inclination)],
                            [0,sin(self._inclination),cos(self._inclination)]])

        self._long = json_entry["long"]*pi/180
        self._rot_long = np.array([[cos(self._long), sin(self._long), 0],
                                [-sin(self._long), cos(self._long),0],
                                [0,0,1]])

        self._parent = json_entry["parent"] #string
        self._period = json_entry["period"] #days
        self._phase = 0.0*pi/180.

        self._b = self._semimajor*sqrt(1-self._e**2) # semiminor 
        self._foci_shift = sqrt(self._semimajor**2 - self._b**2)


        self._mean_motion =(2*pi/self._period) # radians

        self._cached_E = None
        self._cached_theta = None

    def _eccentric(self, mean, E):
        return mean - E + self._e*sin(E) 

    def get_pos(self, time):
        if not isinstance(time, (Time, int, float)):
            raise TypeError("Needed {}, got {}".format(Time, type(time)))

        t = float(time) #/minutes_in_day  # orbits are done in days, not minutesi
        while t>self._period:
            t -= self._period

        mean_anomaly = t*self._mean_motion # time since perihelion 
        
        # find E that minimuzes the zero 
        start = self._cached_E if (self._cached_E is not None) else 0.0
        
        
        result = root(lambda E:self._eccentric(mean_anomaly, E), start, method="broyden1")
        
        if not result.success:
            raise Exception("Failured to solve for eccentric anomaly")
        ecc_anom = result.x
        self._cached_E = ecc_anom
        
       
        theta = atan2( cos(ecc_anom)-self._e, self._roote*sin(ecc_anom)) + self._phase
        radius = self._semimajor*(1-self._e*cos(ecc_anom))
        
        point = np.array([radius*cos(theta),
                 radius*sin(theta),
                 0.0 ])

        #rotate about x-axis (inclination)
        point = np.matmul(self._rot_incl, point)

        #rotate about z-axis (opening in whichever direction)
        point = np.matmul(self._rot_long, point)
       
        if self._parent != "":
            point += self._planet_list[self._parent].get_pos(time)

        return tuple(point) #x,y,z
        
