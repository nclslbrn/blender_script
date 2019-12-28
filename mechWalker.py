import bpy  # noqa
import bmesh  # noqa
from classes.Walker import Walker
# from functions.updateProgress import update_progress
from functions.cleanScene import cleanScene
from functions.skinModifierSetVertexRadius import makeDecreaseVertSkinRadius
from functions.mechify import mechify


# Convenience Variables
D = bpy.data
C = bpy.context

# Delete previous generated curve in the scenecleanScene('MESH')
cleanScene('MESH')


'''
    Your creative code here
'''
materialName = 'ToonShade_EV_v2'
limit = 24
mooveNum = 120
walkerNum = 1
minRadius = 0.05
maxRadius = 0.1

# MOOVE LOOP
for w in range(walkerNum):

    pointPos = Walker(0, 0, 0)
    pointHistory = []

    for m in range(mooveNum):

        posAlreadyUsed = False
        posTooFar = False
        newWalker = Walker(pointPos.x, pointPos.y, pointPos.z)
        newPos = newWalker.move()

        # check if newPos is out of limit
        if(
            newPos.x < limit * -0.5 or
            newPos.y < limit * -0.5 or
            newPos.x > limit * 0.5 or
            newPos.y > limit * 0.5
        ):
            posTooFar = True

        # check if newPos already exists in pointHistory
        for p in range(len(pointHistory)):
            if(
                pointHistory[p][0] == newPos.x and
                pointHistory[p][1] == newPos.y and
                pointHistory[p][2] == newPos.y
            ):
                posAlreadyUsed = True

        # then store newPos in pointHistory
        if not posAlreadyUsed and not posTooFar:
            pointHistory.append([pointPos.x, pointPos.y, pointPos.z])
            pointHistory.append([newPos.x, newPos.y, newPos.z])
            pointPos = newPos
        else:
            del pointHistory[len(pointHistory)-1]

    edges = []
    for i in range(0, len(pointHistory), 2):
        edges.append([i, i+1])

    meshName = "DLA-Tree-{}".format(w)
    mesh = bpy.data.meshes.new(meshName)
    treeObj = bpy.data.objects.new(meshName, mesh)
    treeObj.location = (0, 0, 0)
    C.scene.collection.objects.link(treeObj)
    mesh.from_pydata(pointHistory, edges, [])
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bm.to_mesh(mesh)
    mesh.update()
    bm.clear()
    bm.free()

    makeDecreaseVertSkinRadius(treeObj, meshName, maxRadius, minRadius)
    mechify(treeObj)
