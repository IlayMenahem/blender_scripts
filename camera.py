import bpy

def add_camera(location: tuple[float, float, float], rotation: tuple[float, float, float],
                resolution: tuple[int, int], fov: float) -> bpy.types.Object:
    '''
    Adds a camera to the scene with the given location and rotation.

    Parameters:
    - location: The location of the camera in 3D space (x, y, z).
    - rotation: The rotation of the camera as Euler angles (x, y, z).
    - resolution: The resolution of the camera in pixels (width, height).
    - fov: The field of view of the camera in degrees.

    Returns:
    - The newly created camera object.
    '''
    camera = bpy.data.cameras.new("camera")
    camera_obj = bpy.data.objects.new("camera", camera)
    camera_obj.location = location
    camera_obj.rotation_euler = rotation
    camera_obj.data.resolution_x = resolution[0]
    camera_obj.data.resolution_y = resolution[1]
    camera_obj.data.angle = fov

    bpy.context.collection.objects.link(camera_obj)

    return camera_obj

def attach_camera_to_curve(camera: bpy.types.Object, curve: bpy.types.Object, path_duration: int):
    '''
    Attaches a camera to a curve to create a path animation.

    Parameters:
    - camera: The camera object to attach to the curve.
    - curve: The curve object that defines the camera path.
    - path_duration: The duration of the path animation in frames.

    Returns:
    - None
    '''
    bpy.context.view_layer.objects.active = camera
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    camera.constraints["Follow Path"].target = curve
    camera.constraints["Follow Path"].use_fixed_location = True
    camera.constraints["Follow Path"].forward_axis = 'FORWARD_X'
    camera.constraints["Follow Path"].up_axis = 'UP_Z'

    # Add animation to make camera follow path
    camera.constraints["Follow Path"].offset_factor = 0.0
    camera.constraints["Follow Path"].keyframe_insert(data_path="offset_factor", frame=1)
    camera.constraints["Follow Path"].offset_factor = 1.0
    camera.constraints["Follow Path"].keyframe_insert(data_path="offset_factor", frame=path_duration)

    bpy.context.view_layer.update()

def get_video(file_path: str, camera: bpy.types.Object, path_duration: int):
    '''
    Renders a video using the specified camera and path duration.
    Uses GPU acceleration with cycles rendering for optimal performance.

    Parameters:
    - file_path: The path where the rendered video will be saved.
    - camera: The camera object used for rendering the video.
    - path_duration: The duration of the video in frames.

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

    bpy.ops.render.render(animation=True)
