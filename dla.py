import bpy  # noqa
import bmesh  # noqa
import csv
# progress bar implementation (visible on terminal)
from functions.updateProgress import update_progress
# particle class
from classes.Agent import Agent
# function to erase object (specified by type) on the scene
from functions.cleanScene import cleanScene
# function to create and copy dodecahedron
from functions.dodecahedron import createDodecahedron, cloneDodecahedron

D = bpy.data
C = bpy.context

# display agentSize and limit size (and hide progress)
debug = False
# Used to build DLA from CSV file
writeAndCompute = True
# How many agents live at same time
agentNum = 25
# How many agents will stuck on tree
agentLimit = 100

# Distance limit of of agents move
limit = 6.0
# Factor to increase limit size
expand = 1.001
maxLimit = 260
# Size of the first agent (decrease with time)
agentSize = 0.35
# Factor to decrease agents size
shrink = 0.99
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


# init agents around the cluster
def initAgents():

    for a in range(agentNum-1):

        newAgent = Agent(size=agentSize, x=0, y=0, z=0)
        newAgent.onRadius(
            size=agentSize,
            limit=limit
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

            for m in range(16):

                agents[a].move()
                agents[a].reInitIfOutside(limit)

                for c in range(len(tree)):

                    if isTreeFilled():
                        break

                    dx = round(abs(tree[c].x - agents[a].x), 1)
                    dy = round(abs(tree[c].y - agents[a].y), 1)
                    dz = round(abs(tree[c].z - agents[a].z), 1)

                    minD = round(abs(agents[a].size + tree[c].size)*2, 1)

                    if(
                        dx <= minD and
                        dy <= minD and
                        dz <= minD
                    ):

                        # Add the agent to the tree
                        tree.append(agents[a])

                        # change constants
                        if agentSize > minAgentSize:
                            agentSize *= shrink

                        """ if limit < maxLimit:
                            limit *= expand """

                        # reset the agent
                        del agents[a]
                        newAgent = Agent(x=0, y=0, z=0, size=agentSize)
                        newAgent.onRadius(
                            limit=limit,
                            size=agentSize
                        )
                        agents.append(newAgent)

            if debug:
                print(
                    "Limit: {} | Size : {} | Obj : {}/{}".format(
                        limit,
                        agentSize,
                        len(tree),
                        agentLimit
                    )
                )

        computationDone = isTreeFilled()

        if not debug:
            update_progress("Computing DLA tree", len(tree) / agentLimit)

        if computationDone:
            print(
                "Limit: {} | Size : {}".format(
                    limit,
                    agentSize
                )
            )
            break

    # Storing tree coordinnates into csv
    # (back up in case of Blender crash),
    with open('../data-output/tree.csv', 'w') as dataFile:
        writer = csv.writer(dataFile)
        for i in range(len(tree)):
            writer.writerow([
                tree[i].size,
                tree[i].x,
                tree[i].y,
                tree[i].z
            ])

# Build tree from CSV file
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
