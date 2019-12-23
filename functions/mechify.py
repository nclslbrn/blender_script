import bpy  # noqa
import bmesh  # noqa
from math import pi


D = bpy.data
C = bpy.context


def mechify(currObj):
    edgeSplitMod = currObj.modifiers.new("Tree edge split", 'EDGE_SPLIT')
    edgeSplitMod.split_angle = pi/4
    edgeSplitMod.use_edge_angle = True
    edgeSplitMod.use_edge_sharp = True

    bevelMod = currObj.modifiers.new("Tree bevel", 'BEVEL')
    bevelMod.loop_slide = False
    bevelMod.use_clamp_overlap = False
    bevelMod.offset_type = 'OFFSET'
    bevelMod.width = 0.07
    bevelMod.material = 2

    solidifyMod = currObj.modifiers.new("tree solidify", 'SOLIDIFY')
    solidifyMod.thickness = 0.7
    solidifyMod.use_rim = True
    solidifyMod.material_offset = 3
    solidifyMod.material_offset_rim = 1
