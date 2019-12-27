import bpy  # noqa
import bmesh  # noqa
import csv

from functions.updateProgress import update_progress
from classes.Agent import Agent
from functions.measure import measure
from functions.cleanScene import cleanScene
from functions.dodecahedron import createDodecahedron, cloneDodecahedron
# from functions.skinModifierSetVertexRadius import setupVertSkinRadius
# from functions.mechify import mechify
D = bpy.data
C = bpy.context


'''
    Your creative code here

'''
debug = False
writeAndCompute = True

agentNum = 50
agentLimit = 1000
agentSize = 0.25
limit = 12
shrink = 0.995
agents = []
tree = []
vertices_radius = []
buildCompleted = False if writeAndCompute else False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = agentSize


def initParticles():
    if debug:
        print('Creating particles...')

    for a in range(agentNum-1):
        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.onLimit(
            size=agentSize,
            limit=limit
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

        for m in range(2):

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
                size=agentSize
            )


def copyParticleToStructure(completion):

    if debug:
        print("Computing the tree...")

    currentSize = agentSize

    for a in range(len(agents)):

        for t in range(len(tree)):

            distance = measure(agents[a], tree[t])

            if distance <= (agents[a].size + tree[t].size)*4:

                # Add the agent to the tree
                tree.append(agents[a])

                # reset the agent
                currentSize *= shrink
                del agents[a]
                newAgent = Agent(x=0, y=0, z=0, size=currentSize)
                newAgent.onLimit(
                    limit=limit,
                    size=currentSize
                )
                agents.append(newAgent)

    return currentSize


def checkTreeLenght(buildCompleted):
    if debug:
        print("Check for tree length...")

    # check for tree array size
    if len(tree) > agentLimit:
        buildCompleted = True
    # check for tree size
    """ for t in range(len(tree)):
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
            buildCompleted = True """

    return buildCompleted


def drawLine(mesh, p1, p2):
    mesh.verts.extend(p1, p2)
    mesh.edges.extend(-1, -2)


cleanScene('MESH')
initParticles()
ddObj = createDodecahedron(size=agentSize)
progress = 0

if writeAndCompute:
    while not buildCompleted:

        moveParticle(progress)
        agentSize = copyParticleToStructure(progress)
        buildCompleted = checkTreeLenght(buildCompleted)
        progress = len(tree) / agentLimit
        update_progress("Computing DLA tree", progress)

        if buildCompleted:
            break

    # Storing tree coordinnates
    with open('../data-output/tree.csv', 'w') as dataFile:
        writer = csv.writer(dataFile)
        for i in range(len(tree)):
            writer.writerow([
                tree[i].size,
                tree[i].x,
                tree[i].y,
                tree[i].z
            ])


with open('../data-output/tree.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        cloneDodecahedron(
            size=float(row[0]),
            location=(float(row[1]), float(row[2]), float(row[3]))
        )

update_progress("Building DLA tree", 1)
