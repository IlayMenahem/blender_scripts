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

def apply_texture(mesh: bpy.types.Object, path: str) -> bpy.types.Object:
    # init a clean material
    material = bpy.data.materials.new(name="TerrainMaterial")
    material.use_nodes = True
    material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Create nodes
    texture_coordinate = nodes.new('ShaderNodeTexCoord')
    image_texture = nodes.new('ShaderNodeTexImage')
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Set node properties
    image_texture.image = bpy.data.images.load(path)

    # Create links
    links.new(texture_coordinate.outputs[0], image_texture.inputs[0])
    links.new(image_texture.outputs[0], principled_bsdf.inputs[0])
    links.new(principled_bsdf.outputs[0], material_output.inputs[0])

    # Assign and activate material on mesh
    mesh.data.materials.append(material)
    mesh.data.materials[0] = material

    return mesh

def generate_blender_terrain(path: str, xpix: int, ypix: int, height_variation: float,
    ruggedness: float, seed: int = 0):
    terrain = generate_terrain(xpix, ypix, height_variation, ruggedness, seed)
    mesh = array_to_mesh(terrain)
    mesh = apply_texture(mesh, path)

    return mesh
