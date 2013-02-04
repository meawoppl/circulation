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

startPointList = [[-1, -2], [0, 1], [1, -2]]
 
c0, c1, c2 = list(radii(*tuple(startPointList)))

# next: rewrite all with circles def as c = [r, px, py]
# rad = c[0] and coordinates of the center c[1] and c[2]
# latter adding c[3] to make a 3d gasket with spheres

def circulate(c0, c1, c2, depth):
    cList = [c0, c1, c2]

    if depth == 0:
        return c3

    new = []
    for circleA, circleB in itertools.combinations(cList, 2):
        cInner, cOuter = circit(circleA, circleB, c2)

        if circleA[0] * circleB[0] > 0:
            cNew = cInner
        else:
            cNew = cOuter

        result = circulate(circleA, circleB, cNew, depth-1)
        new += result
    return c3 + new

loops = 4

c3, c4 = circit(c0, c1, c2)

circleList = [c0, c1, c2] + circulate(c0, c1, c2, loops) # + circulate(c0, c1, c2, c3, loops)

w = 512
h = 512

# Make a pdf surface
surf =  cairo.PDFSurface(open("test.pdf", "w"), w, h)

# Get a context object
ctx = cairo.Context(surf)

lineWidth = 0.001
ctx.set_line_width(lineWidth)

# both center and scale are defined by biggest circle
# print '#3 center: ', plot[3], ', radius: ', rlot[3]
# scale here and center in draw step by shifting


# next: translate and scale the data not the context
biggestCircle = circleList[3]
biggestR = abs(biggestCircle[0])
ctx.translate(w/2, h/2)
ctx.scale(250/biggestR, 250/biggestR)

def drawCircle(ctx, c):
    ctx.save()
    ctx.move_to(c[1] - c[0], c[2])
    ctx.arc(c[1], c[2], c[0], -pi, pi)
    ctx.restore()
    ctx.stroke()
    
cnt = 0
with  open('circdata', 'w') as datafile:
    for c in circleList:
        if abs(c[0]) > lineWidth:
            drawCircle(ctx, abs(c[0]), c[1] - biggest[1], c[2] - biggest[2])
            cnt+=1
            datafile.write(str(abs(c[0])) + ", " + str(c[1] - biggest[1]) + ", " + str(pt[2] - biggest[2]) + "\n")

print cnt, '/', len(clot), ' circles in ', loops, ' loops.'
surf.finish()
