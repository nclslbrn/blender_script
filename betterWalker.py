import bpy  # noqa
import bmesh  # noqa
from classes.Walker import Walker
from random import uniform
# from functions.updateProgress import update_progress
from functions.cleanScene import cleanScene
from functions.updateProgress import update_progress
from functions.dodecahedron import createDodecahedron, cloneDodecahedron


# Convenience Variables
D = bpy.data
C = bpy.context

cleanScene('MESH')
debug = False
numElem = 0
maxElem = 10000
walkerSize = 0.1
materialName = 'ToonShade_EV_v2'
splitProbability = 0.5
stopProbability = 0.4
walkers = []
walkers.append(Walker(0, 0, 0))
walkers[0].setSize(walkerSize)

material = D.materials.get('origin-away-blue-orange')
ddObj = createDodecahedron(size=walkerSize)
ddObj.active_material = material

while numElem < maxElem:

    prevWalkerSize = walkerSize

    for walker in walkers:

        walker.move(prevWalkerSize*2)
        numElem += 1

        if debug:
            print("New element in tree ({})".format(numElem))

        cloneDodecahedron(
            size=walkerSize,
            location=(walker.x, walker.y, walker.z)
        )

        prevWalkerSize = walker.size

    walkersCopy = walkers
    n = 0
    for walker in walkersCopy:

        if uniform(0, 1) <= splitProbability:

            newWalker = Walker(walker.x, walker.y, walker.z)
            newWalker.move(walkerSize)
            walkerSize *= 0.995
            newWalker.setSize(walkerSize)
            walkers.append(newWalker)

            if debug:
                print("Walker n°{} split".format(n))

        if n > 0 and uniform(0, 1) <= stopProbability:

            del walkers[n]
            if debug:
                print("Walker n°{} died".format(n))
        n += 1

    if numElem >= maxElem:
        break

    elif not debug:
        update_progress("Processing ", numElem/maxElem)
