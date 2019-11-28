import bpy
import random
# import bmesh
import numpy
# import scipy
from math import sin, cos, pi  # sqrt
# from mathutils import Vector

# Convenience Variables
D = bpy.data
C = bpy.context

# Delete everythings in the scene
objs = []
for obj in C.scene.objects:
    objs.append(obj)
bpy.ops.object.delete({"selected_objects": objs})

'''
    Your creative code here

'''
size = 12
pointPos = {'x': 0, 'y': 0, 'z': 0}
pointHistory = []
nPoint = 0
step = 15

quarterPi = pi / 4

'''
    MOOVE FUNCTION
'''


def NN(point):
    point['x'] -= step
    return point


def SS(point):
    point['x'] += step
    return point


def WW(point):
    point['y'] -= step
    return point


def EE(point):
    point['y'] += step
    return point


def NE(point):
    point['x'] += step * cos(quarterPi)
    point['y'] -= step * sin(quarterPi)
    return point


def NW(point):
    point['x'] -= step * cos(quarterPi)
    point['y'] -= step * sin(quarterPi)
    return point


def SE(point):
    point['x'] += step * cos(quarterPi)
    point['y'] += step * sin(quarterPi)
    return point


def SW(point):
    point['x'] -= step * cos(quarterPi)
    point['y'] += step * sin(quarterPi)
    return point


moves = {
    'moveNN': NN,
    'moveNE': NE,
    'moveEE': EE,
    'moveSE': SE,
    'moveSS': SS,
    'moveSW': SW,
    'moveWW': WW,
    'moveNW': NW
}

'''
    SETUP OBJECT
'''


def setupCurve():
    curveRes = 32
    extrude = 0.01
    # Setup curve path
    curveData = D.curves.new(name='curveName', type='CURVE')
    curveData.bevel_depth = 0.01
    curveData.dimensions = '3D'
    curveData.resolution_u = curveRes
    curveData.render_resolution_u = curveRes
    curveData.extrude = extrude

    # Setup curve object
    curve = bpy.data.objects.new('objName', curveData)
    curve.location = (0, 0, 0)
    C.scene.collection.objects.link(curve)

    polyline = curveData.splines.new('BEZIER')

    return polyline


def drawCurve(curve, pointHistory):
    points = numpy.array(pointHistory)
    polyline.bezier_points.add(len(points-1))

    for p in range(0, len(points)):

        polyline.bezier_points[p].co = [
            points[p][0],
            points[p][1],
            points[p][2]
        ]

    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = True


'''
    MOOVE LOOP
'''

polyline = setupCurve()

while(
    pointPos['x'] > size * -0.5 or
    pointPos['y'] > size * -0.5 or
    pointPos['x'] < size * 0.5 or
    pointPos['y'] < size * 0.5
):
    move = random.choice(list(moves.keys()))
    pointPos = moves[move](pointPos)
    pointHistory.append([pointPos['x'], pointPos['y'], pointPos['z']])
    drawCurve(polyline, pointHistory)
    nPoint += 1
