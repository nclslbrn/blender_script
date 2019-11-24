import bpy
import bmesh
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

def create_uv_sphere(name, u=32, v=32, d=1):
    bm =  bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, diameter=d)
    mesh = D.meshes.new(name + "_mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    # create object and link to scene
    x = random.randint(-3.0, 3.0)
    y = random.randint(-3.0, 3.0)
    z = random.randint(-3.0, 3.0)
    obj = D.objects.new(name, mesh)
    obj.location = (x, y, z)
    C.scene.collection.objects.link(obj)
    for face in mesh.polygons:
        face.use_smooth = True

    # C.scene.collection.objects.active = bpy.data.objects[name]
    # C.area.type = "PROPERTIES"
    # bpy.ops.object.modifier_add(type='COLLISION')
    return obj

numSphere = 64

for s in range(0,numSphere):
    diameter = random.uniform(0.5, 1.3)
    sphere = create_uv_sphere('sphere-' + str(s), u=32, v=32, d=diameter)
    