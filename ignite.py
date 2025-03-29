import bpy

def add_fire_and_smoke(tree_obj):
    """
    Adds fire and smoke to a tree object using a simplified and more reliable approach.
    """
    # Store the tree's dimensions and location
    tree_dims = tree_obj.dimensions
    tree_loc = tree_obj.location

    # Calculate domain size based on tree dimensions (with some extra space)
    domain_size = max(tree_dims) * 4
    domain_height = tree_dims.z * 6  # Extra height for smoke to rise

    # Add a cube for the domain, positioned above the tree to allow smoke to rise
    bpy.ops.mesh.primitive_cube_add(size=1.0,location=(tree_loc.x, tree_loc.y, tree_loc.z + domain_height/4))
    domain = bpy.context.object
    domain.name = f"FireDomain_{tree_obj.name}"
    domain.scale = (domain_size, domain_size, domain_height)

    # Add the fluid modifier to the domain
    bpy.context.view_layer.objects.active = domain
    domain.select_set(True)
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'

    domain_settings = domain.modifiers["Fluid"].domain_settings
    domain_settings.domain_type = 'GAS'

    # Lower resolution for better stability
    domain_settings.resolution_max = 64

    # Explicitly disable adaptive domain to avoid related errors
    if hasattr(domain_settings, 'use_adaptive_domain'):
        domain_settings.use_adaptive_domain = False

    domain_settings.time_scale = 1.0
    domain_settings.burning_rate = 0.75
    domain_settings.flame_smoke = 1.0
    domain_settings.flame_vorticity = 0.5
    domain_settings.flame_ignition = 1.2
    domain_settings.flame_max_temp = 3.0
    domain_settings.vorticity = 0.2

    # Now set up the tree as the flow object
    print(f"Setting up {tree_obj.name} as flow object...")
    bpy.context.view_layer.objects.active = tree_obj
    tree_obj.select_set(True)
    bpy.ops.object.modifier_add(type='FLUID')
    tree_obj.modifiers["Fluid"].fluid_type = 'FLOW'

    # Configure flow settings with more conservative values
    flow_settings = tree_obj.modifiers["Fluid"].flow_settings
    flow_settings.flow_type = 'FIRE'  # Use just FIRE instead of BOTH for simplicity
    flow_settings.flow_behavior = 'INFLOW'
    flow_settings.fuel_amount = 0.5

    flow_settings.subframes = 2

    # Set initial velocity for more natural fire movement
    flow_settings.use_initial_velocity = True
    flow_settings.velocity_normal = 1.0
    flow_settings.temperature = 2.0
    flow_settings.velocity_factor = 0.5

    return domain
