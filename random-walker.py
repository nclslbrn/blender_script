import bpy
import random
import numpy
import sys
import os
# import bmesh
# import scipy
# from mathutils import Vector
from math import sin, cos, pi  # sqrt

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from walker import walker

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
limit = 12
pointPos = {'x': 0, 'y': 0, 'z': 0}
pointHistory = []
nPoint = 0
step = 0.5
quarterPi = pi / 4
mooveNum = 75


# SETUP OBJECT


def setupCurve(points):
    curveRes = 2
    extrude = 0
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
    polyline = curveData.splines.new('POLY')

    return polyline


def drawCurve(curve, points):
    polyline.points.add(len(points))

    for p in range(len(points)):

        polyline.points[p].co = (
            points[p][0],
            points[p][1],
            points[p][2],
            0.1
        )
        # polyline.points[p].radius = random.uniform(0.1, 0.5)

    polyline.order_u = len(polyline.points)
    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = False


# MOOVE LOOP


for m in range(0, mooveNum):

    posAlreadyUsed = False
    posTooFar = False

    newWalker = walker(pointPos.x, pointPos.y, pointPos.z)
    newPos = newWalker.move()
    # newPos = moves[move](pointPos)

    # check if newPos is out of limit
    if(
        newPos['x'] < limit * -0.5 or
        newPos['y'] < limit * -0.5 or
        newPos['x'] > limit * 0.5 or
        newPos['y'] > limit * 0.5
    ):
        posTooFar = True

    # check if newPos already exists in pointHistory
    for p in range(len(pointHistory)):
        if(
            pointHistory[p][0] == newPos['x'] and
            pointHistory[p][1] == newPos['y'] and
            pointHistory[p][2] == newPos['y']
        ):
            posAlreadyUsed = True

    # then store newPos in pointHistory
    if not posAlreadyUsed and not posTooFar:
        pointHistory.append([newPos['x'], newPos['y'], newPos['z']])
        pointPos = newPos

points = numpy.array(pointHistory)
print(len(points))
polyline = setupCurve(points)
drawCurve(polyline, points)
