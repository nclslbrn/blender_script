import bpy  # noqa
import bmesh  # noqa


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
isFinal = False
debug = False

agentNum = 75
agentLimit = 500 if isFinal else 200
agentSize = 3 if isFinal else 0.5
limit = 42 if isFinal else 16
shrink = 0.97
agents = []
tree = []
# lines = []
vertices_radius = []
buildCompleted = False
treeCount = 0
tree.append(Agent)
tree[0].x = 0
tree[0].y = 0
tree[0].z = 0
tree[0].size = agentSize
vertices_radius.append(agentSize)


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

            if distance <= (agents[a].size + tree[t].size)*2:

                # Add the agent to the tree
                tree.append(agents[a])

                # Add thes to coordinate to lines
                # lines.append([tree[t].x, tree[t].y, tree[t].z])
                # lines.append([agents[a].x, agents[a].y, agents[a].z])
                vertices_radius.append(agents[a].size)

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
    agentSize = copyParticleToStructure(progress)
    buildCompleted = checkTreeLenght(buildCompleted)
    progress = len(tree) / agentLimit
    update_progress("Computing DLA tree", progress)

    if buildCompleted:
        break

'''
# build the mesh
meshName = "DLA-Tree"
mesh = bpy.data.meshes.new(meshName)
edges = []
for i in range(0, len(lines), 2):
    edges.append([i, i+1])
# Create tree object
treeObj = bpy.data.objects.new(meshName, mesh)
treeObj.location = (0, 0, 0)
# Add it to the scene collection
C.scene.collection.objects.link(treeObj)
# Create a mesh
mesh.from_pydata(lines, edges, [])
mesh.update(calc_edges=True)
# Remove double vertices
bm = bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
bm.to_mesh(mesh)
mesh.update()
bm.clear()
bm.free()
'''

# Add skin modifier and assign tree[].size to vertice radius
# setupVertSkinRadius(treeObj, meshName, vertices_radius)
# makeDecreaseVertSkinRadius(treeObj, meshName, 0.8, 0.1)
# Add split edge, bevel and solidify modifier
# mechify(treeObj)

ddObj = createDodecahedron()
for i in range(len(tree)):
    cloneDodecahedron(
        original=ddObj,
        size=tree[i].size,
        location=(tree[i].x, tree[i].y, tree[i].z)
    )

update_progress("Building DLA tree", 1)
