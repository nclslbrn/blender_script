import bpy  # noqa


def cleanScene(type_to_delete='MESH'):
    objs = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            objs.append(obj)
    bpy.ops.object.delete({"selected_objects": objs})
