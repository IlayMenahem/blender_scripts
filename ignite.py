import bpy
import os

def add_fire_and_smoke(tree_obj):
    """
    Adds a fire and smoke simulation to the tree using Blender's fluid physics.
    """
    # Add a cube around the tree to act as the domain
    bpy.ops.mesh.primitive_cube_add(size=10, location=tree_obj.location)
    domain = bpy.context.object
    domain.name = "FireDomain"

    # Scale and position the domain to fully enclose the tree
    domain.scale = (2, 2, 2)  # Adjust scale as needed
    domain.location.z += 2  # Move the domain up slightly

    # Set the cube as the domain for the fire and smoke simulation
    bpy.context.view_layer.objects.active = domain
    domain.select_set(True)
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'

    # Configure the domain settings for fire and smoke
    domain_settings = domain.modifiers["Fluid"].domain_settings
    domain_settings.domain_type = 'GAS'
    domain_settings.use_adaptive_domain = True

    # Enable fire and smoke
    if hasattr(domain_settings, 'use_flame'):
        domain_settings.use_flame = True  # Enable flame simulation
    if hasattr(domain_settings, 'use_smoke'):
        domain_settings.use_smoke = True  # Enable smoke simulation


    # Set the tree as the flow object to emit fire and smoke
    bpy.context.view_layer.objects.active = tree_obj
    tree_obj.select_set(True)
    bpy.ops.object.modifier_add(type='FLUID')
    tree_obj.modifiers["Fluid"].fluid_type = 'FLOW'

    # Configure the flow settings
    flow_settings = tree_obj.modifiers["Fluid"].flow_settings
    flow_settings.flow_type = 'FIRE'
    flow_settings.flow_behavior = 'INFLOW'  # Set flow behavior to inflow
    flow_settings.fuel_amount = 0.4  # Set fuel value to 0.4
    flow_settings.use_initial_velocity = True
    flow_settings.velocity_normal = 1.0
    flow_settings.temperature = 1000  # High temperature for fire

    #flow_settings.flow_source = 'GEOMETRY'  # Emit fire from the tree's geometry
    flow_settings.velocity_normal = 2.0  # Increase velocity for more lively flames
    #flow_settings.flow_density = 1.0  # Higher density for thicker flames
    #flow_settings.flow_smoke = 0.5  # Less smoke for a cleaner fire effect

def main(tree_blend_path, output_path):
    """
    Loads a tree from a BLEND file, adds fire and smoke, and saves the result.
    """
    # Clear the existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Load the tree object from the BLEND file
    with bpy.data.libraries.load(tree_blend_path) as (data_from, data_to):
        data_to.objects = [obj for obj in data_from.objects if obj.startswith("tree")]  # Only link tree objects

    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)
        tree_obj = obj  # Assume the first object is the tree

    # Add fire and smoke to the tree
    add_fire_and_smoke(tree_obj)

    # Save the result to a new BLEND file
    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    print("--------- not here ----------")

if __name__ == "__main__":
    # Example usage
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    tree_blend_path = os.path.join(script_dir, "tree.blend")  # Path to tree.blend
    output_path = os.path.join(script_dir, "tree_with_fire.blend")  # Path to save the output

    main(tree_blend_path, output_path)
