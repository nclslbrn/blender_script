import bpy
import os
import sys
import bmesh  # noqa
dir = os.path.dirname(bpy.data.filepath)
print(dir)
if dir not in sys.path:
    sys.path.append(dir)

from classes.Pool import Pool  # noqa: E731

D = bpy.data
C = bpy.context


'''
    Delete everythings in the scene

'''
objs = []
for obj in C.scene.objects:
    objs.append(obj)
bpy.ops.object.delete({"selected_objects": objs})

'''
    Your creative code here

'''
N = 12
width = Pool(maxItems=N)
width.update()

height = []
depth = []

for i in range(N):
    height.append(Pool(maxItems=N))
    height[i].update()

    for j in range(N):
        depth.append(Pool(maxItems=N))
        depth[i*N + j].update()


# create a default
mesh = bpy.data.meshes.new('Voxel')
basic_cube = bpy.data.objects.new('original-voxel', mesh)
basic_cube.location = (0, 0, 0)

# Add the object into the scene.
C.scene.collection.objects.link(basic_cube)

# Construct the bmesh cube and assign it to the blender mesh.
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=0.25)
bm.to_mesh(mesh)
bm.free()

cubeID = 0


x = 1
for nX in range(N):
    y = 1
    dx = width.items[nX]

    for nY in range(N):
        z = 1
        dy = height[nX].items[nY]

        for nZ in range(N):
            dz = depth[nX * N + nY].items[nZ]

            clone = basic_cube.copy()
            clone.name = 'VoxCopy-' + str(cubeID)
            # clone.data = basic_cube.data.copy()
            clone.scale = (dx, dy, dz)
            clone.location = (x, y, z)
            C.scene.collection.objects.link(clone)

            cubeID += 1

            z -= dz
        y -= dy
    x -= dx
