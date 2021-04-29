from orbit import Orbit
from math import log10
import json

class Body(Orbit):
    def __init__(self, json_entry, planet_list):
        Orbit.__init__(self, json_entry, planet_list)
        
        json_entry = json_entry["props"]
        self._designation = json_entry["designation"]
        self._mass = json_entry["mass"]
        self._radius = json_entry["radius"]
        self._rot_period = json_entry["period"]
        self._tilt = json_entry["tilt"]
        self._color = json_entry["color"]
        self.f_scale = json_entry["f_scale"]

    @property
    def color(self):
        return self._color

    @property
    def ms(self):
        value = 5*pow(1.5,log10(self._mass/(5.97e24))) 

        return value

f = open("objects.json",'r')
data = json.load(f)
f.close()

print("Constructing Bodies")
Bodies = {}
for entry in data.keys():
    Bodies[entry] = Body(data[entry], Bodies)
print("Done!")
