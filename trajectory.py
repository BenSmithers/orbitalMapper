from scipy.integrate import odeint as solve_ivp
from body import Bodies
import numpy as np
from math import sqrt

from scipy.optimize import minimize

from cascade.utils import get_closest

A = 1e-4 #km/s/s
G = (6.67e-11)*(1e-9) #km km km kg / s*s 
M = Bodies["sun"]._mass

def get_cost(t_i, p_i, v_i, a_i, t_flip, a_f, t_max, body):
    """
    Given initial conditions, a pre-flip acceleration, a flip time, and a post-flip acceleration, calculate a "cost"

    The cost is a combination of physical displacement and relative velocities 
    """
    initial = np.linspace(0, t_flip, 30)
    print("flip {}".format(t_flip))
    print("max {}".format(t_max))

    mid = calculate_traj(initial, p_i, v_i, a_i)[-1]
    
    
    p_m = (mid[0], mid[1], mid[2])
    v_m = (mid[3], mid[4], mid[5])

    later = np.linspace(0, t_max-t_flip, 30)
    final = calculate_traj(later, p_m, v_m, a_f)

    def get_p_dif(time):
        t = time[0]
        diff = get_closest(t, later, final)[0:3] - Bodies[body].get_pos(float(t_i)+t)
        return sqrt(np.dot(diff, diff))

    t_min = minimize( get_p_dif, 0.5*(t_max-t_flip)).x[0] #measures time after flip

    return([get_closest(t_min, later, final), final])


def func(t,p, accel_vector):
    x, y, z, xdot, ydot, zdot = p

    R = (x**2 + y**2 + z**2)**1.5

    xdt = xdot
    ydt = ydot
    zdt = zdot 

    xdotdt = accel_vector[0] - G*M*x/R
    ydotdt = accel_vector[1] - G*M*y/R
    zdotdt = accel_vector[2] - G*M*z/R
    
    return( xdt, ydt, zdt, xdotdt, ydotdt, zdotdt )

def calculate_traj(t, pos_i, vel_i, av):

    times = t*60

    accel_vector=av*10*(1e-3)

    initial_state = (pos_i[0], pos_i[1], pos_i[2], vel_i[0], vel_i[1], vel_i[2])

    result = solve_ivp(lambda t,p: func(t,p, accel_vector), initial_state, times, tfirst=True)
    return(result)


