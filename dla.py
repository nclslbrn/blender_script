import bpy  # noqa
import sys
import os
import bmesh  # noqa
import time
from math import sqrt
# from mathutils import *

dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

from classes.Agent import Agent  # noqa: E731
#  from classes.print import print, printPos  # noqa: E731

D = bpy.data
C = bpy.context


'''
    Your creative code here

'''
agentNum = 500
agentLimit = 200
AgentSpeed = 0.1
agentSize = 0.5
limit = 12
agents = []
tree = []
buildCompleted = False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0

debug = False


def cleanScene():
    objs = []
    for obj in C.scene.objects:
        if obj.type == 'MESH':
            objs.append(obj)
    bpy.ops.object.delete({"selected_objects": objs})


def measure(first, second):
    locx = second.x - first.x
    locy = second.y - first.y
    locz = second.z - first.z

    distance = sqrt((locx)**2 + (locy)**2 + (locz)**2)
    return distance


def create_orig_voxel(
    name='default_cube',
    d=0.1,
    location=(0, 0, 0),
    faces=True
):

    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Voxel')
    basic_cube = bpy.data.objects.new(name, mesh)
    basic_cube.location = location

    # Add the object into the scene.
    C.scene.collection.objects.link(basic_cube)

    # Construct the bmesh cube and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=agentSize)
    bm.to_mesh(mesh)
    bm.free()

    return basic_cube


def initParticles():
    if debug:
        print('Creating particles...')

    for a in range(agentNum-1):
        newAgent = Agent(x=0, y=0, z=0)
        newAgent.set(limit=limit, speed=AgentSpeed)
        agents.append(newAgent)


def moveParticle():

    if debug:
        print("Moving particles...")

    for agent in agents:
        min = limit * -0.5
        max = limit * 0.5

        for m in range(5):
            agent.move()

        if(
            agent.x < min or
            agent.y < min or
            agent.z < min or
            agent.x > max or
            agent.y > max or
            agent.z > max
        ):
            agent.set(limit=limit, speed=AgentSpeed)


def copyParticleToStructure():

    if debug:
        print("Computing the tree...")

    for branch in tree:
        nAgent = 0
        for agent in agents:
            if measure(agent, branch) <= agentSize:

                agent.stop = True
                tree.append(agent)
                del agents[nAgent]
                newAgent = Agent(x=0, y=0, z=0)
                newAgent.set(limit=limit, speed=AgentSpeed)
                agents.append(newAgent)

            nAgent += 1


def checkTreeLenght(buildCompleted):
    if debug:
        print("Check for tree length...")

    if len(tree) > agentLimit:
        buildCompleted = True

    for branch in tree:
        min = limit * -0.5
        max = limit * 0.5
        if(
            branch.x < min or
            branch.y < min or
            branch.z < min or
            branch.x > max or
            branch.y > max or
            branch.z > max
        ):
            buildCompleted = True

    return buildCompleted


def showParticle():
    srcObject = create_orig_voxel(
        name='origVoxel',
        d=agentSize,
        location=(0, 0, 0),
        faces=True
    )
    na = 0
    for agent in agents:
        voxelCopy = srcObject.copy()
        voxelCopy.name = 'particle-' + str(na)
        voxelCopy.data = srcObject.data.copy()
        voxelCopy.animation_data_clear()
        voxelCopy.location = (agent.x, agent.y, agent.z)
        C.scene.collection.objects.link(voxelCopy)
        na += 1


def buildShape():
    print("Building tree...")

    srcObject = create_orig_voxel(
        name='origVoxel',
        d=agentSize,
        location=(0, 0, 0),
        faces=True
    )
    nt = 0
    for t in tree:
        voxelCopy = srcObject.copy()
        voxelCopy.name = 'Voxel-copy-' + str(nt)
        voxelCopy.data = srcObject.data.copy()
        voxelCopy.animation_data_clear()
        voxelCopy.location = (t.x, t.y, t.z)
        C.scene.collection.objects.link(voxelCopy)
        nt += 1


cleanScene()
initParticles()

while not buildCompleted:
    moveParticle()
    copyParticleToStructure()
    buildCompleted = checkTreeLenght(buildCompleted)

    if debug:
        print(str(len(tree)) + " elements in the tree.")

    if buildCompleted:
        break
    # time.sleep(0.5)  # pause of 0.5sec
buildShape()

# showParticle()
