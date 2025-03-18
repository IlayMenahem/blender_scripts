import os

from terrain import generate_blender_terrain
from vegetation import generate_trees, put_on_mesh, load_tree_on_fire
from light import add_light
from camera import add_camera, get_video, look_at_curve
from path import generate_curve
from utils import clear, save_scene_to_file

if __name__ == "__main__":
    terrain_texture_path: str = "textures/grass-terrain/textures/rocky_terrain_02_diff_4k.jpg"
    terrain_texture_path: str = os.path.join(os.getcwd(), terrain_texture_path)
    file_path: str = os.path.join(os.getcwd(), "terrains", "terrain.blend")
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 0.5

    tree_count: int = 300
    tree_on_fire_position: tuple = (xpix / 2, ypix / 2)

    seed: int = 0

    light_type: str = "SUN"
    light_location: tuple = (0, 0, 10)
    light_strength: float = 1.0
    light_color: tuple = (1, 1, 1)

    camera_location: tuple = (xpix / 2, ypix / 2, 100)
    camera_rotation: tuple = (0, 0, 0)

    render_resolution: tuple = (144, 144)
    render_fov: float = 30.0
    path_duration: int = 200

    curve_offset: tuple = (xpix / 2, ypix / 2, 25)
    curve_scale: float = 20
    point_count: int = 8

    clear()

    add_light(light_type, light_location, light_strength, light_color)
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count, seed)
    curve = look_at_curve(camera, curve, path_duration)
    mesh = generate_blender_terrain(terrain_texture_path, xpix, ypix, height_variation, ruggedness, seed)
    generate_trees(tree_count, xpix, ypix, mesh)

    # tree_on_fire_path = os.path.join(os.getcwd(), "models", "FireSimulation.blend")
    # bpy.ops.wm.open_mainfile(filepath=tree_on_fire_path)

    # output to a json file - the camera location, rotation, and location of fire

    get_video("videos/terrain.mp4", camera, path_duration, render_resolution, render_fov)
