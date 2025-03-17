import bpy
import math

def add_camera(location: tuple[float, float, float], rotation: tuple[float, float, float]) -> bpy.types.Object:
    '''
    Adds a camera to the scene with the given location and rotation.

    Parameters:
    - location: The location of the camera in 3D space (x, y, z).
    - rotation: The rotation of the camera as Euler angles (x, y, z).

    Returns:
    - The newly created camera object.
    '''
    camera = bpy.data.cameras.new("camera")
    camera_obj = bpy.data.objects.new("camera", camera)
    camera_obj.location = location
    camera_obj.rotation_euler = rotation

    bpy.context.collection.objects.link(camera_obj)

    return camera_obj

def attach_to_curve(obj: bpy.types.Object, curve: bpy.types.Object, path_duration: int):
    '''
    Attaches an object to a curve to create a path animation.

    Parameters:
    - obj: The object to attach to the curve.
    - curve: The curve object that defines the path.
    - path_duration: The duration of the path animation in frames.

    Returns:
    - The object that was attached to the curve
    '''
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    obj.constraints["Follow Path"].target = curve
    obj.constraints["Follow Path"].use_fixed_location = True
    obj.constraints["Follow Path"].forward_axis = 'FORWARD_X'
    obj.constraints["Follow Path"].up_axis = 'UP_Z'

    # Add animation to make camera follow path
    obj.constraints["Follow Path"].offset_factor = 0.0
    obj.constraints["Follow Path"].keyframe_insert(data_path="offset_factor", frame=1)
    obj.constraints["Follow Path"].offset_factor = 1.0
    obj.constraints["Follow Path"].keyframe_insert(data_path="offset_factor", frame=path_duration)

    bpy.context.view_layer.update()

    return obj

def look_at_curve(camera: bpy.types.Object, curve: bpy.types.Curve, path_duration: int):
    '''
    Camera follows the curve

    Parameters:
    - camera: The camera object to be adjusted.
    - curve: The curve object to be followed.
    - path_duration: The duration of the animation in frames.

    Returns:
    - Camera Object
    '''
    target = bpy.data.objects.new("Target", None)
    bpy.context.collection.objects.link(target)

    attach_to_curve(target, curve, path_duration)

    camera.constraints.new(type='TRACK_TO')
    camera.constraints["Track To"].target = target
    camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    camera.constraints["Track To"].up_axis = 'UP_Y'
    camera.constraints["Track To"].influence = 1.0

    return camera

def get_video(file_path: str, camera: bpy.types.Object, path_duration: int, resolution: tuple[int, int], fov: float):
    '''
    Renders a video using the specified camera and path duration.
    Uses GPU acceleration with cycles rendering for optimal performance.

    Parameters:
    - file_path: The path where the rendered video will be saved.
    - camera: The camera object used for rendering the video.
    - path_duration: The duration of the video in frames.
    - resolution: The resolution of the video in pixels.
    - fov: The field of view of the camera in degrees.

    Returns:
    - None
    '''
    bpy.context.scene.camera = camera
    bpy.context.scene.frame_end = path_duration
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.filepath = file_path

    # use GPU acceleration with cycles rendering for optimal performance
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'

    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.camera.data.angle = math.radians(fov)

    bpy.ops.render.render(animation=True)
