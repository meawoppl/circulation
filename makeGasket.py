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


iCount = 2
for i in range(iCount):
    newPoints = []
    newRadaii = []
    for (i0, i1, i2) in itertools.combinations(range(len(pointsList)), 3):
        p0, p1, p2 = pointsList[i0], pointsList[i1], pointsList[i2]
        r0, r1, r2 = radaiiList[i0], radaiiList[i1], radaiiList[i2]

        pB, pBr, pS, pSr = circit(p0, r0, p1, r1, p2, r2)

        newPoints += [pB,  pS]
        newRadaii += [pBr, pSr]

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

