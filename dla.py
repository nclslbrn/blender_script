import bpy  # noqa
import bmesh  # noqa
# import time
# from mathutils import *

from functions.updateProgress import update_progress  #  noqa: E731
from classes.Agent import Agent  # noqa: E731
from functions.measure import measure  # noqa: E731
from functions.cleanScene import cleanScene  # noqa: E731


D = bpy.data
C = bpy.context


'''
    Your creative code here

'''
agentNum = 200
agentLimit = 200
AgentSpeed = 0.1
agentSize = 0.1
limit = 24
agents = []
tree = []
buildCompleted = False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0

debug = False


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
    '''
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=4,
        v_segments=4,
        diameter=agentSize
    )
    '''
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
        # voxelCopy.name = 'Voxel-copy-' + str(nt)
        voxelCopy.data = srcObject.data.copy()
        voxelCopy.animation_data_clear()
        voxelCopy.location = (t.x, t.y, t.z)
        C.scene.collection.objects.link(voxelCopy)
        progress = nt / len(tree)
        update_progress("Building DLA tree", progress)
        nt += 1


cleanScene('MESH')
srcObject = create_orig_voxel(
    name='origVoxel',
    d=agentSize,
    location=(0, 0, 0),
    faces=True
)

initParticles()

while not buildCompleted:
    moveParticle()
    copyParticleToStructure()
    buildCompleted = checkTreeLenght(buildCompleted)
    progress = len(tree) / agentLimit
    update_progress("Computing DLA tree", progress)

    if buildCompleted:
        break

update_progress("Computing DLA tree", 1)
buildShape()
update_progress("Building DLA tree", 1)
