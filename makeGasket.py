from math import sin, cos, pi
import cairo
from circles import radia, circit

import itertools


pointsList = []
for i in range(3):
    x = cos(2.0 * pi * i / 3)
    y = sin(2.0 * pi * i / 3)

    pointsList.append((x,y))
    
radaiiList = list(radia(*tuple(pointsList)))


print pointsList


iCount = 1
for i in range(iCount):

    newPoints = []
    newRadaii = []
    for p1, p2, p3 in itertools.combinations(pointsList, 3):
        pinner, pir, pouter, por = circit(p1, p2, p3)

        newPoints += [pinner,  pouter]
        newRadaii += [abs(pir), abs(por)]

    pointsList += newPoints
    radaiiList += newRadaii


# Make a pdf surface
surf =  cairo.PDFSurface(open("test.pdf", "w"), 512, 512)

# Get a context object
ctx = cairo.Context(surf)

ctx.set_line_width(0.01)

ctx.translate(512/2, 512/2)
ctx.scale(50, 50)

def drawCircle(ctx, x, y, r):
    ctx.save()
    ctx.move_to(x-r, y)
    ctx.arc(x, y, r, -pi, pi)
    ctx.restore()
    ctx.stroke()
    
for pt, rad in zip(pointsList, radaiiList):
    print pt, rad
    drawCircle(ctx, pt[0], pt[1], rad)

surf.finish()

