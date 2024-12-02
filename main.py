import os
import bpy

from terrain import generate_terrain, generate_blender_terrain, apply_texture
from vegetation import generate_trees

if __name__ == "__main__":
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 1.0

    tree_count = 100
    tree_height = 10
    tree_radius = 2

    seed: int = 0

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    terrain = generate_terrain(xpix, ypix, height_variation, ruggedness, seed)
    mesh = generate_blender_terrain(terrain)
    mesh = apply_texture(mesh)
    bpy.context.view_layer.objects.active = mesh

    # generate_trees(tree_count, xpix, ypix, mesh, tree_height, tree_radius)

    if os.path.exists("terrain.blend"):
        os.remove("terrain.blend")
    bpy.ops.wm.save_as_mainfile(filepath="terrain.blend", check_existing=False)
