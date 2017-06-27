import bpy
import sys
from math import pi

argv = sys.argv[sys.argv.index('--') + 1:]
path_to_result_blend_file = argv[0]
path_to_stl = argv[1]

scene = bpy.data.scenes['Scene']

bpy.ops.import_mesh.stl(filepath=path_to_stl, global_scale=0.01)


for ob in scene.objects:
    if ob.type == 'MESH' and ob.name.startswith("Cube"):
        ob.select = True
    else:
        ob.select = False
        if 'FOOT' in ob.name:
            ob.name = ob.name.lower().replace(' ', '_')

bpy.ops.object.delete()

bpy.context.scene.camera.location = (1.4, 0, 6)
bpy.context.scene.camera.rotation_euler = (0, 0.0, pi / 2)
bpy.data.objects['Lamp'].location = (0, 0, 6)

bpy.ops.wm.save_as_mainfile(filepath=path_to_result_blend_file, check_existing=True,)
