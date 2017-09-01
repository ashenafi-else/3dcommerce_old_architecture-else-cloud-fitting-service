import sys
import bpy
import bmesh
import mathutils
from mathutils.bvhtree import BVHTree


argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []


output_image_file_path = argv[0]
output_json_file_path = output_image_file_path.replace('.png', '.json')
model_file_path = argv[1]
scan_file_path = argv[2]

print("Will be using:")
print("model: {0}".format(model_file_path))
print("scan: {0}".format(scan_file_path))

if 'blend4web' not in bpy.context.user_preferences.addons:
    bpy.ops.wm.addon_enable(module='blend4web')
    bpy.ops.wm.save_userpref()

# ------------------------------------------------------------------------------
# FUNCTIONS


def move_to_zero(obj):
    """Moves object to scene zero

    :param obj: object which should be moved
    :type obj: bpy.types.Object
    """
    obj_bounds = get_bound_box(obj)
    obj_mesh = bmesh.new()
    obj_mesh.from_mesh(obj.data)

    # centering
    for ver in obj_mesh.verts:
        ver.co.y -= (obj_bounds[0].y + obj_bounds[2].y) / 2
        ver.co.x -= (obj_bounds[0].x + obj_bounds[4].x) / 2
        ver.co.z -= obj_bounds[0].z

    obj_mesh.to_mesh(obj.data)
    obj.data.update()
    obj_mesh.free()


def rescale(obj, vec):
    """rescale object by axis

    :param obj: object to rescale
    :type obj: bpy.types.Object
    :param vec: tuple with coefficients by all axis (x, y, z)
    :type vec: (float, float, float)
    """
    obj_mesh = bmesh.new()
    obj_mesh.from_mesh(obj.data)

    for ver in obj_mesh.verts:
        ver.co.x *= vec[0]
        ver.co.y *= vec[1]
        ver.co.z *= vec[2]

    obj_mesh.to_mesh(obj.data)
    obj.data.update()
    obj_mesh.free()


def adding_model_curvature(scan, model):
    """add curvature to scan by model feet

    :param scan: scan object
    :type scan: bpy.types.Object
    :param model: model object
    :type model: bpy.types.Object
    """
    min_coord = int(min(ver.co.x for ver in model.verts))
    max_coord = int(max(ver.co.x for ver in model.verts))

    step = 1

    for n in range(min_coord, max_coord, step):
        ver_in_range = [ver.co.z for ver in model.verts if (n - step) < ver.co.x < n or int(ver.co.x) == n]

        if len(ver_in_range) != 0:
            min_in_range = min(ver_in_range)

            ver_in_range2 = [ver for ver in scan.verts if (n - step) < ver.co.x < n or int(ver.co.x) == n]
            if len(ver_in_range2) != 0:
                min_in_range2 = min(ver.co.z for ver in ver_in_range2)

                for ver in ver_in_range2:
                    ver.co.z += (min_in_range - min_in_range2) + 0.3


def assign_colors(mesh, colors):
    """assign colors to mesh vertex

    :param mesh: mesh to apply vertex colors
    :type mesh: bmesh.types.BMesh
    :param colors: colors list (rgb tuple with 0..1 per channel)
    :type colors: list of (float, float, float)
    """
    vertex_colour = mesh.vertex_colors[0].data
    faces = mesh.faces

    for i in range(len(faces)):
        v = vertex_colour[i]
        f = faces[i].verts_raw
        v.color1 = colors[f[0]]
        v.color2 = colors[f[1]]
        v.color3 = colors[f[2]]
        v.color4 = colors[f[3]]


def get_bound_box(obj):
    """return bound bov vectors list

    :param obj: object to extract bound box
    :type obj: bpy.types.Object
    :return: bound box vectors to vertices
    :rtype: list of mathutils.Vector
    """
    result = [mathutils.Vector(obj.matrix_world * mathutils.Vector(corner)) for corner in obj.bound_box]

    return result


def render_image(camera, resolution, file_name, multiplier=1):
    """ render image by particular camera

    :param camera: camera
    :type camera: bpy.types.Object
    :param resolution: tuple*2 with picture resolution (width, height)
    :type resolution: (int, int)
    :param file_name: name of result PNG file
    :type file_name: string
    :param multiplier: resolution multiplier
    :type multiplier: int
    """      
    bpy.context.scene.camera = camera
    bpy.context.scene.render.resolution_x = int(resolution[0]) * multiplier
    bpy.context.scene.render.resolution_y = int(resolution[1]) * multiplier
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.quality = 90
    bpy.context.scene.render.filepath = file_name
    bpy.ops.render.render(write_still=True)


