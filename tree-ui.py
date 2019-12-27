import bpy


class DLAtreePanel(bpy.types.Panel):
    bl_label = "Diffusion Limited Aggregation Generator"
    bl_idname = "DLA_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_deorate = False

        scene = context.scene
        col = layout.column()


def register():
    bpy.utils.register_class(DLAtreePanel)


def unregister():
    bpy.utils.unregister_class(DLAtreePanel)


if __name__ == "__main__":
    register()
