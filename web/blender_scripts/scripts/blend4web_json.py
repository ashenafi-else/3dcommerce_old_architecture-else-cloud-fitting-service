import bpy
import sys
import os.path

argv = sys.argv
path = argv[argv.index('--') + 1]
argv = argv[argv.index('--') + 2:]


def combine_with(file_path, link=True):
    if os.path.isfile(file_path):
        with bpy.data.libraries.load(file_path, link=link) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects]

        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.objects.link(obj)

if 'blend4web' not in bpy.context.user_preferences.addons:
    bpy.ops.wm.addon_enable(module='blend4web')
    bpy.ops.wm.save_userpref()

if argv:
    combine_with(argv[0])

bpy.ops.export_scene.b4w_json(filepath=path, do_autosave=False, save_export_path=False)