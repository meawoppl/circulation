from math import sin, cos, pi
import cairo
from circles import radii, circit
import itertools


startPointList = []
for i in range(3):
    x = cos(2.0 * pi * i / 3)
    y = sin(2.0 * pi * i / 3)

    startPointList.append((x,y))
    
startRadiiList = list(radii(*tuple(startPointList)))


def circulate(p0, r0, p1, r1, p2, r2, p3, r3, depth):
    pointList = [p0, p1, p2]
    radiiList = [r0, r1, r2]  

    if depth==0:
        return [p3], [r3]
    else:
        newPL = []
        newRL = []
        for indxs in itertools.combinations(range(3), 2):
            i0, i1 = indxs
            pI, rI, pO, rO = circit(pointList[i0], radiiList[i0], 
                                    pointList[i1], radiiList[i1],
                                    p3, r3)

            if radiiList[i0]*radiiList[i1]*r3 > 0:
                pNew, rNew = pI, rI
            else:
                pNew, rNew = pO, rO
            result = circulate(pointList[i0], radiiList[i0], 
                               pointList[i1], radiiList[i1],
                               p3, r3, pNew, rNew, depth-1)
            newPL += result[0]
            newRL += result[1]
        return [p3]+newPL, [r3]+newRL

loops = 8

p0, p1, p2 = startPointList
r0, r1, r2 = startRadiiList
p3, r3, p4, r4 = circit(p0, r0, p1, r1, p2, r2)

plot = [p0, p1, p2] + circulate(p0, r0, p1, r1, p2, r2, p3, r3, loops)[0] + circulate(p0, r0, p1, r1, p2, r2, p4, r4, loops)[0]

rlot = [r0, r1, r2] + circulate(p0, r0, p1, r1, p2, r2, p3, r3, loops)[1]  + circulate(p0, r0, p1, r1, p2, r2, p4, r4, loops)[1]

print len(plot), ' circles in ', loops, ' loops.'

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
    
for pt, rad in zip(plot, rlot):
    drawCircle(ctx, pt[0], pt[1], abs(rad))

surf.finish()

