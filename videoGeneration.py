import os
import bpy
import random
import argparse
from utils import clear
from path import generate_curve
from camera import add_camera, look_at_curve, get_video

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a video of the fire and forrest")

    parser.add_argument("--scene-path", type=str, default=os.path.join("terrains", "terrain.blend"))
    parser.add_argument("--output-video-path", type=str, default=os.path.join("videos", "terrain.mp4"),
                        help="Path to save the output video file")
    parser.add_argument("--camera-location", type=tuple, default=(50, 50, 100),
                            help="Location of camera")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for generation")

    parser.add_argument("--render-resolution", type=tuple, default=(144, 144),
                        help="Render resolution")
    parser.add_argument("--render-fov", type=float, default=30.0,
                        help="Field of view for rendering")
    parser.add_argument("--path-duration", type=int, default=200,
                        help="Duration of camera path")

    parser.add_argument("--curve-offset", type=tuple, default=(50, 50, 25),
                        help="Offset of the curve the camera follows")
    parser.add_argument("--curve-scale", type=float, default=20,
                        help="Scale of camera curve")
    parser.add_argument("--point-count", type=int, default=8,
                        help="Number of points in camera curve")

    args = parser.parse_args()

    video_path: str = os.path.join(os.getcwd(), args.output_video_path)
    scence_path: str = os.path.join(os.getcwd(), args.scene_path)

    seed: int = args.seed
    random.seed(seed)

    camera_location: tuple = args.camera_location
    camera_rotation: tuple = (0, 0, 0)

    render_resolution: tuple = args.render_resolution
    render_fov: float = args.render_fov
    path_duration: int = args.path_duration

    curve_offset: tuple = args.curve_offset
    curve_scale: float = args.curve_scale
    point_count: int = args.point_count

    clear()
    bpy.ops.wm.open_mainfile(filepath=scence_path)

    camera = add_camera(camera_location, camera_rotation)
    curve = generate_curve(curve_offset, curve_scale, point_count)
    curve = look_at_curve(camera, curve, path_duration)

    get_video(video_path, camera, path_duration, render_resolution, render_fov)
