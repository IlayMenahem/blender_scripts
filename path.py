import bpy
import random

def generate_curve(offset: tuple[float, float, float], scale: float, point_count: int, seed: int) -> bpy.types.Object:
    random.seed(seed)
    if point_count < 4:
        raise ValueError("each curve must have at least 4 points")

    curve_data = bpy.data.curves.new(name='MyCurve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12

    # Create a new spline in the curve
    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(point_count - 1)

    # Set coordinates for the points
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
