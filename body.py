from orbit import Orbit
from math import log10

class Body(Orbit):
    def __init__(self, json_entry, planet_list):
        Orbit.__init__(self, json_entry, planet_list)
        
        json_entry = json_entry["props"]
        self._designation = json_entry["designation"]
        self._mass = json_entry["mass"]
        self._radius = json_entry["radius"]
        self._rot_period = json_entry["period"]
        self._tile = json_entry["tilt"]
        self._color = json_entry["color"]
    @property
    def color(self):
        return self._color

    @property
    def ms(self):
        value = 10*pow(2,log10(self._mass/(5.97e24))) 

        return value
