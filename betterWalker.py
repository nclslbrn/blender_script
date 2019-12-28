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
walkerSize = 0.05
materialName = 'ToonShade_EV_v2'
splitProbability = 0.25
stopProbability = 0.25
walkers = []
walkers.append(Walker(0, 0, 0))
ddObj = createDodecahedron(size=walkerSize)

while numElem < maxElem:

    for walker in walkers:

        walker.move()
        numElem += 1
        if debug:
            print("Add element n°{} move".format(numElem))
        cloneDodecahedron(
            size=walkerSize,
            location=(walker.x, walker.y, walker.z)
        )

    walkersCopy = walkers
    n = 0
    for walker in walkersCopy:

        if uniform(0, 1) <= splitProbability:

            newWalker = Walker(walker.x, walker.y, walker.z)
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
