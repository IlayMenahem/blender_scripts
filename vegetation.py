import bpy
import random

'''
First Task in blender scripting:

Basic Vegetation Generation: In the provided Blender project, 
implement initial “tree” models using simple cones for placeholders. 
Set up a basic random spawning system with a density control variable to adjust tree concentration.
'''

# Parameters
tree_count = 50
area_size = 10
tree_height = 2
tree_radius = 0.5

# Function to create a tree
def create_tree(location):
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=tree_radius, depth=tree_height, location=location)
    tree = bpy.context.object
    mat = bpy.data.materials.new(name="TreeMaterial")
    mat.diffuse_color = (0.2, 1, 0, 0.75)  # RGBA for green
    if tree.data.materials:
        tree.data.materials[0] = mat
    else:
        tree.data.materials.append(mat)

# Function to generate trees
def generate_trees(count, area):
    for _ in range(count):
        x = random.uniform(-area, area)
        y = random.uniform(-area, area)
        z = tree_height / 2
        create_tree((x, y, z))

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Generate trees
generate_trees(tree_count, area_size)