import bpy

def generate_curve(offset: tuple[float, float, float], seed: int) -> bpy.types.Object:
    '''
    Generate a curve.
    offset: tuple[float, float, float], the offset of the curve.
    seed: int, the seed of the curve.
    return: a blender object representing the curve.
    '''
    curve = bpy.data.curves.new("curve", 'CURVE')

    return curve

if __name__ == "__main__":
    pass
