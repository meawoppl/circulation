import math
from math import sqrt

def radia(p1, p2, p3):
    """Given three points returns three radia
    """    
    
    a1 = math.sqrt( (p2[0] - p3[0])**2 + (p2[1] - p3[1])**2 )
    a2 = math.sqrt( (p1[0] - p3[0])**2 + (p1[1] - p3[1])**2 )
    a3 = math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

    r1 = (a2 + a3 - a1)/2
    r2 = (a1 + a3 - a2)/2
    r3 = (a2 + a1 - a3)/2
    
    return r1, r2, r3


def circit(p1, r1, p2, r2, p3, r3):
    """Given three points returns center[x], center[y], radius for 
    ... inner and outer circles respectively
    """
    
    r4inner = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 + 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))
    r4outer = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 - 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))

    def center(r4):
        
        b1 = 2*(p2[0]-p1[0])
        c1 = 2*(p2[1]-p1[1])
        d1 = (r1 + r4)**2 - (r2 + r4)**2 + p2[0]**2  - p1[0]**2 + p2[1]**2  - p1[1]**2

        b3 = 2*(p2[0]-p3[0])
        c3 = 2*(p2[1]-p3[1])
        d3 = (r3 + r4)**2 - (r2 + r4)**2 + p2[0]**2  - p3[0]**2 + p2[1]**2  - p3[1]**2

        Cx = -(c3*d1 - c1*d3)/(b3*c1 - b1*c3)
        Cy =  (b3*d1 - b1*d3)/(b3*c1 - b1*c3)
        return Cx, Cy

    return center(r4inner), r4inner, center(r4outer), r4outer
