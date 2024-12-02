import numpy as np
import bpy
import random

'''
First Task in blender scripting:

Basic Vegetation Generation: In the provided Blender project, 
implement initial “tree” models using simple cones for placeholders. 
Set up a basic random spawning system with a density control variable to adjust tree concentration.
'''

def create_tree(tree_height=2, tree_radius=0.5):
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=tree_radius, depth=tree_height)
    tree = bpy.context.object
    mat = bpy.data.materials.new(name="TreeMaterial")
    mat.diffuse_color = (0.2, 1, 0, 0.75)  # RGBA for green

    if tree.data.materials:
        tree.data.materials[0] = mat
    else:
        tree.data.materials.append(mat)

    return tree

def put_on_mesh(obj, terrain_mesh, x, y):
    hight = obj.dimensions.z
    obj.location = (x, y, hight / 2)

    return
    raise NotImplementedError("Implement this function")

    obj.location = (x, y, np.interp(x, [0, 100], [-10, 10]))
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = terrain_mesh
    bpy.ops.object.parent_set(type='VERTEX', keep_transform=True)


def generate_trees(count: int, xpix: int, ypix: int, terrain_mesh: bpy.types.Object
                   , tree_height: float, tree_radius: float):
    '''
    generate trees on the terrain mesh
    :param count: number of trees
    :param xpix: width of the terrain
    :param ypix: height of the terrain
    :param terrain_mesh: the terrain mesh
    :param tree_height: height of the tree
    :param tree_radius: radius of the tree
    '''
    for _ in range(count):
        x = random.uniform(0, xpix)
        y = random.uniform(0, ypix)

        tree = create_tree(tree_height, tree_radius)
        put_on_mesh(tree, terrain_mesh, x, y)
