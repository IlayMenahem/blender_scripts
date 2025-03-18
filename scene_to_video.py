import os
import bpy

from utils import clear
from camera import add_camera, get_video, look_at_curve
from light import add_light
from path import generate_curve

if __name__ == "__main__":
    # initialize variables
    scence_file_path: str = os.path.join(os.getcwd(), "terrains", "forrestSimulationFinal.blend")
    terrain_video_path: str = os.path.join(os.getcwd(), "videos", "terrain.mp4")
    fire_only_video_path: str = os.path.join(os.getcwd(), "videos", "fire_only.mp4")

    seed: int = 0

    camera_location: tuple[float, float, float] = (0.0, 0.0, 50.0)
    camera_rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    camera_fov: float = 20.0
    camera_resolution: tuple[int, int] = (128, 128)
    path_duration: int = 10

    curve_offset: tuple[float, float, float] = (0.0, 0.0, 10.0)
    curve_scale: float = 0
    point_count: int = 8

    light_type: str = "SUN"
    light_location: tuple[float, float, float] = (0.0, 0.0, 100.0)
    light_strength: float = 10.0
    light_color: tuple[float, float, float] = (1.0, 1.0, 1.0)

    # load scene
    clear()
    bpy.ops.wm.open_mainfile(filepath=scence_file_path)
    add_light(light_type, light_location, light_strength, light_color)
    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count, seed)
    look_at_curve(camera, curve, path_duration)

    get_video(terrain_video_path, camera, path_duration, camera_resolution, camera_fov)
