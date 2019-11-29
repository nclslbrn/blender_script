import bpy
import sys
import os
from math import sqrt
# from mathutils import *

dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

from classes.Agent import Agent  # noqa: E731
from classes.print import print as print  # noqa: E731

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
step = 0.1
limit = 2
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


def create_cube(name, d=0.1, faces=True):

    Verts = [
        (1.0, 1.0, -1.0),
        (1.0, -1.0, -1.0),
        (-1.0, -1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (1.0, 1.0, 1.0),
        (1.0, -1.0, 1.0),
        (-1.0, -1.0, 1.0),
        (-1.0, 1.0, 1.0)
    ]

    face_indices = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7)
    ]

    Faces = face_indices if faces else []

    if not (d == 1.0):
        Verts = [tuple(v*d for v in vert) for vert in Verts]

    mesh = D.meshes.new(name + "_mesh")
    mesh.from_pydata(Verts, [], Faces)
    mesh.update()

    obj = D.objects.new(name + "_Object", mesh)
    C.scene.collection.objects.link(obj)
    return obj


for a in range(agentNum):
    agents.append(Agent)
    agents[a].set(agents[a], limit, step)

while not buildCompleted:

    for a in range(len(agents)):

        agents[a].move(agents[a])

        for t in range(len(tree)):

            if measure(agents[a], tree[t]) <= 0.1:

                agents[a].stop = True

                if(
                    agents[a].x < limit * -0.5 or
                    agents[a].y < limit * -0.5 or
                    agents[a].z < limit * -0.5 or
                    agents[a].x > limit * 0.5 or
                    agents[a].y > limit * 0.5 or
                    agents[a].z > limit * 0.5
                ):
                    buildCompleted = False
                    break

                tree.append(agents[a])

                #   Debug
                #   print("%.2f : %.2f : %.2f" % (agents[a].x, agents[a].y, agents[a].z))
                del agents[-1]
                agents.append(Agent)
                last = len(agents)-1
                agents[last] = Agent.set(agents[last], limit, step)

if buildCompleted:
    for t in range(len(tree)):
        bpy.ops.mesh.primitive_cube_add(
            location=(tree[t].x, tree[t].y, tree[t].z)
        )