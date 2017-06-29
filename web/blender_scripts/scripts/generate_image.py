import bpy
import sys
from math import pi

argv = sys.argv[sys.argv.index('--') + 1:]
path_to_result_image = argv[0]
resolution = argv[1], argv[2]


scene = bpy.data.scenes['Scene']


def render_image(resolution, file_name):
    bpy.context.scene.camera.location = (1.4, 0, 4.6)
    bpy.context.scene.camera.rotation_euler = (0, 0, -pi/2)
    bpy.context.scene.render.resolution_x = int(resolution[0])
    bpy.context.scene.render.resolution_y = int(resolution[1])
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.quality = 90
    bpy.context.scene.render.filepath = file_name
    bpy.ops.render.render(write_still=True)


for ob in scene.objects:
    if ob.type == 'MESH' and ob.name.startswith("Cube"):
        ob.select = True
    else:
        ob.select = False
        ob.location = (0, 0, 0)
        ob.rotation_euler = (0, 0, 0)

bpy.ops.object.delete()
bpy.data.objects['Lamp'].location = (0, 0, 6)

render_image(resolution, path_to_result_image)