import bpy

# Convenience Variables
D = bpy.data
C = bpy.context


def setupCurve(w, points, material):
    curveRes = 2
    extrude = 0
    # Setup curve path
    curveName = "curve-" + str(w)
    curveData = D.curves.new(name='curveName', type='CURVE')
    curveData.bevel_depth = 0.1
    curveData.dimensions = '3D'
    curveData.resolution_u = curveRes
    curveData.render_resolution_u = curveRes
    curveData.extrude = extrude

    # Setup curve object
    curve = bpy.data.objects.new(curveName, curveData)
    curve.active_material = material
    curve.location = (0, 0, 0)

    # Add modifier
    modifierName = 'solid-' + str(w)
    curve.modifiers.new(name=modifierName, type='SOLIDIFY')
    curve.modifiers[modifierName].thickness = 0.04

    # Add it to the scene
    C.scene.collection.objects.link(curve)
    polyline = curveData.splines.new('NURBS')

    return polyline


def drawCurve(polyline, points, minRadius, maxRadius, radiusStep):

    if len(points):
        polyline.points.add(len(points))

        for p in range(len(points)):
            polyline.points[p].co = (
                points[p][0],
                points[p][1],
                points[p][2],
                1
            )
            radius = minRadius + (len(points) - p) * radiusStep
            polyline.points[p].radius = radius

    else:
        polyline.points.add(1)
        polyline.points[0].co = (
            points[0],
            points[1],
            points[2],
            1
        )
        polyline.points[p].radius = minRadius + (maxRadius - minRadius)/2

    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = False
