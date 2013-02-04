from math import sin, cos, pi
import cairo
from circles import radii, circit
import itertools

# """
# original
# """
# startPointList = []
# for i in range(3):
#     x = 2.5*cos(2.0 * pi * i / 3)
#     y = 2.5*sin(2.0 * pi * i / 3)

#     startPointList.append((x,y))

# """
# anomalus
# """
# startPointList = [(-2, 2), (0, 0), (2, 2)]

startPointList = [(-1, -2), (0, 1), (1, -2)]

startRadiiList = list(radii(*tuple(startPointList)))

def circulate(p0, r0, p1, r1, p2, r2, p3, r3, depth):
    pointList = [p0, p1, p2]
    radiiList = [r0, r1, r2]  

    if depth == 0:
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

loops = 3

p0, p1, p2 = startPointList
r0, r1, r2 = startRadiiList
p3, r3, p4, r4 = circit(p0, r0, p1, r1, p2, r2)

plot = [p0, p1, p2] + circulate(p0, r0, p1, r1, p2, r2, p4, r4, loops)[0] + circulate(p0, r0, p1, r1, p2, r2, p3, r3, loops)[0]

rlot = [r0, r1, r2] + circulate(p0, r0, p1, r1, p2, r2, p4, r4, loops)[1] + circulate(p0, r0, p1, r1, p2, r2, p3, r3, loops)[1]

# Make a pdf surface
surf =  cairo.PDFSurface(open("test.pdf", "w"), 512, 512)

# Get a context object
ctx = cairo.Context(surf)

width = 0.001
ctx.set_line_width(width)

# both center and scale are defined by biggest circle
# print '#3 center: ', plot[3], ', radius: ', rlot[3]
# scale here and center in draw step by shifting


# next: translate and scale the data not the context
biggestP = plot[3]
biggestR = abs(rlot[3])
ctx.translate(512/2, 512/2)
ctx.scale(250/biggestR, 250/biggestR)

def drawCircle(ctx, x, y, r):
    ctx.save()
    ctx.move_to(x-r, y)
    ctx.arc(x, y, r, -pi, pi)
    ctx.restore()
    ctx.stroke()
    
cnt = 0
with  open('circdata', 'w') as datafile:
    for pt, rad in zip(plot, rlot):
        if abs(rad) > width:
            drawCircle(ctx, pt[0] - biggestP[0], pt[1] - biggestP[1], abs(rad))
            cnt+=1
            datafile.write(str(pt[0] - biggestP[0]) + ", " + str(pt[1] - biggestP[1]) + ", " + str(abs(rad)) + "\n")

print cnt, '/', len(plot), ' circles in ', loops, ' loops.'
surf.finish()
