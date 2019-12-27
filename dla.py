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

agentNum = 100
agentLimit = 10000
agentSize = 1.0
limit = 24
shrink = 0.9995
expand = 1.05
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

    for a in range(agentNum-1):
        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.onLimit(
            size=agentSize,
            limit=limit
        )
        agents.append(newAgent)


def moveParticle(completion):

    for a in range(len(agents)):
        min = (limit+1) * -0.5
        max = (limit+1) * 0.5

        for m in range(24):
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

    currentSize = agentSize
    currentLimit = limit

    for a in range(len(agents)):

        for t in range(len(tree)):

            distance = measure(agents[a], tree[t])

            if distance <= (agents[a].size + tree[t].size)*4:

                # Add the agent to the tree
                tree.append(agents[a])

                # reset the agent
                if currentSize > 0.05:
                    currentSize *= shrink
                if currentLimit < 74:
                    currentLimit *= expand

                del agents[a]
                newAgent = Agent(x=0, y=0, z=0, size=currentSize)
                newAgent.onLimit(
                    limit=limit,
                    size=currentSize
                )
                agents.append(newAgent)

            if debug:
                print(
                    "Limit: {} | Size : {} | Obj : {}/{}".format(
                        currentLimit,
                        currentSize,
                        len(tree),
                        agentLimit
                    )
                )

    return {currentSize, currentLimit}


def checkTreeLenght(buildCompleted):

    if len(tree) > agentLimit:
        buildCompleted = True

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
        agentSize, limit = copyParticleToStructure(progress)
        buildCompleted = checkTreeLenght(buildCompleted)

        if not debug:
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
    index = 0

    for row in reader:
        cloneDodecahedron(
            size=float(row[0]),
            location=(float(row[1]), float(row[2]), float(row[3]))
        )
        index += 1

        if not debug:
            progress = index / agentLimit
            update_progress("Building DLA tree", progress)

if not debug:
    update_progress("Building DLA tree", 1)
