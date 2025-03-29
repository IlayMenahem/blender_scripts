import os
import bpy
import random
from ignite import add_fire_and_smoke

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

def put_on_mesh(obj, x, y):
    '''
    Places the given object on height 0 at the specified coordinates.

    Parameters:
    obj (bpy.types.Object): The object to place.
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
        put_on_mesh(tree, x, y)

def add_burning_tree(position: tuple) -> bpy.types.Object:
    '''
    add a burning tree to the scene at the specified position.

    Parameters:
    position (tuple): The position of the burning tree.

    Returns:
    bpy.types.Object: The burning tree object.
    '''
    tree = load_vegetation()
    put_on_mesh(tree, position[0], position[1])
    add_fire_and_smoke(tree)
