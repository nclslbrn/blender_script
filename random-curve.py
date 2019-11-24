import bpy
import random
from mathutils import *
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

'''
# Create a bezier circle and enter edit mode.
curve = bpy.ops.curve.primitive_bezier_circle_add(radius=1.0,
                                      location=(0.0, 0.0, 0.0),
                                      enter_editmode=True)

# Subdivide the curve by a number of cuts, giving the
# random vertex function more points to work with.
bpy.ops.curve.subdivide(number_cuts=16)
# Randomize the vertices of the bezier circle.
# offset [-inf .. inf], uniform [0.0 .. 1.0],
# normal [0.0 .. 1.0], RNG seed [0 .. 10000].
bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.0, seed=0)

# Scale the curve while in edit mode.
bpy.ops.transform.resize(value=(2.0, 2.0, 3.0))

# Return to object mode.
bpy.ops.object.mode_set(mode='OBJECT')
'''
def MakeRandomCurve(objName, curveName, numPoint, scale):
    curveData = D.curves.new(name=curveName, type='CURVE')
    #curveData.dimensions = '3D'
    curve = bpy.data.objects.new(objName, curveData)  
    curve.location = (0,0,0) # object origin  
    C.scene.collection.objects.link(curve)

    polyline = curveData.splines.new('BEZIER')
    polyline.bezier_points.add(numPoint-1)

    for p in range(0, numPoint):
        x = random.randint(-scale, scale)
        y = random.randint(-scale, scale)
        z = random.randint(-scale, scale)
        
        polyline.bezier_points[p].co = [x, y, z]

    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = True 
    
    return curve

curve = MakeRandomCurve('curveObject', 'curve', 32, 5)