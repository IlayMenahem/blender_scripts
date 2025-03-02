from perlin_noise import PerlinNoise
import numpy as np
import bpy

def generate_noise(xpix: int, ypix: int, octave: int, seed: int) -> np.ndarray:
    '''
    Generate a 2D Perlin noise array with given dimensions and parameters.

    Parameters:
        - xpix (int): Width of the noise array.
        - ypix (int): Height of the noise array.
        - octave (int): Number of octaves for the Perlin noise.
        - seed (int): Seed for the Perlin noise.

    Returns:
        - noise (np.ndarray): 2D Perlin noise array.
    '''

    noise = PerlinNoise(octaves=octave, seed=seed)
    noise = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    noise = np.array(noise)

    return noise

def generate_terrain(xpix: int, ypix: int, height_variation: float,
                    ruggedness: float, seed: int = 0) -> np.ndarray:
    '''
    Generate a 2D terrain array with given dimensions and parameters.
    the terrain is a weighted sum of multiple layers of Perlin noise with varying octaves.

    Parameters:
        - xpix (int): Width of the terrain array.
        - ypix (int): Height of the terrain array.
        - height_variation (float): Height variation of the terrain.
        - ruggedness (float): Ruggedness of the terrain.
        - seed (int): Seed for the Perlin noise.

    Returns:
        - terrain (np.ndarray): 2D terrain array.
    '''

    octaves: list[int] = [3, 6, 12, 24]
    scales: list[float] = [height_variation, height_variation, ruggedness, ruggedness]

    terrains: list[np.ndarray] = [generate_noise(xpix, ypix, octave, seed) for octave in octaves]
    terrain = np.array(sum(terrain * scale for terrain, scale in zip(terrains, scales)))

    return terrain

def array_to_mesh(terrain: np.ndarray) -> bpy.types.Object:
    '''
    Converts a 2D terrain array to a Blender mesh object.

    Parameters:
        - terrain (np.ndarray): 2D terrain array.

    Returns:
        - obj (bpy.types.Object): Blender mesh object.
    '''

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
    '''
    Applies an image to a Blender mesh object.

    Parameters:
        mesh (bpy.types.Object): The Blender mesh object to apply the texture to.
        path (str): The path to the image file to use as the texture.

    Returns:
        bpy.types.Object: The mesh object with the texture applied.

    '''

    # init a clean material
    material = bpy.data.materials.new(name="TerrainMaterial")
    material.use_nodes = True
    material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Add texture nodes
    texture_coordinate = nodes.new('ShaderNodeTexCoord')
    image_texture = nodes.new('ShaderNodeTexImage')
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Set node properties
    image_texture.image = bpy.data.images.load(path)

    # link the texture nodes
    links.new(texture_coordinate.outputs[0], image_texture.inputs[0])
    links.new(image_texture.outputs[0], principled_bsdf.inputs[0])
    links.new(principled_bsdf.outputs[0], material_output.inputs[0])

    # Assign and activate material on mesh
    mesh.data.materials.append(material)

    return mesh

def generate_blender_terrain(path: str, xpix: int, ypix: int, height_variation: float,
    ruggedness: float, seed: int = 0):
    '''
    Generates a Blender mesh object with a terrain texture applied.
    the terrain is generated using perlin noise.

    Parameters:
        path (str): The path to the image file to use as the texture.
        xpix (int): The number of pixels in the x direction.
        ypix (int): The number of pixels in the y direction.
        height_variation (float): The height variation of the terrain.
        ruggedness (float): The ruggedness of the terrain.
        seed (int): The seed for the random number generator.

    Returns:
        bpy.types.Object: The mesh object with the texture applied.

    '''

    terrain = generate_terrain(xpix, ypix, height_variation, ruggedness, seed)
    mesh = array_to_mesh(terrain)
    mesh = apply_texture(mesh, path)

    return mesh
