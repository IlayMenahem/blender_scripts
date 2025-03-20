import os
import bpy
import argparse
import random
from mathutils import Vector
from utils import clear, save_scene_to_file, remove_file
from camera import add_camera, look_at_curve
from light import add_light
from path import generate_curve
from ignite import add_fire_and_smoke

def load_blend(filepath, object_name):
    """Load a specific object from a BLEND file."""
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = [object_name]
    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)

def save_fire_coords_to_file(coords, filepath):
    """
    Save the coordinates of the tree set on fire to a text file.

    Parameters:
        coords (tuple): The (x, y, z) coordinates of the tree set on fire.
        filepath (str): The path to the output text file.
    """
    if coords:
        with open(filepath, "w") as file:
            file.write(f"Fire tree coordinates: {coords}\n")
        print(f"Fire tree coordinates saved to: {filepath}")
    else:
        print("No fire tree coordinates to save.")

def place_trees_on_terrain(terrain_obj, tree_obj, num_trees, fire_iteration):
    """Place trees on the terrain surface and add fire to one."""
    # Get the terrain's bounding box in global coordinates
    bbox_corners = [terrain_obj.matrix_world @ Vector(corner) for corner in terrain_obj.bound_box]
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    for corner in bbox_corners:
        bpy.ops.mesh.primitive_cube_add(size=1, location=corner)
    for i in range(num_trees):
        # Generate random coordinates within the terrain's bounds
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        # Raycast to find the terrain's surface at (x, y)
        origin = (x, y, max(corner.z for corner in bbox_corners) + 10)  # Start higher above the terrain
        direction = (0, 0, -1)  # Cast downwards
        result, location, normal, index, object, matrix = bpy.context.scene.ray_cast(
            bpy.context.view_layer.depsgraph, origin, direction
        )

        if result:
            # Duplicate the tree and place it at the hit location
            new_tree = tree_obj.copy()
            new_tree.location = location
            new_tree.rotation_euler = (0, 0, random.uniform(0, 3.14159))  # Random rotation
            bpy.context.collection.objects.link(new_tree)
            if i == fire_iteration:
                add_fire_and_smoke(new_tree)  # Add fire to the specified tree
                fire_tree_coords = location
                save_fire_coords_to_file(fire_tree_coords, "fire_tree_coords.txt")
    return min_x, max_x, min_y, max_y

def generate_forest(terrain_blend_path, tree_blend_path, tree_name, num_trees, output_path, fire_iteration):
    """Generate the forest, add light, camera, and curve, then save the scene."""
    # Clear the existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Load the terrain
    load_blend(terrain_blend_path, "Landscape.003")  # Replace with the actual name of the terrain object

    # Load the tree object
    if tree_blend_path and os.path.exists(tree_blend_path):
        load_blend(tree_blend_path, tree_name)
        tree_obj = bpy.data.objects.get(tree_name)
        if not tree_obj:
            raise ValueError(f"Tree object '{tree_name}' not found in {tree_blend_path}.")
    else:
        raise FileNotFoundError(f"Tree file not found at {tree_blend_path}.")

    # Get the terrain object
    terrain_obj = bpy.data.objects.get("Landscape.003")  # Replace with the actual name
    if not terrain_obj:
        raise ValueError("Terrain object not found in the scene.")

    # Place trees on the terrain
    min_x,max_x,min_y,max_y=place_trees_on_terrain(terrain_obj, tree_obj, num_trees, fire_iteration)

    # Add light (sun)
    add_light(type="SUN", location=(0.0, 0.0, 100.0), strength=10.0, color=(1.0, 1.0, 1.0))

    # Add camera and curve
    camera = add_camera(location=(0.0, 0.0, 50.0), rotation=(0.0, 0.0, 0.0))
    curve = generate_curve(min_x,max_x,min_y,max_y,offset=(0.0, 0.0, 5), scale=20.0, point_count=8, seed=0)
    look_at_curve(camera, curve, path_duration=200)

    # Save the result to a new BLEND file
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"Scene saved to: {output_path}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate a forest scene with Blender.")
    parser.add_argument("--terrain", required=True, help="Path to the terrain .blend file.")
    parser.add_argument("--tree", required=True, help="Path to the tree .blend file.")
    parser.add_argument("--name", required=True, help="Name of the tree object in the .blend file.")
    parser.add_argument("--num_trees", type=int, required=True, help="Total number of trees to place.")
    parser.add_argument("--output", required=True, help="Path to save the output .blend file.")
    parser.add_argument("--fire_iteration", type=int, required=True, help="The tree iteration to set on fire.")

    # Parse arguments
    args = parser.parse_args()

    # Resolve paths relative to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    terrain_blend_path = os.path.join(script_dir, args.terrain)
    tree_blend_path = os.path.join(script_dir, args.tree)
    output_path = os.path.join(script_dir, args.output)

    # Remove the output file if it already exists
    remove_file(output_path)

    # Generate the forest, add light, camera, and curve, then save the scene
    generate_forest(
        terrain_blend_path=terrain_blend_path,
        tree_blend_path=tree_blend_path,
        tree_name=args.name,
        num_trees=args.num_trees,
        output_path=output_path,
        fire_iteration=args.fire_iteration
    )