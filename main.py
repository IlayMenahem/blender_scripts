import bpy

from terrain import generate_blender_terrain
from vegetation import generate_trees
from utils import clear, remove_file

if __name__ == "__main__":
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 0.5

    tree_count = 100
    tree_height = 10
    tree_radius = 2

    seed: int = 0

    clear()

    mesh = generate_blender_terrain(xpix, ypix, height_variation, ruggedness, seed)

    generate_trees(tree_count, xpix, ypix, mesh, tree_height, tree_radius)

    remove_file("blends/terrain.blend")
    bpy.ops.wm.save_as_mainfile(filepath="blends/terrain.blend", check_existing=False)
