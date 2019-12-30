import bpy  # noqa

# Delete every object of a specified type
# Type: MESH, CURVE, SURFACE, META, FONT, ARMATURE, LATTICE,
# EMPTY, GPENCIL, CAMERA, LIGHT, SPEAKER, LIGHT_PROBE


def cleanScene(type_to_delete='MESH'):
    objs = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            objs.append(obj)
    bpy.ops.object.delete({"selected_objects": objs})
