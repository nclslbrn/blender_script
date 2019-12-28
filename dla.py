import bpy  # noqa
import bmesh  # noqa
import csv
# progress bar implementation (visible on terminal)
from functions.updateProgress import update_progress
# particle class
from classes.Agent import Agent
# function to get distance between two coordinate
from functions.measure import measure
# function to erase object (specified by type) on the scene
from functions.cleanScene import cleanScene
# function to create and copy dodecahedron
from functions.dodecahedron import createDodecahedron, cloneDodecahedron

D = bpy.data
C = bpy.context

# display agentSize and limit size (and hide progress)
debug = False
# Used to build DLA from CSV file
writeAndCompute = False
# How many agents live at same time
agentNum = 100
# How many agents will stuck on tree
agentLimit = 10000
# Size of the first agent (make decrease with time)
agentSize = 1.0
# Distance limit for the moves of the agents
limit = 24
# Factor to decrease agents size
shrink = 0.9995
# Factor to increase limit size
expand = 1.05
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
        newAgent.onLimit(
            size=agentSize,
            limit=limit
        )
        agents.append(newAgent)

# move agents reinit them if
# they go away from limit


def moveAgents(completion):

    min = (limit+1) * -0.5
    max = (limit+1) * 0.5

    for a in range(len(agents)):

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

# check if agent is stuck on tree


def copyAgentsToTree(completion):

    currentSize = agentSize
    currentLimit = limit

    for a in range(len(agents)):

        for t in range(len(tree)):

            distance = measure(agents[a], tree[t])

            if distance <= (agents[a].size + tree[t].size)*4:

                # Add the agent to the tree
                tree.append(agents[a])

                # change constants
                if currentSize > 0.05:
                    currentSize *= shrink
                if currentLimit < 74:
                    currentLimit *= expand

                # reset the agent
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

# used to get the progress of computation


def checkTreeLenght(computationDone):

    if len(tree) > agentLimit:
        computationDone = True

    return computationDone


cleanScene('MESH')
initAgents()
ddObj = createDodecahedron(size=agentSize)
progress = 0

if writeAndCompute:
    while not computationDone:

        moveAgents(progress)
        agentSize, limit = copyAgentsToTree(progress)
        computationDone = checkTreeLenght(computationDone)

        if not debug:
            progress = len(tree) / agentLimit
            update_progress("Computing DLA tree", progress)

        if computationDone:
            break

    # Storing tree coordinnates into csv
    # (back up in case of Blender crash)0,

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
with open('../data-output/10000-tree.csv') as File:
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
