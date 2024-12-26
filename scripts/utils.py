import bpy
import os

def remove_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
