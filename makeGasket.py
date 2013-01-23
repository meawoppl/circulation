from math import sin, cos, pi
import cairo
from circles import radia, circit

import itertools


pointList = []
for i in range(3):
    x = cos(2.0 * pi * i / 3)
    y = sin(2.0 * pi * i / 3)

    pointList.append((x,y))
    
radaiiList = list(radia(*tuple(pointList)))


def circulate(p0, r0, p1, r1, p2, r2, depth):
    pointList = [p0, p1, p2]
    radaiList = [r0, r1, r2]
    p3, r3, p4, r4 = circit(p0, r0, p1, r1, p2, r2)

    pointList += [p3, p4]
    radaiList += [r3, r4]
    
    if depth==0:
        return pointList, radaiList
    else:
        newPL = []
        newRL = []
        for indxs in itertools.combinations(range(3), 2):
            i0, i1 = indxs
            for i2 in [3, 4]:
                result = circulate(pointList[i0], radaiList[i0], 
                                   pointList[i1], radaiList[i1],
                                   pointList[i2], radaiList[i2], depth-1)
                newPL += result[0]
                newRL += result[1]
        return pointList+newPL, radaiList+newRL

pl, rl = circulate(pointList[0], radaiiList[0], 
                   pointList[1], radaiiList[1],
                   pointList[2], radaiiList[2],5)


# Make a pdf surface
surf =  cairo.PDFSurface(open("test.pdf", "w"), 512, 512)

# Get a context object
ctx = cairo.Context(surf)

ctx.set_line_width(0.0001)

ctx.translate(512/2, 512/2)
ctx.scale(50, 50)

def drawCircle(ctx, x, y, r):
    ctx.save()
    ctx.move_to(x-r, y)
    ctx.arc(x, y, r, -pi, pi)
    ctx.restore()
    ctx.stroke()
    
for pt, rad in zip(pl, rl):
    print pt, rad
    drawCircle(ctx, pt[0], pt[1], abs(rad))

surf.finish()

