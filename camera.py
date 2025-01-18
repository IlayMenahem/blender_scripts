import bpy

def add_camera(location: tuple[float, float, float], rotation: tuple[float, float, float]) -> bpy.types.Object:
    camera = bpy.data.cameras.new("camera")
    camera_obj = bpy.data.objects.new("camera", camera)
    camera_obj.location = location
    camera_obj.rotation_euler = rotation

    bpy.context.collection.objects.link(camera_obj)

    return camera_obj
