import bpy  # noqa
import bmesh  # noqa
import csv
import sys
# progress bar implementation (visible on terminal)
from functions.updateProgress import update_progress
# particle class
from classes.Agent import Agent
# function to erase every object cleanScene(<type>) on the scene
from functions.cleanScene import cleanScene
# function to create and copy dodecahedron
from functions.dodecahedron import createDodecahedron, cloneDodecahedron

# Argument from command line
# blender --python dla.py -- <writeAndCompute>
argv = sys.argv
argv = argv[argv.index("--") + 1:]

D = bpy.data
C = bpy.context

# display agentSize and limit size (and hide progress)
debug = False
# Used to build DLA from CSV file
writeAndCompute = argv[0] if argv[0] else True
# How many agents live at same time
agentNum = 50
# How many agents will stuck on tree
agentLimit = 500

# Distance limit of of agents move (increase over time)
diffusionLimit = 4.0
maxDiffusionDistance = 24
# Size of the first agent (decrease over time)
agentSize = 0.35
# Factor to decrease agents size
shrink = 0.995
minAgentSize = 0.01

# Array to store moving agent
agents = []
# Array to store dead agents
tree = []
# State of computation at the begining of the script
computationDone = False if writeAndCompute else True

# Create the first cluster at the center
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = agentSize

filePath = '../data-output/tree.csv'


# init agents around the cluster
def initAgents():

    for a in range(agentNum-1):

        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.onRadius(
            size=agentSize,
            limit=diffusionLimit
        )
        agents.append(newAgent)


def isTreeFilled():
    if len(tree) >= agentLimit:
        return True
    else:
        return False


cleanScene('MESH')
initAgents()
ddObj = createDodecahedron(size=agentSize)

if writeAndCompute:
    while not computationDone:

        for a in range(len(agents)):

            for m in range(32):

                agents[a].move()
                agents[a].reInitIfOutside(diffusionLimit)

                for c in range(len(tree)):

                    if isTreeFilled():
                        break

                    dx = round(abs(tree[c].x - agents[a].x), 2)
                    dy = round(abs(tree[c].y - agents[a].y), 2)
                    dz = round(abs(tree[c].z - agents[a].z), 2)

                    minD = round(agents[a].size + tree[c].size, 2)*2

                    if(
                        dx <= minD and
                        dy <= minD and
                        dz <= minD
                    ):

                        # add the agent to the tree
                        tree.append(agents[a])

                        # change constants
                        if agentSize > minAgentSize:
                            agentSize *= shrink

                        # reset the agent
                        del agents[a]
                        newAgent = Agent(x=0, y=0, z=0, size=agentSize)
                        newAgent.onRadius(
                            limit=diffusionLimit,
                            size=agentSize
                        )
                        agents.append(newAgent)

                    if diffusionLimit < maxDiffusionDistance:

                        if abs(tree[c].x) >= diffusionLimit*0.95:
                            diffusionLimit = round(abs(tree[c].x)*1.05, 1)

                        if abs(tree[c].y) >= diffusionLimit*0.95:
                            diffusionLimit = round(abs(tree[c].y)*1.05, 1)

                        if abs(tree[c].z) >= diffusionLimit*0.95:
                            diffusionLimit = round(abs(tree[c].z)*1.05, 1)

            if debug:
                print(
                    "Limit: {} | Size : {} | Obj : {}/{}".format(
                        diffusionLimit,
                        agentSize,
                        len(tree),
                        agentLimit
                    )
                )

        computationDone = isTreeFilled()

        if not debug:
            update_progress("Computing", len(tree) / agentLimit)

        if computationDone:
            print(
                "Limit: {} | Size : {}".format(
                    diffusionLimit,
                    agentSize
                )
            )
            break

    # Storing tree coordinnates into csv
    # (back up in case of Blender crash),
    with open(filePath, 'w') as dataFile:
        writer = csv.writer(dataFile)
        for i in range(len(tree)):
            writer.writerow([
                tree[i].size,
                tree[i].x,
                tree[i].y,
                tree[i].z
            ])

# Build tree from CSV file
with open(filePath) as File:
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
