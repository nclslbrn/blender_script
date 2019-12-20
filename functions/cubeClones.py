
import bpy  # noqa
import bmesh  # noqa


D = bpy.data
C = bpy.context


def create_original(
    name='default_cube',
    d=0.1,
    location=(0, 0, 0),
    faces=True
):

    # Create an empty mesh and add the object.
    mesh = bpy.data.meshes.new('Voxel')
    basic_cube = bpy.data.objects.new(name, mesh)
    basic_cube.location = location

    # Add the object into the scene.
    C.scene.collection.objects.link(basic_cube)

    # Construct the bmesh cube and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=d)
    bm.to_mesh(mesh)
    bm.free()

    return basic_cube


def clone_original(original=create_original(), size=1, location=(0, 0, 0)):
    clone = original.copy()
    # clone.name = 'Voxel-copy-' + str(nt)
    clone.data = original.data.copy()
    clone.animation_data_clear()
    clone.scale = (size, size, size)
    clone.location = (location)
    C.scene.collection.objects.link(clone)


'''
How use it

def buildShape():

    srcObject = create_original(
        name='origVoxel',
        d=agentSize,
        location=(0, 0, 0),
        faces=True,
    )

    for t in range(len(tree)):
        clone_original(
            original=srcObject,
            size=tree[t].size,
            location=(tree[t].x, tree[t].y, tree[t].z)
        )

'''
