import os
import bpy

from utils import clear, clear_except_to
from camera import add_camera, attach_camera_to_curve, get_video
from path import generate_curve

if __name__ == "__main__":
    # initialize variables
    scence_file_path = os.path.join(os.getcwd(), "scene.blend")
    terrain_video_path = os.path.join(os.getcwd(), "videos", "terrain.mp4")
    fire_only_video_path = os.path.join(os.getcwd(), "videos", "fire_only.mp4")

    seed = 0

    camera_location: tuple = (0, 0, 5)
    camera_rotation: tuple = (0, 0, 0)
    path_duration: int = 200

    camera_x = 100
    camera_y = 100
    camera_z = 100
    curve_offset: tuple = (camera_x, camera_y, camera_z)
    curve_scale: float = 20
    point_count: int = 8

    # load scene
    clear()
    bpy.ops.wm.open_mainfile(filepath=scence_file_path)

    # create camera and path
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count, seed)
    attach_camera_to_curve(camera, curve, path_duration)

    # render video
    get_video(terrain_video_path, camera, path_duration)

    # render fire only
    fire_obj = bpy.data.objects["Fire"]
    clear_except_to(fire_obj)
    get_video(fire_only_video_path, camera, path_duration)
