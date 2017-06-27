import bpy
import sys
from math import pi


scene = bpy.data.scenes['Scene']

if 'blend4web' not in bpy.context.user_preferences.addons:
    bpy.ops.wm.addon_enable(module='blend4web')
    bpy.ops.wm.save_userpref()


def customize_object(active_object, diffuse_color=(1.0, 1.0, 1.0), alpha=1.0, location=(0, 0, 0), rotation=(0, 0, 0)):
    active_object.select = True
    material = bpy.data.materials.new(name='Material' + active_object.name)
    active_object.data.materials.append(material)
    material.diffuse_color = diffuse_color
    material.use_transparency = True
    material.alpha = alpha
    active_object.location = location
    active_object.rotation_euler = rotation
    active_object.select = False


for ob in scene.objects:
    if '_foot' in ob.name:
        active_object = ob

customize_options = {
    'left_foot': {
        'location': (1.4, -1, 0),
        'rotation': (0, 0, pi),
        'diffuse_color': (0.8, 2, 1.6),
    },
    'right_foot': {
        'location': (1.4, 1, 0),
        'rotation': (0, 0, pi),
        'diffuse_color': (0.8, 2, 1.6),
    },
}

if active_object.name in customize_options:
    customize_object(
        active_object=active_object,
        location=customize_options[active_object.name]['location'],
        rotation=customize_options[active_object.name]['rotation'],
        diffuse_color=customize_options[active_object.name]['diffuse_color'],
    )
active_object.b4w_do_not_batch = True
active_object.b4w_dynamic_geometry = True

bpy.ops.wm.save_mainfile()