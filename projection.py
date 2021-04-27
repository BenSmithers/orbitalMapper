import numpy as np

from math import sqrt, acos

def magsq(arr):
    tot = 0.0
    for i in arr:
        tot += i**2
    return(tot)

def mag(arr):
    return sqrt(magsq(arr))

def project(point, normal):
    """
    We take a point (3-vector) 
    and a normal vector (3-vector)
    """

    if not isinstance(point, np.ndarray):
        raise TypeError("Want numby")
    if not isinstance(normal, np.ndarray):
        raise TypeError("Want numby")
    
    n_mag = mag(normal)

    d = np.dot(point, normal)/n_mag
    p = d*normal/n_mag

    return point - p

def proj_angles(point, camera):
    """
    Returns the angles (zenith, azimuth) that the camera
    will perceive a point. 

    Positions are in cartesian, heliocentric system 
    """
    
    if not isinstance(point, np.ndarray):
        raise TypeError("Want numby")
    if not isinstance(camera, np.ndarray):
        raise TypeError("Want numby")
 

    p_minus_c = point - camera

    c_mag = mag(camera)

    pmc_mag = mag(p_minus_c)

    phi = acos(np.dot(p_minus_c, -camera)/(pmc_mag*c_mag))
    theta = acos( np.dot(p_minus_c, (0,0,1))/pmc_mag)

    return(theta,phi)
