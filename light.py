import bpy

def add_light(type, location, strength, color):
    bpy.ops.object.light_add(type=type, location=location)
    light = bpy.context.object.data
    light.energy = strength
    light.color = color
