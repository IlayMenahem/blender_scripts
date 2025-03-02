import os

from terrain import generate_blender_terrain
from vegetation import generate_trees
from light import add_light
from camera import add_camera, attach_camera_to_curve
from path import generate_curve
from utils import clear, save_scene_to_file

if __name__ == "__main__":
    texture_path: str = "textures/grass-terrain/textures/rocky_terrain_02_diff_4k.jpg"
    path: str = os.path.join(os.getcwd(), texture_path)
    file_path: str = os.path.join(os.getcwd(), "terrain.blend")
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

    camera_location: tuple = (0, 0, 5)
    camera_rotation: tuple = (0, 0, 0)
    path_duration: int = 200

    curve_offset: tuple = (xpix / 2, ypix / 2, 50)
    curve_scale: float = 20
    point_count: int = 8

    clear()

    add_light(light_type, light_location, light_strength, light_color)
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count, seed)
    attach_camera_to_curve(camera, curve, path_duration)
    mesh = generate_blender_terrain(path, xpix, ypix, height_variation, ruggedness, seed)
    generate_trees(tree_count, xpix, ypix, mesh)

    # get_video("videos/terrain.mp4", camera, path_duration)
    save_scene_to_file(file_path)
