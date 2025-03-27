import bpy
import os
import random
from mathutils import Vector

from utils import load_blend
from ignite import add_fire_and_smoke

def save_fire_coords_to_file(coords, filepath):
    """
    Save the coordinates of the tree set on fire to a text file.

    Parameters:
        coords (tuple): The (x, y, z) coordinates of the tree set on fire.
        filepath (str): The path to the output text file.
    """
    if not coords:
        raise ValueError("No coordinates provided to save to file.")

    with open(filepath, "w") as file:
        file.write(f"Fire tree coordinates: {coords}\n")

def place_trees_on_terrain(terrain_obj, tree_obj, num_trees, fire_iteration):
    """
    Place trees on the terrain surface and add fire to one.

    Parameters:
        terrain_obj (bpy.types.Object): The terrain object.
        tree_obj (bpy.types.Object): The tree object to use.
        num_trees (int): The total number of trees to place.
        fire_iteration (int): The tree iteration to set on fire.
    """
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
    min_x, max_x, min_y, max_y = place_trees_on_terrain(terrain_obj, tree_obj, num_trees, fire_iteration)

    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    return (min_x, max_x, min_y, max_y)
