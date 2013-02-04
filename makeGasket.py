from math import sin, cos, pi
import cairo
from circles import radii, circit
import itertools

"""
original
"""
startPoints = list(range(3))
for i in startPoints:
    x = 2.5*cos(2.0 * pi * i / 3)
    y = 2.5*sin(2.0 * pi * i / 3)
    startPoints[i] = [x, y]

# """
# anomalus
# """
# startPoints = [[-2, 2], [0, 0], [2, 2]]

# """
# earhoops
# """
# startPoints = [[-1, -2], [0, 1], [1, -2]] 

# all circles are now defined as c = [r, px, py] with 
# radius = c[0] and coordinates of the center c[1] and c[2]
# latter adding c[3] to make a 3d gasket with spheres

def circulate(c0, c1, c2, c3, depth):
    cList = [c0, c1, c2]

    if depth == 0:
        return [c3]
    else:
        new = []
        for indxs in itertools.combinations(range(3), 2):
            i0, i1 = indxs
            cI, cO = circit(cList[i0], cList[i1], c3)

            if cList[i0][0]*cList[i1][0]*c3[0] > 0:
                cNew = cI
            else:
                cNew = cO

            result = circulate(cList[i0], cList[i1], 
                               c3, cNew, depth-1)
            new += result
        return [c3] + new

loops = 8

[c0, c1, c2] = radii(*startPoints)
c3, c4 = circit(c0, c1, c2)

clot = [c0, c1, c2] + circulate(c0, c1, c2, c4, loops) + circulate(c0, c1, c2, c3, loops)

w = 512
h = 512

# Make a pdf surface
surf =  cairo.PDFSurface(open("test.pdf", "w"), w, h)
# Make a svg surface
# surf =  cairo.SVGSurface(open("test.svg", "w"), w, h)

# Get a context object
ctx = cairo.Context(surf)

lineWidth = 0.001
ctx.set_line_width(lineWidth)

# both center and scale are defined by biggest circle
# print '#3 center: ', plot[3], ', radius: ', rlot[3]
# scale here and center in draw step by shifting

# next: translate and scale the data not the context
biggest = clot[3]
ctx.translate(w/2, h/2)
ctx.scale(250/abs(biggest[0]), 250/abs(biggest[0]))

def drawCircle(ctx, c):
    ctx.save()
    ctx.move_to(c[1] - c[0], c[2])
    ctx.arc(c[1], c[2], c[0], -pi, pi)
    ctx.restore()
    ctx.stroke()

cnt = 0
with  open('circdata', 'w') as datafile:
    datafile.write("r,x,y\n")
    for c in clot:
        if abs(c[0]) > lineWidth:
            d = [abs(c[0]), c[1] - biggest[1], c[2] - biggest[2]]
            drawCircle(ctx, d)
            cnt+=1
            datafile.write(str(d[0]) + "," + str(d[1]) + "," + str(d[2]) + "\n")

print cnt, '/', len(clot), ' circles in ', loops, ' loops.'
surf.finish()
