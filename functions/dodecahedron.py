# Dodecahedron
# (c) TomDalek
# 2011-03-06 (blender 2.56a-beta)
# Update 2019-12-26 to tun on blender 2.8
# http://en.wikipedia.org/wiki/Dodecahedron
# http://www.rwgra    clone = original.copy()
# clone.name = 'Voxel-copy-' + str(nt)
import math
import bpy  # noqa


def createDodecahedron():
    # phi is the Golden Ratio = ~1.618
    phi = (1 + math.sqrt(5)) / 2.0
    phi2 = phi * phi
    phi3 = phi * phi * phi

    coords = [
        (0,   phi,  phi3),  # V4   0
        (0,  -phi,  phi3),  # V8   1

        (phi2,  phi2,  phi2),  # V11  2
        (-phi2,  phi2,  phi2),  # V13  3
        (-phi2, -phi2,  phi2),  # V16  4
        (phi2, -phi2,  phi2),  # V18  5

        (phi3,     0,   phi),  # V20  6
        (-phi3,     0,   phi),  # V23  7
        (phi,  phi3,     0),  # V28  8
        (-phi,  phi3,     0),  # V30  9
        (-phi, -phi3,     0),  # V34 10
        (phi, -phi3,     0),  # V36 11
        (phi3,     0,  -phi),  # V38 12
        (-phi3,     0,  -phi),  # V41 13

        (phi2,  phi2, -phi2),  # V45 14
        (-phi2,  phi2, -phi2),  # V47 15
        (-phi2, -phi2, -phi2),  # V50 16
        (phi2, -phi2, -phi2),  # V52 17

        (0,   phi, -phi3),  # V56 18
        (0,  -phi, -phi3)  # V60 19
    ]

    faces = [
        (1, 0, 4), (0, 3, 4), (3, 7, 4),
        (0, 1, 2), (1, 5, 2), (5, 6, 2),

        (0, 2, 3), (2, 8, 3), (8, 9, 3),
        (1, 4, 5), (4, 10, 5), (10, 11, 5),

        (3, 9, 7), (9, 15, 7), (15, 13, 7),
        (4, 7, 10), (7, 13, 10), (13, 16, 10),
        (5, 11, 6), (11, 17, 6), (17, 12, 6),
        (2, 6, 8), (6, 12, 8), (12, 14, 8),

        (9, 8, 15), (8, 14, 15), (14, 18, 15),
        (11, 10, 17), (10, 16, 17), (16, 19, 17),

        (13, 15, 16), (15, 18, 16), (18, 19, 16),
        (12, 17, 14), (17, 19, 14), (19, 18, 14)
    ]

    me = bpy.data.meshes.new("DodecahedronMesh")

    ob = bpy.data.objects.new("Dodecahedron", me)
    ob.location = (0, 0, 0)
    # bpy.context.scene.objects.link(ob)
    bpy.context.scene.collection.objects.link(ob)
    me.from_pydata(coords, [], faces)
    me.update(calc_edges=True)

    return ob


def cloneDodecahedron(
    original=createDodecahedron(),
    size=1,
    location=(0, 0, 0)
):
    clone = original.copy()
    # clone.name = 'Voxel-copy-' + str(nt)
    clone.data = original.data.copy()
    clone.scale = (size, size, size)
    clone.location = (location)
    bpy.context.scene.collection.objects.link(clone)
