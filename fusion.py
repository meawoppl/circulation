from math import sin, cos, pi
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
startPoints = [[-1, -2], [0, 1], [1, -2]]

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

            result = circulate(cList[i0], cList[i1], c3, cNew, depth-1)
            new += result
        return [c3] + new

loops = 6

[c0, c1, c2] = radii(*startPoints)
c3, c4 = circit(c0, c1, c2)

clot = [c0, c1, c2] + circulate(c0, c1, c2, c4, loops) + circulate(c0, c1, c2, c3, loops)

from shapely import *
from shapely.ops import cascaded_union
from shapely.geometry.polygon import LinearRing
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import  MultiPolygon
from scipy import *
from pylab import *
import cairo


# def makeShapelyAnnulus(x, y, r, n = 500):
#     t = linspace(0, 2*pi, n)
#     return LinearRing(zip((cos(t) * r) + x, (sin(t) * r) + y)).buffer(0.002)

def makeShapelyAnnulus(x, y, r, n = 500):
    return Point(x, y).buffer(r)

def plotShapelyPolygon(polygon):
    print type(polygon)
    x, y = array(polygon.exterior.coords).T
    plot(x, y, "b")

    for ring in (polygon.interiors):
        x, y = array(ring.coords).T
        plot(x, y, "b")

def plotMPolygon(mpolygon):
    for p in mpolygon.geoms:
        plotShapelygon(p)

def plotShapelygon(sgon):
    if isinstance(sgon, MultiPolygon):
        plotMPolygon(sgon)
    else: # isinstance(sgon, Polygon):
        plotShapelyPolygon(sgon)
    # else:
    #     print "wtf", type(sgon)


def svgShapelyPolygon(polygon, svgFilename):
    def traceXYs(xs, ys, ctx):
        ctx.new_path()
        for x, y in zip(xs, ys):
            ctx.line_to(x, y)
        ctx.stroke()

    surf =  cairo.SVGSurface(open(svgFilename, "w"), 512, 512)
    ctx = cairo.Context(surf)

    xs, ys = array(polygon.exterior.coords).T
    traceXYs(xs, ys, ctx)

    for ring in (polygon.interiors):
        xs, ys = array(ring.coords).T
        traceXYs(xs, ys, ctx)

    surf.finish()


biggestR = max(abs(array(clot)[:,0]))
print biggestR
annuli = []
for n, c in enumerate(clot):
    r, x, y = c
    if abs(r) > 3: continue
    if abs(r) < 0.02: continue
    annuli.append( makeShapelyAnnulus(x, y, abs(r)) )

    # if n % 101: print n

print "Computing Union"
testUnion = cascaded_union(annuli)

print "Plotting"
# plotShapelyPolygon(testUnion)
plotShapelygon(testUnion)
#svgShapelyPolygon(testUnion, "test-union.svg")
axis("image")
show()

1/0

print "Computing Circles"
annuli = []
for n, line in enumerate(open("circdata").readlines()):
    if n == 0: continue
    x, y, r = [float(v) for v in line.strip().split(",")]
    annuli.append(makeShapelyCircle(x, y, r).buffer(1))

print "Computing Union"
# testUnion = cascaded_union(annuli)


ext = array(testUnion.exterior)
plot(ext[:,0], ext[:,1])

for pg in testUnion.interiors:
    ary = array(pg)
    plot(ary[:,0], ary[:,1])

axis("image")
show()
