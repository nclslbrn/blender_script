import bpy
import numpy
import sys
import os
import random as random
dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

from classes.Walker import Walker  # noqa: E731
from classes.print import print as print  # noqa: E731

# Convenience Variables
D = bpy.data
C = bpy.context

# Delete previous generated curve in the scene

objs = []
for obj in C.scene.objects:
    if obj.type == 'CURVE':
        objs.append(obj)
bpy.ops.object.delete({"selected_objects": objs})

'''
    Your creative code here
'''
limit = 12
mooveNum = 120
walkerNum = 26
animFrame = 500

bpy.context.scene.frame_end = animationFrame


# SETUP OBJECT

def setupCurve(points):
    curveRes = 2
    extrude = 0
    # Setup curve path
    curveData = D.curves.new(name='curveName', type='CURVE')
    curveData.bevel_depth = 0.1
    curveData.dimensions = '3D'
    curveData.resolution_u = curveRes
    curveData.render_resolution_u = curveRes
    curveData.extrude = extrude

    # Setup animation
    curveData.bevel_factor_end = 0
    curveData.keyframe_insert(data_path="bevel_factor_end", frame=0)
    curveData.bevel_factor_end = 1
    curveData.keyframe_insert(data_path="bevel_factor_end", frame=animFrame)

    # Setup curve object
    curve = bpy.data.objects.new('objName', curveData)
    curve.location = (0, 0, 0)

    # Add it to the scene
    C.scene.collection.objects.link(curve)
    polyline = curveData.splines.new('NURBS')

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
        polyline.points[p].radius = random.uniform(0.1, 0.5)

    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = False


# MOOVE LOOP
for w in range(walkerNum):

    pointPos = Walker(0, 0, 0)
    pointHistory = []

    for m in range(mooveNum):

        posAlreadyUsed = False
        posTooFar = False
        newWalker = Walker(pointPos.x, pointPos.y, pointPos.z)
        newPos = newWalker.move()

        # check if newPos is out of limit
        if(
            newPos.x < limit * -0.5 or
            newPos.y < limit * -0.5 or
            newPos.x > limit * 0.5 or
            newPos.y > limit * 0.5
        ):
            posTooFar = True

        # check if newPos already exists in pointHistory
        for p in range(len(pointHistory)):
            if(
                pointHistory[p][0] == newPos.x and
                pointHistory[p][1] == newPos.y and
                pointHistory[p][2] == newPos.y
            ):
                posAlreadyUsed = True

        # then store newPos in pointHistory
        if not posAlreadyUsed and not posTooFar:
            pointHistory.append([newPos.x, newPos.y, newPos.z])
            pointPos = newPos
        else:
            del pointHistory[len(pointHistory)-1]

    points = numpy.array(pointHistory)
    polyline = setupCurve(points)
    drawCurve(polyline, points)

print("DONE")
