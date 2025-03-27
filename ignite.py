import bpy
import os


def add_fire_and_smoke(tree_obj):
    """
    Adds a fire and smoke simulation to the tree using Blender's fluid physics.
    """
    print("Starting add_fire_and_smoke function...")

    # Add a cube around the tree to act as the domain
    bpy.ops.mesh.primitive_cube_add(size=10, location=tree_obj.location)
    domain = bpy.context.object

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
    else:
        print("use_flame attribute not found in domain_settings")

    if hasattr(domain_settings, 'use_smoke'):
        domain_settings.use_smoke = True  # Enable smoke simulation
    else:
        print("use_smoke attribute not found in domain_settings")

    # Set the tree as the flow object to emit fire and smoke
    bpy.context.view_layer.objects.active = tree_obj
    tree_obj.select_set(True)
    bpy.ops.object.modifier_add(type='FLUID')
    tree_obj.modifiers["Fluid"].fluid_type = 'FLOW'

    # Configure the flow settings
    flow_settings = tree_obj.modifiers["Fluid"].flow_settings
    flow_settings.flow_type = 'BOTH'
    flow_settings.flow_behavior = 'INFLOW'  # Set flow behavior to inflow
    flow_settings.fuel_amount = 0.4  # Set fuel value to 0.4
    flow_settings.use_initial_velocity = True
    flow_settings.velocity_normal = 1.0
    flow_settings.temperature = 1000  # High temperature for fire

    #flow_settings.flow_source = 'GEOMETRY'  # Emit fire from the tree's geometry
    flow_settings.velocity_normal = 2.0  # Increase velocity for more lively flames
