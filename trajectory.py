from scipy.integrate import odeint as solve_ivp
from body import Bodies
import numpy as np
from math import sqrt

A = 1e-5 #km/s/s
G = (6.67e-11)*(1e-9) #km km km kg / s*s 
M = Bodies["sun"]._mass

def func(t,p):
    x, y, z, xdot, ydot, zdot = p

    R = (x**2 + y**2 + z**2)**1.5
    V = sqrt(xdot**2 + ydot**2 + zdot**2)

    xdt = xdot
    ydt = ydot
    zdt = zdot 

    xdotdt = A*xdot/V - G*M*x/R
    ydotdt = A*ydot/V - G*M*y/R
    zdotdt = A*zdot/V - G*M*z/R
    
    return( xdt, ydt, zdt, xdotdt, ydotdt, zdotdt )

def calculate_traj(times, pos_i, vel_i):
    pos_i/=1
    vel_i/=1

    times*= 60


    initial_state = (pos_i[0], pos_i[1], pos_i[2], vel_i[0], vel_i[1], vel_i[2])

    result = solve_ivp( func,initial_state, times, tfirst=True)
    return(result)
