import bpy

def add_light(type: str, location: tuple, strength: float, color: tuple):
    '''
    Adds a light object to the scene with the given type, location, strength, and color.

    Parameters:
    - type: The type of light to add ('POINT', 'SUN', 'SPOT', 'AREA').
    - location: The location of the light in 3D space (x, y, z).
    - strength: The strength of the light.
    - color: The color of the light as a tuple of RGB values (r, g, b).

    Returns:
    - The newly created light object.
    '''

    bpy.ops.object.light_add(type=type, location=location)
    light = bpy.context.object.data
    light.energy = strength
    light.color = color
