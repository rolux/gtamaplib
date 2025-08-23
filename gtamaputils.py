import json
import os

from PIL import Image

from . import gtamaplib as ml
from . import gtamapdata as md

DIRNAME = os.path.dirname(__file__)


def find_aiwe():

    cam = ml.get_camera("AI World Editor Map (4K)")
    aiwe_w, aiwe_h = Image.open(md.maps["aiwe"]["filename"]).size
    aiwe_left, aiwe_top = cam.landmark_pixels["AIWE"]
    aiwe_right, aiwe_bottom = aiwe_left + 2 * aiwe_w, aiwe_top + 2 * aiwe_h
    # create a new aiwe instance that works for the camera image
    aiwe = ml.AIWE()
    aiwe = ml.AIWE(
        scale=aiwe.scale * 2,
        pixel=(
            aiwe_left + aiwe.pixel[0] * 2,
            aiwe_top + aiwe.pixel[1] * 2
        )
    )
    # initialize the camera
    xyz = -6636.086, 3000.623, 1_000_000.000
    hfov = 1
    cam.set_xyz(xyz).set_fov((hfov, None))
    # calibrate xy
    center_pixel = (cam.w / 2 - 0.5, cam.h / 2 - 0.5)
    center_world = aiwe.get_world_xy(center_pixel)
    center_cam = cam.get_point_at_zero_elevation(center_pixel)
    delta_x = center_cam[0] - center_world[0]
    delta_y = center_cam[1] - center_world[1]
    x = cam.x - delta_x
    y = cam.y - delta_y
    cam.set_xyz((x, y, cam.z))
    # calibrate hfov
    aiwe_sw_pixel = aiwe_left, aiwe_bottom
    aiwe_ne_pixel = aiwe_right, aiwe_top
    aiwe_sw_world = aiwe.get_world_xy(aiwe_sw_pixel)
    aiwe_ne_world = aiwe.get_world_xy(aiwe_ne_pixel)
    ns_world = aiwe_ne_world[0] - aiwe_sw_world[0]
    for step in (-0.001, 0.0001, -0.00001, 0.000001):
        best_loss = float("inf")
        while True:
            aiwe_sw_cam = cam.get_point_at_zero_elevation(aiwe_sw_pixel)[:2]
            aiwe_ne_cam = cam.get_point_at_zero_elevation(aiwe_ne_pixel)[:2]
            ns_cam = aiwe_ne_cam[0] - aiwe_sw_cam[0]
            loss = abs(ns_cam - ns_world)
            if loss < best_loss:
                best_loss = loss
            else:
                break
            hfov += step
            cam.set_fov((hfov, None))
    hfov -= step
    cam.set_fov((hfov, None))
    return cam


def find_mary_brickell():

    ms_cam = ml.get_camera("Metro (SE) (A) (4K)")
    ts_cam = ml.get_camera("Tennis Stadium (4K)")
    lm_name = "Nine at Mary Brickell Village"
    ray_a = (ms_cam.xyz, ms_cam.get_landmark_direction(f"{lm_name} (A)"))
    ray_b = (ms_cam.xyz, ms_cam.get_landmark_direction(f"{lm_name} (B)"))
    ray_e = (ts_cam.xyz, ts_cam.get_landmark_direction(f"{lm_name} (E)"))
    z = int(max(ms_cam.z, ts_cam.z)) + 1
    for step in (1, -0.1, 0.01, -0.001):
        loss = float("inf")
        while True:
            plane = ((0, 0, z), (0, 0, 1))
            point_a = ml.intersect_ray_and_plane(ray_a, plane)
            point_b = ml.intersect_ray_and_plane(ray_b, plane)
            point_e = ml.intersect_ray_and_plane(ray_e, plane)
            ray_ab = (point_a, ml.get_direction(point_a, point_b))
            angular_delta = ml.intersect_rays(ray_ab, ray_e)[-1]
            if angular_delta < loss:
                loss = angular_delta
            else:
                break
            z += step
    print("\n".join([
        f'    "{lm_name} ({corner})": (' + ", ".join([
            f"{v:.3f}" for v in point
        ]) + f"),  # via {ms_cam.name} & {ts_cam.name}"
        for corner, point in (
            ("A", point_a),
            ("B", point_b),
            ("E", point_e)
        )
    ]))


def render_all(
    mode,
    cameras_dirname="cameras",
    maps_dirname="maps",
    json_filename=f"{DIRNAME}/render_all.json"
):

    latest = {}
    if os.path.exists(json_filename):
        with open(json_filename, "r") as f:
            latest = json.load(f)

    if "c" in mode:
        os.makedirs(cameras_dirname, exist_ok=True)
        for cam_name in md.cameras:
            filename = f"{cameras_dirname}/{cam_name}.png"
            cam = ml.get_camera(cam_name)
            hash_ = cam.get_hash()
            if not os.path.exists(filename) or latest.get(cam_name) != hash_:
                cam.render_all().save(filename)
                latest[cam_name] = hash_
                tmp_filename = f"{json_filename}.tmp"
                with open(tmp_filename, "w") as f:
                    json.dump(latest, f, indent=4, sort_keys=True)
                os.replace(tmp_filename, json_filename)
    
    if "m" in mode:
        os.makedirs(maps_dirname, exist_ok=True)
        for map_name in reversed(list(md.maps.keys())):
            m = ml.get_map(map_name).open(scale=1.0, add_padding=True).draw_all()
            for section_name, crop in md.map_sections.items():
                filename = f"{maps_dirname}/{map_name} {section_name}.png"
                m.save(filename, crop, section_name)