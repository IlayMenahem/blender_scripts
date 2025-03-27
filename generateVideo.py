import os
import bpy
import random
import argparse

from utils import remove_file, clear
from camera import add_camera, look_at_curve, get_video
from light import add_light
from path import generate_curve
from forrestGeneration import generate_forest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a forest scene with Blender.")
    parser.add_argument("--terrain", required=True, help="Path to the terrain .blend file.")
    parser.add_argument("--tree", required=True, help="Path to the tree .blend file.")
    parser.add_argument("--name", required=True, help="Name of the tree object in the .blend file.")
    parser.add_argument("--num_trees", type=int, required=True, help="Total number of trees to place.")
    parser.add_argument("--output", type=str, default="video.mp4", help="Path to save the output file.")
    parser.add_argument("--forrest_path", type=str, default="forrest.blend", help="Path to save the forrest file.")
    parser.add_argument("--fire_iteration", type=int, default=0, help="The tree iteration to set on fire.")

    parser.add_argument("--seed", type=int, default=0, help="Random seed for curve generation.")

    parser.add_argument("--camera_location", type=float, nargs=3, default=[0.0, 0.0, 10.0],
                        help="Camera location as x y z coordinates.")
    parser.add_argument("--camera_rotation", type=float, nargs=3, default=[0.0, 0.0, 0.0],
                        help="Camera rotation in Euler angles.")
    parser.add_argument("--camera_fov", type=float, default=20.0,
                        help="Camera field of view in degrees.")
    parser.add_argument("--camera_resolution", type=int, nargs=2, default=[128, 128],
                        help="Camera resolution width height.")
    parser.add_argument("--path_duration", type=int, default=200,
                        help="Duration of the camera path animation in frames.")

    parser.add_argument("--curve_offset", type=float, nargs=3, default=[0.0, 0.0, 5.0],
                        help="Offset for the camera path curve.")
    parser.add_argument("--curve_scale", type=float, default=1.0,
                        help="Scale factor for the camera path curve.")
    parser.add_argument("--point_count", type=int, default=8,
                        help="Number of control points for the camera path curve.")

    parser.add_argument("--light_type", type=str, default="SUN",
                        choices=["SUN", "POINT", "SPOT", "AREA"],
                        help="Type of light to add to the scene.")
    parser.add_argument("--light_location", type=float, nargs=3, default=[0.0, 0.0, 100.0],
                        help="Light location as x y z coordinates.")
    parser.add_argument("--light_strength", type=float, default=10.0,
                        help="Light strength/energy value.")
    parser.add_argument("--light_color", type=float, nargs=3, default=[1.0, 1.0, 1.0],
                        help="Light color as RGB values (0.0-1.0).")

    args = parser.parse_args()

    tree_name = args.name
    num_trees = args.num_trees
    fire_iteration = args.fire_iteration

    script_dir = os.path.dirname(os.path.abspath(__file__))
    terrain_blend_path = os.path.join(script_dir, args.terrain)
    tree_blend_path = os.path.join(script_dir, args.tree)
    output_path = os.path.join(script_dir, args.output)
    forrest_path = os.path.join(script_dir, args.forrest_path)

    seed = args.seed
    random.seed(seed)

    camera_location = tuple(args.camera_location)
    camera_rotation = tuple(args.camera_rotation)
    camera_fov = args.camera_fov
    camera_resolution = tuple(args.camera_resolution)
    path_duration = args.path_duration

    curve_offset = tuple(args.curve_offset)
    curve_scale = args.curve_scale
    point_count = args.point_count

    light_type = args.light_type
    light_location = tuple(args.light_location)
    light_strength = args.light_strength
    light_color = tuple(args.light_color)

    remove_file(output_path)
    remove_file(forrest_path)

    bounding_square = generate_forest(terrain_blend_path, tree_blend_path, tree_name, num_trees, forrest_path, fire_iteration)

    clear()
    bpy.ops.wm.open_mainfile(filepath=forrest_path)

    add_light(light_type, light_location, light_strength, light_color)

    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(bounding_square, curve_offset, curve_scale, point_count, seed)
    look_at_curve(camera, curve, path_duration=200)

    get_video(output_path, camera, path_duration, camera_resolution, camera_fov)
