import bpy
import random

def generate_curve_bounded(bounding_square: tuple[float, float, float, float], offset: tuple[float, float, float], scale: float, point_count: int, seed: int) -> bpy.types.Object:
    """
    Generates a random curve with the given offset, scale, point count, and seed.

    Parameters:
    - bounding_square: The bounding square for the curve. min_x, max_x, min_y, max_y
    - offset: The offset of the curve.
    - scale: The scale of the curve.
    - point_count: The number of points in the curve.
    - seed: The seed for the random number generator.

    Returns:
    - The generated curve object.
    """
    if point_count < 4:
        raise ValueError("each curve must have at least 4 points")

    curve_data = bpy.data.curves.new(name='MyCurve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12

    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(point_count - 1)

    min_x, max_x, min_y, max_y = bounding_square
    points = spline.bezier_points
    for i, point in enumerate(points):
        x = random.uniform(min_x, max_x) + offset[0]
        y = random.uniform(min_y, max_y) + offset[1]
        z = random.uniform(-scale, scale) + offset[2]
        point.co = (x, y, z)
        point.handle_left_type = 'AUTO'
        point.handle_right_type = 'AUTO'

    curve_obj = bpy.data.objects.new('MyCurveObject', curve_data)

    bpy.context.scene.collection.objects.link(curve_obj)

    return curve_obj

def generate_curve(offset: tuple[float, float, float], scale: float, point_count: int) -> bpy.types.Object:
    """
    Generates a random curve with the given offset, scale, point count, and seed.

    Parameters:
    - offset: The offset of the curve.
    - scale: The scale of the curve.
    - point_count: The number of points in the curve.

    Returns:
    - The generated curve object.
    """
    if point_count < 4:
        raise ValueError("each curve must have at least 4 points")

    curve_data = bpy.data.curves.new(name='MyCurve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12

    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(point_count - 1)

    points = spline.bezier_points
    for i, point in enumerate(points):
        x = random.uniform(-scale, scale) + offset[0]
        y = random.uniform(-scale, scale) + offset[1]
        z = random.uniform(-scale, scale) + offset[2]
        point.co = (x, y, z)
        point.handle_left_type = 'AUTO'
        point.handle_right_type = 'AUTO'

    curve_obj = bpy.data.objects.new('MyCurveObject', curve_data)

    bpy.context.scene.collection.objects.link(curve_obj)

    return curve_obj
