import bpy
import sys
import os
import bmesh
from math import sqrt
# from mathutils import *

dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

from classes.Agent import Agent  # noqa: E731
from classes.print import printPos  # noqa: E731

D = bpy.data
C = bpy.context

'''
    Delete everythings in the scene

'''
objs = []
for obj in C.scene.objects:
    if obj.type == 'MESH':
        objs.append(obj)
bpy.ops.object.delete({"selected_objects": objs})

'''
    Your creative code here

'''
agentNum = 6000
agentLimit = 500
step = 0.01
limit = 0.5
agents = []
tree = []
buildCompleted = False

tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0


def measure(first, second):

    locx = second.x - first.x
    locy = second.y - first.y
    locz = second.z - first.z

    distance = sqrt((locx)**2 + (locy)**2 + (locz)**2)
    return distance


def create_cube(name='default_cube', d=0.1, location=(0, 0, 0), faces=True):

    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Voxel')
    basic_cube = bpy.data.objects.new(name, mesh)
    basic_cube.location = location

    # Add the object into the scene.
    C.scene.collection.objects.link(basic_cube)

    # Construct the bmesh cube and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=step)
    bm.to_mesh(mesh)
    bm.free()

    return basic_cube


srcObject = create_cube(name='origVoxel', d=step,
                        location=(0, 0, 0), faces=True)


for a in range(agentNum):
    agents.append(Agent)
    agents[a].set(agents[a], limit, step)


while not buildCompleted:

    for a in range(len(agents)):

        agents[a].move(agents[a])

        for t in range(len(tree)):

            if measure(agents[a], tree[t]) <= step:

                agents[a].stop = True
                tree.append(Agent)
                lastTree = len(tree)-1
                tree[lastTree].x = agents[a].x
                tree[lastTree].y = agents[a].y
                tree[lastTree].z = agents[a].z

                #   Debug
                #   printPos(agents[a])
                print(len(tree))

                del agents[-1]
                agents.append(Agent)
                lastAgent = len(agents)-1
                agents[lastAgent] = Agent.set(agents[lastAgent], limit, step)

            if(
                tree[t].x < limit * -0.5 or
                tree[t].y < limit * -0.5 or
                tree[t].z < limit * -0.5 or
                tree[t].x > limit * 0.5 or
                tree[t].y > limit * 0.5 or
                tree[t].z > limit * 0.5
            ):
                buildCompleted = True
                break

        if len(tree) > agentLimit:

            buildCompleted = True
            break

else:

    print("Build the DLA shape")

    for t in range(len(tree)):

        voxelCopy = srcObject.copy()
        voxelCopy.name = 'Voxel-copy-' + str(t)
        voxelCopy.data = srcObject.data.copy()
        voxelCopy.animation_data_clear()
        if hasattr(tree[t], 'x') and hasattr(tree[t], 'y') and hasattr(tree[t], 'z'):
            printPos(tree[t])
        else:
            print("Tree n° " + str(t) + " x, y and z not set.")

        voxelCopy.location = (tree[t].x, tree[t].y, tree[t].z)
        print(voxelCopy.location)
        C.scene.collection.objects.link(voxelCopy)