def align_object_by_vector(obj, vec):
    """align object by vector (x axis)

    :param obj: object for alignment
    :type obj: bpy.types.Object
    :param vec: vector for alignment
    :type vec: mathutils.Vector
    """
    q = vec.to_track_quat('X', 'Z')

    loc, rot, scale = obj.matrix_world.decompose()

    mat_scale = mathutils.Matrix()
    for i in range(3):
        mat_scale[i][i] = scale[i]

    obj.matrix_world = (
        mathutils.Matrix.Translation(loc) *
        q.to_matrix().to_4x4() *
        mat_scale)

# END FUNCTIONS
# ------------------------------------------------------------------------------

def generate_comparison_image(model_path, scan_path, output_path):
    bpy.ops.import_mesh.stl(filepath=model_path)
    model = bpy.data.objects[bpy.context.selected_objects[0].name]

    bpy.ops.import_mesh.stl(filepath=scan_path)
    scan = bpy.data.objects[bpy.context.selected_objects[0].name]

    # alignment by axis
    vec = mathutils.Vector((1, 0, 0))
    align_object_by_vector(scan, vec)
    align_object_by_vector(model, vec)

    # move to zero
    move_to_zero(model)
    move_to_zero(scan)

    # load meshes
    model_mesh = bmesh.new()
    model_mesh.from_mesh(model.data)
    scan_mesh = bmesh.new()
    scan_mesh.from_mesh(scan.data)

    # color arrays
    scan_colors = [(105/255, 105/255, 105/255) for i in scan_mesh.verts]
    model_colors = [(0, 0, 0) for i in model_mesh.verts]

    # adding curvature
    adding_model_curvature(scan_mesh, model_mesh)

    # cqlculate colors on model by distance to closest point on scan
    bvh = BVHTree.FromBMesh(scan_mesh, epsilon=0.0001)

    # max distance which should be colored
    max_coloring_distance = 5

    for ver in model_mesh.verts:
        fco, normal, _, _ = bvh.find_nearest(ver.co)
        p2 = fco - mathutils.Vector(ver.co)
        dist = -p2.dot(normal)

        if dist > 0:
            dist = min(dist, max_coloring_distance)
            quart = (1 - (dist / max_coloring_distance))
            model_colors[ver.index] = (quart, quart * 0.5, 0)
        else:
            quart = (1 - (-dist / max_coloring_distance))
            model_colors[ver.index] = (1, quart * 0.5, 0)

    # apply colors
    color_layer = model_mesh.loops.layers.color.new("Col")
    for face in model_mesh.faces:
            for loop in face.loops:
                loop[color_layer] = model_colors[loop.vert.index]

    color_layer = scan_mesh.loops.layers.color.new("Col")
    for face in scan_mesh.faces:
            for loop in face.loops:
                loop[color_layer] = scan_colors[loop.vert.index]

    # apply scan changes
    scan_mesh.to_mesh(scan.data)
    scan.data.update()
    model_mesh.to_mesh(model.data)
    model.data.update()

    #  free objects
    scan_mesh.free()
    model_mesh.free()

    # re-scale
    rescale(scan, (0.001, 0.001, 0.001))
    rescale(model, (0.001, 0.001, 0.001))

    # rendering

    # add materials
    model.select = True
    material = bpy.data.materials.new(name='Material_' + model.name)
    material.use_vertex_color_paint = True
    material.use_vertex_color_light = True
    model.data.materials.append(material)
    model.select = False

    scan.select = True
    material = bpy.data.materials.new(name='Material_' + scan.name)
    material.diffuse_color = (1.0, 1.0, 1.0)
    material.use_transparency = True
    material.alpha = 1.0
    material.diffuse_intensity = 0.05
    scan.data.materials.append(material)
    # scan.select = False
    bpy.ops.object.delete()

    # render image
    camera = bpy.data.objects["cameraTOP"]
    render_image(camera, (1920, 1080), output_path)

generate_comparison_image(model_file_path, scan_file_path, output_image_file_path)
bpy.ops.export_scene.b4w_json(filepath=output_json_file_path, do_autosave=False, save_export_path=False)
