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
isFinal = True
debug = False

agentNum = 50
agentLimit = 200 if isFinal else 50
agentSpeed = 1
agentSize = 1
limit = 64 if isFinal else 8
agents = []
tree = []
lines = []
buildCompleted = False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = 1


def initParticles():
    if debug:
        print('Creating particles...')

    for a in range(agentNum-1):
        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.onLimit(
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
            agents[a] = agents[a].onLimit(
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
            if distance >= agentSize * 0.95 and distance <= agentSize:

                tree.append(agents[a])
                del agents[a]
                newAgent = Agent(x=0, y=0, z=0, size=agentSize)
                newAgent.onLimit(
                    limit=limit,
                    speed=agentSpeed,
                    size=agentSize
                )
                agents.append(newAgent)

                lines.append([tree[t].x, tree[t].y, tree[t].z])
                lines.append([agents[a].x, agents[a].y, agents[a].z])


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


def drawLine(mesh, p1, p2):
    mesh.verts.extend(p1, p2)
    mesh.edges.extend(-1, -2)


cleanScene('MESH')

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

# buildShape
mesh = bpy.data.meshes.new("Plane")
edges = []
for i in range(0, len(lines), 2):
    edges.append([i, i+1])

treeObj = bpy.data.objects.new("Plane", mesh)
treeObj.location = (0, 0, 0)
C.scene.collection.objects.link(treeObj)
mesh.from_pydata(lines, edges, [])
mesh.update(calc_edges=True)
# bpy.ops.object.convert(target='CURVE')
update_progress("Building DLA tree", 1)
