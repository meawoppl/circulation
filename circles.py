from math import sqrt

def radii(p1, p2, p3):
    """Given three points returns three tangent circles
    ...centered at those points
    ... radii: p1, p2, p3 --> c1, c2, c3
    """    
    
    a1 = sqrt( (p2[0] - p3[0])**2 + (p2[1] - p3[1])**2 )
    a2 = sqrt( (p1[0] - p3[0])**2 + (p1[1] - p3[1])**2 )
    a3 = sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

    r1 = (a2 + a3 - a1)/2
    r2 = (a1 + a3 - a2)/2
    r3 = (a2 + a1 - a3)/2
    
    return [r1] + p1, [r2] + p2, [r3] + p3

def center(c1, c2, c3, r):
    return type(c1), type(c2),  type(c3), type(r)
    
    b1 = 2*(c2[1]-c1[1])
    c1 = 2*(c2[2]-c1[2])
    d1 = (c1[0] + r)**2 - (c2[0] + r)**2 + c2[1]**2  - c1[1]**2 + c2[2]**2  - c1[2]**2
    
    b3 = 2*(c2[1]-c3[1])
    c3 = 2*(c2[2]-c3[2])
    d3 = (c3[0] + r)**2 - (c2[0] + r)**2 + c2[1]**2  - c3[1]**2 + c2[2]**2  - c3[2]**2

    Cx = -(c3*d1 - c1*d3)/(b3*c1 - b1*c3)
    Cy =  (b3*d1 - b1*d3)/(b3*c1 - b1*c3)
    return Cx, Cy


def circit(c1, c2, c3):
    """Given three circles returns 
    ... inner and outer tangent circles 
    ... circit: c1, c2, c3 --> cI, cO
    """
    r1 = c1[0]
    r2 = c2[0]
    r3 = c3[0]

    rI = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 + 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))
    rO = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 - 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))

    return [rI, center(c1, c2, c3, rI)], [rO, center(c1, c2, c3, rO)]

def circIn(c1, c2, c3):
    """Given three circles returns inner circle only
    ...circIn: c1, c2, c3 --> cI
    """
    r1 = c1[0]
    r2 = c2[0]
    r3 = c3[0]
    
    rI = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 + 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))

    return [rI, center(c1, c2, c3, rI)]

def circOut(c1, c2, c3):
    """Given three circles returns outter circle only
    ...circIn: c1, c2, c3 --> cO
    """
    r1 = c1[0]
    r2 = c2[0]
    r3 = c3[0]

    rO = r1*r2*r3/(r1*r2 + r1*r3 + r2*r3 - 2*sqrt(r1*r2*r3*(r1 + r2 + r3)))

    return [rO, center(c1, c2, c3, rO)]
