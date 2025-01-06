from perlin_noise import PerlinNoise
import numpy as np
import bpy

'''
Terrain Heightmap Implementation
Develop a terrain heightmap using Perlin noise, or a similar technique.
Include controls to adjust height variations, allowing shifts from flat plains to rugged hills.

Ground Texturing with Shaders: Apply base ground textures, using shaders to blend
textures based on slope and elevation for a natural look.
The shader should dynamically adjust textures for varying terrain types, such as grass on flatter areas and rocks on steeper inclines.
'''

def generate_noise(xpix: int, ypix: int, octave: int, seed: int) -> np.ndarray:
    noise = PerlinNoise(octaves=octave, seed=seed)
    noise = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    noise = np.array(noise)

    return noise

def generate_terrain(xpix: int, ypix: int, height_variation: float,
                    ruggedness: float, seed: int = 0) -> np.ndarray:
    octaves: list[int] = [3, 6, 12, 24]
    scales: list[float] = [height_variation, height_variation, ruggedness, ruggedness]

    terrains: list[np.ndarray] = [generate_noise(xpix, ypix, octave, seed) for octave in octaves]
    terrain = np.array(sum(terrain * scale for terrain, scale in zip(terrains, scales)))

    return terrain

def array_to_mesh(terrain: np.ndarray) -> bpy.types.Object:
    mesh = bpy.data.meshes.new("terrain_mesh")

    verts = [(x, y, hight) for (x,y), hight in np.ndenumerate(terrain)]
    edges = []
    faces = [(y * terrain.shape[1] + x, y * terrain.shape[1] + (x + 1),
            (y + 1) * terrain.shape[1] + (x + 1), (y + 1) * terrain.shape[1] + x)
            for x,y in np.ndindex(terrain.shape[0] - 1, terrain.shape[1] - 1)]

    mesh.from_pydata(verts, edges, faces)
    mesh.update()

    obj = bpy.data.objects.new("Terrain", mesh)
    bpy.context.collection.objects.link(obj)

    return obj

def generate_blender_terrain(xpix: int, ypix: int, height_variation: float,
    ruggedness: float, seed: int = 0):
    terrain = generate_terrain(xpix, ypix, height_variation, ruggedness, seed)
    mesh = array_to_mesh(terrain)

    return mesh

def apply_texture(mesh: bpy.types.Object) -> bpy.types.Object:
    '''
    Apply texture to the terrain mesh.
    mesh: bpy.types.Object, the terrain mesh.
    '''
    material = bpy.data.materials.new(name="TerrainMaterial")
    material.use_nodes = True
    material.node_tree.nodes.clear()

    # Create shader nodes
    node_tree = material.node_tree
    nodes = node_tree.nodes

    # Create principled BSDF node
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (0, 0)

    # Create material output node
    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.location = (300, 0)

    # Link nodes together
    links = node_tree.links
    links.new(principled_bsdf.outputs[0], material_output.inputs[0])

    # Assign material to mesh
    mesh.data.materials.append(material)

    return mesh
