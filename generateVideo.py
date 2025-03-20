import os
import bpy
import argparse

from utils import clear, save_scene_to_file, remove_file
from camera import add_camera, get_video, look_at_curve
from light import add_light
from path import generate_curve
from generateforrest import generate_forest


if __name__ == "__main__":
    print("Generating video...")
    parser = argparse.ArgumentParser(prog="generate video",description="Generate video of a fire using blender", add_help=True)
    parser.add_argument("--terrain", required=True, help="Path to the terrain .blend file.")
    parser.add_argument("--tree", required=True, help="Path to the tree .blend file.")
    parser.add_argument("--name", required=True, help="Name of the tree object in the .blend file.")
    parser.add_argument("--num_trees", type=int, required=True, help="Total number of trees to place.")
    parser.add_argument("--output", required=True, help="Path to save the output .blend file.")
    parser.add_argument("--fire_iteration", type=int, required=True, help="The tree iteration to set on fire.")
    #parser.add_argument("--tree_on_fire", required=True, help="Path to the tree_on_fire .blend file.")
    args = parser.parse_args()

    scence_file_path: str = os.path.join(os.getcwd(), "terrains", "forrestSimFinal.blend")
    terrain_video_path: str = os.path.join(os.getcwd(), "videos", "terrain.mp4")
    fire_only_video_path: str = os.path.join(os.getcwd(), "videos", "fire_only.mp4")

    seed: int = 0

    camera_location: tuple[float, float, float] = (0.0, 0.0, 10.0)
    camera_rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    camera_fov: float = 20.0
    camera_resolution: tuple[int, int] = (128, 128)
    path_duration: int = 200

    curve_offset: tuple[float, float, float] = (0.0, 0.0, 5)
    curve_scale: float = 1.0
    point_count: int = 8

    light_type: str = "SUN"
    light_location: tuple[float, float, float] = (0.0, 0.0, 100.0)
    light_strength: float = 10.0
    light_color: tuple[float, float, float] = (1.0, 1.0, 1.0)


    script_dir = os.path.dirname(os.path.abspath(__file__))
    terrain_blend_path = os.path.join(script_dir, args.terrain)
    tree_blend_path = os.path.join(script_dir, args.tree)
    output_path = os.path.join(script_dir, args.output)

    remove_file(output_path)

    generate_forest(terrain_blend_path, tree_blend_path, args.name, args.num_trees, output_path, args.fire_iteration)
    print("--------- not here ----------")
    clear()
    bpy.ops.wm.open_mainfile(filepath=output_path)
    add_light(light_type, light_location, light_strength, light_color)
    print("Adding light...")
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count, seed)
    look_at_curve(camera, curve, path_duration)

    # get_video(terrain_video_path, camera, path_duration, camera_resolution, camera_fov)
    save_scene_to_file(scence_file_path)
