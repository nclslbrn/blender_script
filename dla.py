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
agentNum = 5000
agentLimit = 50000
agentSpeed = 1
agentSize = 1
limit = 32
agents = []
tree = []
buildCompleted = False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = 1

debug = False


def create_orig_voxel(
    name='default_cube',
    d=0.1,
    location=(0, 0, 0),
    faces=True
):

    # Create an empty mesh and add the object.
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
        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.set(
            size=agentSize,
            limit=limit,
            speed=agentSpeed
        )
        agents.append(newAgent)

    if debug:
        print('Particles created')


def moveParticle(completion):

    if debug:
        print("Moving particles...")

    for a in range(len(agents)):
        min = (limit+1) * -0.5
        max = (limit+1) * 0.5

        for m in range(5):

            agents[a] = agents[a].move()

        if(
            agents[a].x < min or
            agents[a].y < min or
            agents[a].z < min or
            agents[a].x > max or
            agents[a].y > max or
            agents[a].z > max
        ):
            agents[a] = agents[a].set(
                limit=limit,
                speed=agentSpeed,
                size=agentSize
            )


def copyParticleToStructure(completion):
    if debug:
        print("Computing the tree...")

    for a in range(len(agents)):

        for t in range(len(tree)):
            distance = measure(agents[a], tree[t])
            if distance >= agentSize * 0.75 and distance <= agentSize * 1.25:

                tree.append(agents[a])
                del agents[a]
                newAgent = Agent(x=0, y=0, z=0, size=agentSize)
                newAgent.set(
                    limit=completion,
                    speed=agentSpeed,
                    size=agentSize
                )
                agents.append(newAgent)


def checkTreeLenght(buildCompleted):
    if debug:
        print("Check for tree length...")
    # check for tree array size
    if len(tree) > agentLimit:
        buildCompleted = True
    # check for tree size
    for t in range(len(tree)):
        min = limit * -0.5
        max = limit * 0.5
        if(
            tree[t].x < min or
            tree[t].y < min or
            tree[t].z < min or
            tree[t].x > max or
            tree[t].y > max or
            tree[t].z > max
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
    for t in range(len(tree)):
        voxelCopy = srcObject.copy()
        # voxelCopy.name = 'Voxel-copy-' + str(nt)
        voxelCopy.data = srcObject.data.copy()
        voxelCopy.animation_data_clear()
        voxelCopy.scale = (tree[t].size, tree[t].size, tree[t].size)
        voxelCopy.location = (tree[t].x, tree[t].y, tree[t].z)
        C.scene.collection.objects.link(voxelCopy)
        progress = t / len(tree)
        update_progress("Building DLA tree", progress)


cleanScene('MESH')
srcObject = create_orig_voxel(
    name='origVoxel',
    d=agentSize,
    location=(0, 0, 0),
    faces=True
)

initParticles()

progress = 0

while not buildCompleted:

    moveParticle(progress)
    copyParticleToStructure(progress)
    buildCompleted = checkTreeLenght(buildCompleted)
    progress = len(tree) / agentLimit
    update_progress("Computing DLA tree", progress)

    if buildCompleted:
        break

update_progress("Computing DLA tree", 1)
buildShape()
update_progress("Building DLA tree", 1)
