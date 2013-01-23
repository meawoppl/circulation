from math import sin, cos, pi
from cairo import *
import itertools


pointsList = []
for x in range(3):
    x = cos(2*pi / 3)
    y = sin(2*pi / 3)

    pointsList.append((x,y))
    

iCount = 1
for i in range(iCount):

    newPoints = []
    for p1, p2, p3 in itertools.permutations(pointsList, 3):
        newOutterPoint = outerCircle(p1, p2, p3)
        newInnerPoint  = innerCircle(p1, p2, p2)

        newPoints += [newOutterPoint, newInnerPoint]

    pointsList += newPoints



# Make a pdf surface
surf =  cairo.PDFSurface(open(filename, "w"), 512, 512)

# Get a context object
ctx = cairo.Context(surf)

for pt in pointsList:
    ctx.arc(pt[0], pt[1], 1, 0, 2*pi)
