import bpy

def add_camera(location: tuple[float, float, float], rotation: tuple[float, float, float]) -> bpy.types.Object:
    camera = bpy.data.cameras.new("camera")
    camera_obj = bpy.data.objects.new("camera", camera)
    camera_obj.location = location
    camera_obj.rotation_euler = rotation

    bpy.context.collection.objects.link(camera_obj)

    return camera_obj

def attach_camera_to_curve(camera: bpy.types.Object, curve: bpy.types.Object, path_duration: int):
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
    Get a video of the camera
    :param file_path: The path to save the video
    :param camera: The camera to record
    :param path_duration: The length of the video
    '''
    bpy.context.scene.camera = camera
    bpy.context.scene.frame_end = path_duration
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.filepath = file_path

    bpy.ops.render.render(animation=True)
