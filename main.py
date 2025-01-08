import bpy
import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

from terrain import generate_blender_terrain
from vegetation import generate_trees
from utils import clear, remove_file

if __name__ == "__main__":
    path: str = os.path.join(os.getcwd(), "textures/brown_mud_leaves/textures/brown_mud_leaves_01_diff_4k.jpg")
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 0.5

    tree_count = 100

    seed: int = 0

    clear()

    mesh = generate_blender_terrain(path, xpix, ypix, height_variation, ruggedness, seed)
    generate_trees(tree_count, xpix, ypix, mesh)

    remove_file("blends/terrain.blend")
    bpy.ops.wm.save_as_mainfile(filepath="blends/terrain.blend", check_existing=False)
