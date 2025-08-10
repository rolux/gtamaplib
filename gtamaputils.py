import json
import os

from . import gtamaplib as ml
from . import gtamapdata as md

DIRNAME = os.path.dirname(__file__)


def find_mary_brickell():

    ms_cam = ml.get_camera("Metro (SE) (A) (4K)")
    ts_cam = ml.get_camera("Tennis Stadium (4K)")
    lm_name = "Nine at Mary Brickell"
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
        for map_name in md.maps:
            m = ml.get_map(map_name).open(scale=1.0, add_padding=True).draw_all()
            for section_name, crop in md.map_sections.items():
                filename = f"{maps_dirname}/{map_name} {section_name}.png"
                m.save(filename, crop, section_name)