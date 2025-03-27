import bpy
import os

def remove_file(file_name: str) -> None:
    '''
    Removes a file if it exists.

    Args:
        file_name (str): The name of the file to remove.
    '''

    if os.path.exists(file_name):
        os.remove(file_name)

def save_scene_to_file(file_name: str) -> None:
    '''
    Saves the current scene to a file. \n
    !!! if the file exists, it will be overwritten !!!

    Args:
        file_name (str): The name of the file to save the scene to.
    '''
    remove_file(file_name)
    bpy.ops.wm.save_as_mainfile(filepath=file_name)

def clear() -> None:
    '''
    Clears the scene by deleting all objects.
    '''
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def clear_except_to(object) -> None:
    '''
    Clears the scene by deleting all objects except the ones in the list.

    Args:
        object (bpy.types.Object): The object to keep.
    '''
    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)
    bpy.ops.object.delete()

def load_blend(filepath, object_name):
    '''
    Load a specific object from a BLEND file.

    Args:
        filepath (str): The path to the BLEND file.
        object_name (str): The name of the object to load.
    '''
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = [object_name]
    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)
