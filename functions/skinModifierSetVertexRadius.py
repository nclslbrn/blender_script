import bpy  # noqa
import bmesh  # noqa


D = bpy.data
C = bpy.context


def makeDecreaseVertSkinRadius(currObj, meshName, maxRadius, minRadius):

    currObj.modifiers.new("Tree skin", 'SKIN')
    obj = D.objects[meshName]
    step = (maxRadius - minRadius) / len(obj.data.skin_vertices[0].data)
    index = len(obj.data.skin_vertices[0].data)
    for v in obj.data.skin_vertices[0].data:
        radius = minRadius + (index * step)
        v.radius = radius, radius
        index -= 1


def makeIncreaseVertSkinRadius(currObj, meshName, maxRadius, minRadius):

    currObj.modifiers.new("Tree skin", 'SKIN')
    obj = D.objects[meshName]
    step = (maxRadius - minRadius) / len(obj.data.skin_vertices[0].data)
    index = 0
    for v in obj.data.skin_vertices[0].data:
        radius = minRadius + (index * step)
        v.radius = radius, radius
        index += 1
