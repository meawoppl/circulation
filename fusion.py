from math import sin, cos, pi
from circles import radii, circit
import itertools
import shapely
from shapely.ops import cascaded_union
from shapely.geometry.polygon import LinearRing
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import  MultiPolygon
from pylab import plot, axis, show
import cairo
import numpy as np

def makeShapelyCircle(x, y, r, thickness=0.01, n=2000):
    t = np.linspace(0, 2*pi, n)
    return LinearRing(zip((np.cos(t) * r) + x, (np.sin(t) * r) + y)).buffer(thickness)

def makeShapelyAnulus(x, y, r, n = 500):
    return Point(x, y).buffer(r)

def plotShapelyPolygon(polygon):
    assert(type(polygon) == shapely.geometry.polygon.Polygon)
    x, y = np.array(polygon.exterior.coords).T
    plot(x, y, "b")

    for ring in (polygon.interiors):
        x, y = np.array(ring.coords).T
        plot(x, y, "b")

def plotMPolygon(mpolygon):
    assert(isinstance(mpolygon, shapely.geometry.multipolygon.MultiPolygon))
    for p in mpolygon.geoms:
        plotShapelygon(p)

def plotShapelygon(sgon):
    if isinstance(sgon, MultiPolygon):
        plotMPolygon(sgon)
    else:
        plotShapelyPolygon(sgon)

def svgShapelyPolygon(polygon, ctx):
    def traceXYs(xs, ys, ctx):
        ctx.new_path()
        for x, y in zip(xs, ys):
            ctx.line_to(x * 100. + 512, y * 100. + 512)
        ctx.stroke()

    xs, ys = np.array(polygon.exterior.coords).T
    traceXYs(xs, ys, ctx)

    for ring in (polygon.interiors):
        xs, ys = np.array(ring.coords).T
        traceXYs(xs, ys, ctx)

def svgMPolygon(mpolygon, ctx):
    assert(isinstance(mpolygon, shapely.geometry.multipolygon.MultiPolygon))
    for p in mpolygon.geoms:
        svgShapelyPolygon(p, ctx)

def svgShapelygon(sgon, svgFilename):
    surf = cairo.SVGSurface(open(svgFilename, "w"), 1024, 1024)
    ctx = cairo.Context(surf)

    if isinstance(sgon, MultiPolygon):
        svgMPolygon(sgon, ctx)
    else:
        svgShapelyPolygon(sgon, ctx)

    print "saving", svgFilename
    surf.flush()        
    surf.write_to_png(svgFilename.split('.')[0] + ".png")
    surf.finish()


def make_one(shift=[0., 0.]):
    """    original   """
    # startPoints = list(range(3))
    # for i in startPoints:
    #     x = 2.5*cos(2.0 * pi * i / 3)
    #     y = 2.5*sin(2.0 * pi * i / 3)
    #     startPoints[i] = [x, y]

    """    anomalus    """
    # startPoints = [[-2, 2], [0, 0], [2, 2]]

    """    earhoops    """
    # startPoints = [[-1, -2], [0, 1], [1, -2]]

    """    random    """
    # startPoints = (np.random.rand(3, 2) * 4. - 2.).tolist()
    
    """    random angles    """
    # startPoints = [[np.cos(2. * np.pi * t), np.sin(2. * np.pi * t)] for t in np.random.rand(3)]

    # all circles are defined as c = [r, px, py] with
    # radius = c[0] and x, y coordinates of the center
    # c[1] and c[2] (latter adding c[3] to make a 3d
    # gasket with spheres)

    def rand_init():
        points = np.random.rand(3, 2) - .5
        return points.tolist()

    def circulate(c0, c1, c2, c3, depth):
        cList = [c0, c1, c2]

        if depth == 0:
            return [c3]
        else:
            new = []
            for indxs in itertools.combinations(range(3), 2):
                i0, i1 = indxs
                cI, cO = circit(cList[i0], cList[i1], c3)
                    
                if cList[i0][0] * cList[i1][0] * c3[0] > 0:
                    cNew = cI
                else:
                    cNew = cO
                        
                new += circulate(cList[i0], cList[i1], c3, cNew, depth-1)
            return [c3] + new
    def sign (p1, p2, p3):
        return (p1[1] - p3[1]) * (p2[2] - p3[2]) - (p2[1] - p3[1]) * (p1[2] - p3[2])

    def PointInTriangle(pt, v1, v2, v3):
        b1 = sign(pt, v1, v2) < 0.
        b2 = sign(pt, v2, v3) < 0.
        b3 = sign(pt, v3, v1) < 0.
        return ((b1 == b2) and (b2 == b3))

    loops = 4

    good3 = False
    while not good3:
        startPoints = rand_init()
        [c0, c1, c2] = radii(*startPoints)
        c3, c4 = circit(c0, c1, c2)
        if c4[0] > 0: continue
        if not PointInTriangle(c4, c1, c2, c3): continue
        good3 = True

    clot = [c0, c1, c2] + circulate(c0, c1, c2, c4, loops) + circulate(c0, c1, c2, c3, loops)

    biggestR = max(abs(np.array(clot)[:,0]))
    scale = 1.4 / biggestR
    annuli = []
    for c in clot:
        r, x, y = c
        if abs(r) < 0.05: continue
        annuli.append( makeShapelyCircle(
            scale * (x - c4[1]) + (shift[0] - 1) *3,
            scale * (y - c4[2]) + (shift[1] - 1) *3,
            scale * abs(r),
            thickness=0.05) )

    testUnion = cascaded_union(annuli)
    return testUnion


def main():
    gaskets = []
    for i in range(3):
        for j in range(3):
            gaskets.append(make_one(shift=[float(i), float(j)]))
    
    threexthree = cascaded_union(gaskets)
    plotShapelygon(threexthree)
    svgShapelygon(threexthree, "examples/test-union.svg")
    axis("image")
    show()


if __name__=='__main__':
    main()
