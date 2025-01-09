import os
import bpy
import random

'''
Basic Vegetation Generation: In the provided Blender project,
implement initial tree models, Set up a basic random spawning system with a density control variable to adjust tree concentration.
'''

def load_tree():
    directory = os.path.join(os.getcwd(), "models/trees")
    filename = "tree.fbx"
    filepath = os.path.join(directory, filename)

    bpy.ops.import_scene.fbx(filepath=filepath)
    tree = bpy.context.selected_objects[0]

    return tree

def put_on_mesh(obj, terrain_mesh, x, y):
    hight = obj.dimensions.z
    obj.location = (x, y, hight / 2)

def generate_trees(count: int, xpix: int, ypix: int, terrain_mesh: bpy.types.Object):
    for _ in range(count):
        x = random.uniform(0, xpix)
        y = random.uniform(0, ypix)

        tree = load_tree()
        put_on_mesh(tree, terrain_mesh, x, y)
