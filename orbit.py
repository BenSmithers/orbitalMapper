from MultiHex.clock import Time, minutes_in_day
from MultiHex.core import Point3d as Point

from scipy.optimize import root
from math import sqrt, sin, cos,tan, pi, atan2

mu_sun = 1.327124e20

class orbit:
    def __init__(self, json_entry, planet_list):
        if not isinstance(json_entry, dict):
            raise TypeError("Expected {}, got {}".format(dict, type(json_entry)))

        self._e = json_entry["eccentricity"] #unitless
        self._roote = sqrt(1-self._e**2)

        self._semimajor = json_entry["semimajor"] #km
        self._shift = self._e*self._semimajor

        self._inclination = json_entry["inclination"] #deg 
        self._rot_incl = np.array([1,0,0],
                            [0,cos(self._inclination),-sin(self._inclination)],
                            [0,sin(self._inclination),cos(self._inclination)])

        self._long = json_entry["long"]+90  #deg 
        self._rot_long = np.array([cos(self._long), sin(self._long), 0],
                                [-sin(self._long), cos(self._long),0],
                                [0,0,1])

        self._parent = json_entry["parent"]
        self._period = json_entry["period"]
        self._phase = 0.0*pi/180.

        self._b = self._semimajor*sqrt(1-self._e**2) # semiminor 
        self._foci_shift = sqrt(self._semimajor**2 - self._b**2)


        self._mean_motion =(2*pi/self._period) # radians

        self._cached_E = None
        self._cached_theta = None

    def _eccentric(self, mean, E):
        return E - self._e*sin(E) - mean

    def _theta(self, theta, E):
        return ( (1-self._e)*tan(theta/2)**2 - (1+self._e)*tan(E/2)**2 )

    def get_pos(self, time):
        if not isinstance(time, (Time, int, float)):
            raise TypeError("Needed {}, got {}".format(Time, type(time)))

        t = float(time) / minutes_in_day # orbits are done in days, not minutes 
        while t>self._period:
            t -= self._period

        mean_anomaly = t*self._mean_motion # time since perihelion 

        # find E that minimuzes the zero 
        start = self._cached_E if (self._cached_E is not None) else self._e

        result = root(lambda E:self._eccentric(mean_anomaly, E),start)
        if not result.success:
            raise Exception("Failured to solve for true anomaly")
        ecc_anom = result.x
        self._cached_E = ecc_anom
        
       
        theta = atan2( cos(ecc_anom)-self._e, sqrt(1-self._e**2)*sin(ecc_anom)) + self._phase
        radius = self._semimajor*(1-self._e*cos(ecc_anom))
        
        point = (radius*cos(theta),
                 radius*sin(theta),
                 0.0 )

        #rotate about x-axis (inclination)
        point = np.matmul(self._rot_incl, point)

        #rotate about z-axis (opening in whichever direction)
        point = np.matmul(self._rot_long, point)
        
        return point
        
