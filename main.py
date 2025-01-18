import bpy
import os

from terrain import generate_blender_terrain
from vegetation import generate_trees
from light import add_light
from camera import add_camera
from path import generate_curve
from utils import clear, remove_file

if __name__ == "__main__":
    path: str = os.path.join(os.getcwd(), "textures/brown_mud_leaves/textures/brown_mud_leaves_01_diff_4k.jpg")
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 0.5

    tree_count: int = 100

    seed: int = 0

    light_type: str = "SUN"
    light_location: tuple = (0, 0, 10)
    light_strength: float = 1.0
    light_color: tuple = (1, 1, 1)

    camera_location: tuple = (0, 0, 10)
    camera_rotation: tuple = (0, 0, 0)

    curve_offset: tuple = (xpix / 2, ypix / 2, 10)
    curve_scale: float = 20
    point_count: int = 8

    clear()

    add_light(light_type, light_location, light_strength, light_color)
    add_camera(camera_location, camera_rotation)
    generate_curve(curve_offset, curve_scale, point_count, seed)
    mesh = generate_blender_terrain(path, xpix, ypix, height_variation, ruggedness, seed)
    generate_trees(tree_count, xpix, ypix, mesh)

    remove_file("blends/terrain.blend")
    bpy.ops.wm.save_as_mainfile(filepath="blends/terrain.blend", check_existing=False)
