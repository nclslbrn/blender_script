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


D = bpy.data
C = bpy.context
# display agentSize and limit size (and hide progress)
debug = False

# Argument from command line
# blender --python dla.py -- <compute> <file.csv>
if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1:]

    if args[0]:
        if args[0] == 'compute':
            computeAndWrite = True
        else:
            computeAndWrite = False

    if args[1] and ".csv" in args[1]:
        file = args[1]
    else:
        file = 'tree.csv'
else:
    computeAndWrite = True
    file = 'tree.csv'

# How many agents live at same time
agentNum = 500
# How many agents will stuck on tree
agentLimit = 3000

# Distance limit of of agents move (increase over time)
diffusionLimit = 7.0
maxDiffusionDistance = 24
# Size of the first agent (decrease over time)
agentSize = 0.4
# Factor to decrease agents size
shrink = 0.999
minAgentSize = 0.05

# Array to store moving agent
agents = []
# Array to store dead agents
tree = []
# State of computation at the begining of the script
computationDone = False if computeAndWrite else True

# Create the first cluster at the center
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = agentSize

filePath = '/Users/nlebrun/Documents/Blender/data-output/' + file

if computeAndWrite:
    print(
        "Python will compute {} DLA points and store them into {}.".format(
            agentLimit,
            file
        )
    )
else:
    print(
        "Blender will build {} DLA points shape from {}.".format(
            agentLimit,
            file
        )
    )

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

if computeAndWrite:

    with open(filePath, 'w') as dataFile:
        writer = csv.writer(dataFile)

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
                            writer.writerow([
                                agents[a].size,
                                agents[a].x,
                                agents[a].y,
                                agents[a].z
                            ])
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

                            if abs(tree[c].x) >= diffusionLimit*0.99:
                                diffusionLimit = round(abs(tree[c].x)*1.025, 1)

                            if abs(tree[c].y) >= diffusionLimit*0.99:
                                diffusionLimit = round(abs(tree[c].y)*1.025, 1)

                            if abs(tree[c].z) >= diffusionLimit*0.99:
                                diffusionLimit = round(abs(tree[c].z)*1.025, 1)

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
