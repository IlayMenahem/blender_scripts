from posix import remove
from perlin_noise import PerlinNoise
import numpy as np
import bpy

from utils import clear, remove_file

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

def generate_blender_terrain(terrain: np.ndarray):
    '''
    Display the terrain in blender.
    terrain: np.ndarray, the terrain to display.
    return: a blender object representing the terrain.
    '''
    mesh = bpy.data.meshes.new("terrain_mesh")
    obj = bpy.data.objects.new("Terrain", mesh)
    bpy.context.collection.objects.link(obj)

    verts = [(x, y, hight) for (x,y), hight in np.ndenumerate(terrain)]
    faces = []
    for x in range(terrain.shape[1]-1):
        for y in range(terrain.shape[0]-1):
            faces.append((
                y * terrain.shape[1] + x,
                y * terrain.shape[1] + (x + 1),
                (y + 1) * terrain.shape[1] + (x + 1),
                (y + 1) * terrain.shape[1] + x
            ))

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    return obj

def apply_texture(mesh: bpy.types.Object) -> bpy.types.Object:
    '''
    Apply texture to the terrain mesh.
    mesh: bpy.types.Object, the terrain mesh.
    '''

    return mesh


if __name__ == "__main__":
    xpix: int = 100
    ypix: int = 100
    height_variation: float = 5.0
    ruggedness: float = 0.5
    seed: int = 0

    remove_file("blends/terrain.blend")
    clear()

    terrain = generate_terrain(xpix, ypix, height_variation, ruggedness, seed)
    mesh = generate_blender_terrain(terrain)
    mesh = apply_texture(mesh)

    bpy.context.view_layer.objects.active = mesh
    bpy.ops.wm.save_as_mainfile(filepath="blends/terrain.blend", check_existing=False)
