import os
import bpy
import random

'''
Basic Vegetation Generation: In the provided Blender project,
implement initial tree models, Set up a basic random spawning system with a density control variable to adjust tree concentration.
'''

def load_vegetation():
    '''
    Loads a tree model from a file and returns it.
    '''
    filenames = ["tree.fbx"]
    filename = random.choice(filenames)
    filepath = os.path.join(os.getcwd(), "models", filename)
    bpy.ops.import_scene.fbx(filepath=filepath)
    tree = bpy.context.selected_objects[0]

    return tree

def put_on_mesh(obj, terrain_mesh, x, y):
    '''
    Places the given object on height 0 at the specified coordinates.

    Parameters:
    obj (bpy.types.Object): The object to place.
    terrain_mesh (bpy.types.Object): The terrain mesh to place the object on.
    x (float): The x-coordinate of the object's position.
    y (float): The y-coordinate of the object's position.

    Returns:
    None
    '''
    height = obj.dimensions.z
    obj.location = (x, y, height / 2)

def generate_trees(count: int, xpix: int, ypix: int, terrain_mesh: bpy.types.Object):
    '''
    Generates trees on the terrain mesh at random positions.

    Parameters:
    count (int): The number of trees to generate.
    xpix (int): The width of the terrain mesh.
    ypix (int): The height of the terrain mesh.
    terrain_mesh (bpy.types.Object): The terrain mesh to place the trees on.

    Returns:
    None
    '''
    for _ in range(count):
        x = random.uniform(0, xpix)
        y = random.uniform(0, ypix)

        tree = load_vegetation()
        put_on_mesh(tree, terrain_mesh, x, y)
