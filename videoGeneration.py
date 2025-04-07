import os
import bpy
import random
import math

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

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'

    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.camera.data.angle = math.radians(fov)

    bpy.ops.render.render(animation=True)

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

if __name__ == "__main__":
    # Configuration values directly hard-coded instead of using argparser
    scene_path = os.path.join("terrains", "terrain.blend")
    output_video_path = os.path.join("videos", "terrain.mp4")
    camera_location = (50, 50, 100)
    seed = 0

    render_resolution = (144, 144)
    render_fov = 30.0
    path_duration = 200

    # Set the random seed
    random.seed(seed)

    # Base path definition
    base_path = '/Users/ilay_menachem/Documents/technion.nosync/2025/blender_scripts'
    video_path = os.path.join(base_path, output_video_path)
    scence_path = os.path.join(base_path, scene_path)

    clear()
    bpy.ops.wm.open_mainfile(filepath=scence_path)

    camera = bpy.data.objects['camera']
    get_video(video_path, camera, path_duration, render_resolution, render_fov)
