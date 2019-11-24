import bpy
import random
import math
from mathutils import *
D = bpy.data
C = bpy.context

'''
    Delete everythings in the scene

'''
objs = []
for obj in C.scene.objects:
    objs.append(obj)
bpy.ops.object.delete({"selected_objects": objs})  

'''
    Your creative code here

'''

def MakeRandomCurve(objName, curveName, numPoint, scale, radius):

    curveRes = 32
    extrude = 0.01

    # Setup curve path
    curveData = D.curves.new(name=curveName, type='CURVE')
    curveData.bevel_depth = radius
    curveData.dimensions = '3D'
    curveData.resolution_u = curveRes
    curveData.render_resolution_u = curveRes
    curveData.extrude = extrude

    # Setup curve object
    curve = bpy.data.objects.new(objName, curveData)  
    curve.location = (0,0,0)
    C.scene.collection.objects.link(curve)

    polyline = curveData.splines.new('BEZIER')
    polyline.bezier_points.add(numPoint-1)

    x = 0
    y = 0
    z = 0

    for p in range(0, numPoint):

        x = random.randint(-scale, scale)
        y = random.randint(-scale, scale)
        z = random.randint(-scale, scale)

        polyline.bezier_points[p].co = [x, y, z]

    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = True 

    
    return curve

curve = MakeRandomCurve('curveObject', 'curve', 256, 5, 0.01)