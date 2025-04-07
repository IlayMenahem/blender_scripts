import os
import argparse
import random

from terrain import generate_blender_terrain
from vegetation import generate_trees, add_burning_tree
from light import add_light
from utils import clear, save_scene_to_file
from path import generate_curve
from camera import add_camera, look_at_curve

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Blender scene with terrain, trees, and a burning tree.")

    parser.add_argument("--terrain-texture-path", type=str,
                        default="textures/grass-terrain/textures/rocky_terrain_02_diff_4k.jpg",
                        help="Path to terrain texture")
    parser.add_argument("--output-path", type=str,
                        default=os.path.join("terrains", "terrain.blend"),
                        help="Path to save the output blend file")
    parser.add_argument("--xpix", type=int, default=100,
                        help="Number of pixels in x dimension")
    parser.add_argument("--ypix", type=int, default=100,
                        help="Number of pixels in y dimension")
    parser.add_argument("--height-variation", type=float, default=5.0,
                        help="Height variation for terrain")
    parser.add_argument("--ruggedness", type=float, default=0.5,
                        help="Ruggedness of terrain")

    parser.add_argument("--tree-count", type=int, default=60,
                        help="Number of trees to generate")
    parser.add_argument("--tree-on-fire-position", type=tuple, default=(50, 50),
                        help="Position of burning tree")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for generation")

    parser.add_argument("--light-type", type=str, default="SUN",
                        help="Type of light to use")
    parser.add_argument("--light-location", type=tuple, default=(0, 0, 25),
                        help="Location of light source")
    parser.add_argument("--light-strength", type=float, default=1.0,
                        help="Strength of light")
    parser.add_argument("--light-color", type=tuple, default=(1, 1, 1),
                        help="Color of light")

    parser.add_argument("--curve-offset", type=tuple, default=(50, 50, 25),
                            help="Offset of the curve the camera follows")
    parser.add_argument("--curve-scale", type=float, default=20,
                        help="Scale of camera curve")
    parser.add_argument("--point-count", type=int, default=8,
                        help="Number of points in camera curve")

    parser.add_argument("--path-duration", type=int, default=200,
                        help="Duration of camera path")
    parser.add_argument("--camera-location", type=tuple, default=(50, 50, 100),
                            help="Location of camera")

    args = parser.parse_args()

    terrain_texture_path: str = os.path.join(os.getcwd(), args.terrain_texture_path)
    file_path: str = os.path.join(os.getcwd(), args.output_path)
    xpix: int = args.xpix
    ypix: int = args.ypix
    height_variation: float = args.height_variation
    ruggedness: float = args.ruggedness

    tree_count: int = args.tree_count
    tree_on_fire_position: tuple = args.tree_on_fire_position

    seed: int = args.seed
    random.seed(args.seed)

    light_type: str = args.light_type
    light_location: tuple = args.light_location
    light_strength: float = args.light_strength
    light_color: tuple = args.light_color

    camera_location: tuple = args.camera_location
    camera_rotation: tuple = (0, 0, 0)
    path_duration: int = args.path_duration

    curve_offset: tuple = args.curve_offset
    curve_scale: float = args.curve_scale
    point_count: int = args.point_count

    clear()

    add_burning_tree(tree_on_fire_position)
    mesh = generate_blender_terrain(terrain_texture_path, xpix, ypix, height_variation, ruggedness, seed)
    generate_trees(tree_count, xpix, ypix, mesh)
    add_light(light_type, light_location, light_strength, light_color)
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count)
    curve = look_at_curve(camera, curve, path_duration)

    save_scene_to_file(file_path)
