"""
gtamaplib v0.1.0
This library follows the same geometric conventions that Grand Theft Auto uses internally.
World coordinates are right-handed ENU: +X is East, +Y is North, +Z is up. Yaw about world +Z
(0 deg is North, increasing CCW), pitch about local +X, roll about local +Y. Right-hand rule.
Image origin is in the top left. Pixel (x, y) denotes the center at (x + 0.5, y + 0.5).
"""

import colorsys
from functools import lru_cache
import hashlib
import json
import math
import multiprocessing
import os
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial.transform import Rotation as R
from tqdm import tqdm

from . import gtamapdata as md

multiprocessing.set_start_method("fork", force=True)
Image.MAX_IMAGE_PIXELS = None

DIRNAME = os.path.dirname(__file__)


### CAMERA #########################################################################################

class Camera:

    def __init__(
        self, id, name, player,
        xyz, ypr, fov, size,
        pixels=None, lines=None
    ):
        self.id = id
        self.name = name
        self.color = get_color(self.name)
        self.player = player
        self.set_xyz(xyz)
        self.set_ypr(ypr)
        self.set_size(size)
        self.set_fov(fov)
        self.landmark_pixels = pixels or {}
        self.lines = lines or [[], []]
        if self.name not in md.cameras:
            self.register()

    def __repr__(self):
        player = (f"(" + ", ".join([
            f"{v:.3f}" for v in self.player
        ]) + ")") if self.player else "None"
        d = 6 if self.hfov < 1 else 3
        return (
            f"<Camera {self.id} {self.name}: {player}, "
            f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f}), "
            f"({self.yaw:.3f}, {self.pitch:.3f}, {self.roll:.3f}), "
            f"({self.hfov:.{d}f}, {self.vfov:.{d}f}), ({self.w}, {self.h})>"
        )

    def _get_pitch_from_hlines(self):
        if not self.lines[0]: return None
        vpx, vpy = self._get_vp_from_lines(self.lines[0])
        ndc_y = 1 - 2 * ((vpy + 0.5) / self.h)
        tan_v = np.tan(np.radians(self.vfov / 2))
        return np.degrees(-np.arctan(ndc_y * tan_v))

    def _get_pitch_from_vlines(self):
        if not self.lines[1]: return None
        def rotate(point):
            x, y = point
            dx, dy = x - cx, y - cy
            return (
                c * dx - s * dy + cx,
                s * dx + c * dy + cy
            )
        cx, cy = self.w / 2 - 0.5, self.h / 2 - 0.5
        r = -np.radians(self.roll)
        c, s = np.cos(r), np.sin(r)
        if len(self.lines[1]) == 1:
            a, b = self.lines[1][0]
            line_unrolled = (rotate(a), rotate(b))
            vp_unrolled = intersect_lines_2d(line_unrolled, ((cx, 0), (cx, self.h)))
            if vp_unrolled is None:
                return 0.0
        else:
            lines_unrolled = [(rotate(a), rotate(b)) for (a, b) in self.lines[1]]
            vp_unrolled = self._get_vp_from_lines(lines_unrolled)
        vpy_unrolled = vp_unrolled[1]
        ndc_y = 1 - 2 * ((vpy_unrolled + 0.5) / self.h)
        tan_v = np.tan(np.radians(self.vfov / 2))
        return np.degrees(np.arctan(1 / (ndc_y * tan_v)))

    def _get_vp_from_lines(self, lines):
        n = len(lines)
        points = [
            intersect_lines_2d(lines[i], lines[j])
            for i in range(n)
            for j in range(i + 1, n)
        ]
        points = np.array([p for p in points if p is not None], dtype=float)
        return tuple(points.mean(axis=0)) if len(points) else None

    def calibrate_yaw(self, lm_name, lm_point=None):
        """
        Sets yaw so that a given landmark's pixel matches a given point
        """
        if lm_point is None: lm_point = md.landmarks[lm_name]
        d_current = self.get_landmark_direction(lm_name)
        b_current, _ = get_angles_from_direction(d_current)
        d_target = get_direction(self.xyz, lm_point)
        b_target, _ = get_angles_from_direction(d_target)
        yaw = (self.yaw + get_angle_delta(b_current, b_target)) % 360
        self.set_ypr((yaw, self.pitch, self.roll))
        return self

    def calibrate_pitch(self, lm_name, lm_point=None):
        """
        Sets pitch so that a given landmark's pixel matches a given point
        """
        if lm_point is None: lm_point = md.landmarks[lm_name]
        d_current = self.get_landmark_direction(lm_name)
        _, e_current = get_angles_from_direction(d_current)
        d_target = get_direction(self.xyz, lm_point)
        _, e_target = get_angles_from_direction(d_target)
        pitch = self.pitch + get_angle_delta(e_current, e_target)
        self.set_ypr((self.yaw, pitch, self.roll))
        return self

    def calibrate_z(self, lm_name, lm_point=None):
        """
        Sets z so that a given landmark's pixel matches a given point
        """
        if lm_point is None: lm_point = md.landmarks[lm_name]
        z_current = intersect_rays(
            (lm_point, (0, 0, 1)),
            (self.xyz, self.get_landmark_direction(lm_name))
        )[1][2]
        z_target = lm_point[2]
        z = self.z - z_current + z_target
        self.set_xyz((self.x, self.y, z))
        return self

    def calibrate_yaw_and_pitch(self, lm_name, lm_point=None, iters=3):
        """
        Sets yaw and pitch so that a given landmark's pixel matches a given point.
        After three iterations, this should be sufficiently precise.
        """
        if lm_point is None: lm_point = md.landmarks[lm_name]
        for _ in range(iters):
            self.calibrate_yaw(lm_name, lm_point)
            self.calibrate_pitch(lm_name, lm_point)
        return self

    def calibrate_yaw_and_z(self, lm_name, lm_point=None):
        """
        Sets yaw and z so that a given landmark's pixel matches a given point
        """
        if lm_point is None: lm_point = md.landmarks[lm_name]
        self.calibrate_yaw(lm_name, lm_point)
        self.calibrate_z(lm_name, lm_point)
        return self

    def clear_landmark_directions(self, include_local=False):
        """
        Clears cached landmark directions
        """
        self.landmark_directions = {}
        if include_local:
            self.landmark_directions_local = {}
        return self

    def draw_circle(self, xy, r, fill=(255, 255, 255), outline=(0, 0, 0), width=1):
        """
        Draws a circle at screen coordinates xy
        """
        if not hasattr(self, "image"): self.open()
        x, y = xy
        self.draw.circle(
            (int(round(x * self.scale + self.offset)), int(round(y * self.scale))),
            int(round(r * self.scale)),
            fill=fill, outline=outline, width=int(round(width * self.scale))
        )
        return self

    def draw_label(self, xy, length, text, color, text_color):
        """
        Draws a label at screen coordinates xy
        """
        if not hasattr(self, "image"): self.open()
        x, y = xy
        self.draw_line(((x, y), (x, y - length)), color, 1)
        box = draw_box(text, 10 * self.scale, color, text_color).rotate(90, expand=True)
        xy = (
            int(round(x * self.scale + self.offset - box.size[0] / 2)),
            int(round((y - length) * self.scale - box.size[1]))
        )
        self.image.paste(box, xy)
        return self

    def draw_line(self, line, fill=(0, 0, 0), width=1):
        """
        Draws a line between screen coordinates line[0] and line[1]
        """
        if not hasattr(self, "image"): self.open()
        (x0, y0), (x1, y1) = line
        x0 = int(round(x0 * self.scale + self.offset))
        y0 = int(round(y0 * self.scale))
        x1 = int(round(x1 * self.scale + self.offset))
        y1 = int(round(y1 * self.scale))
        try:
            self.draw.line((x0, y0, x1, y1), fill=fill, width=int(round(width * self.scale)))
        except SystemError:
            pass  # int too large
        return self

    def get_hash(self):
        """
        Returns a unique hash for the current settings and landmarks coordinates.
        Storing this hash allows users to skip re-rendering the camera image.
        """
        data = [
            self.id, self.name, self.player,
            self.xyz, self.ypr, self.fov, self.size,
            self.landmark_pixels, self.lines,
            [
                (lm_name, md.landmarks[lm_name])
                for lm_name in self.landmark_pixels
                if lm_name in md.landmarks
            ]
        ]
        return hashlib.sha1(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()

    def get_horizon(self):
        """
        Returns the y coordinate of the horizon
        """
        tan_v = np.tan(np.radians(self.vfov / 2))
        ndc_y = -np.tan(np.radians(self.pitch)) / tan_v
        return (1 - ndc_y) * 0.5 * self.h - 0.5

    def get_hvp(self):
        """
        Returns the horizontal vanishing point
        """
        h_lines = self.lines[0]
        if not h_lines: return
        n = len(h_lines)
        points = np.array([
            intersect_lines_2d(h_lines[i], h_lines[j])
            for i in range(n)
            for j in range(i + 1, n)
        ])
        return points.mean(axis=0)

    def get_vvp(self):
        """
        Returns the vertical vanishing point
        """
        if self.pitch == 0: return None
        cx, cy = self.w * 0.5, self.h * 0.5
        fx = cx / np.tan(np.radians(self.hfov) * 0.5)
        fy = cy / np.tan(np.radians(self.vfov) * 0.5)
        rot = R.from_quat(self.q)
        dir_x, dir_y, dir_z = rot.inv().apply([0, 0, 1])
        x = fx * (dir_x / dir_y) + cx
        y = cy - fy * (dir_z / dir_y)
        return float(x), float(y)

    def get_landmark_direction(self, lm_name):
        """
        Returns the direction vector of a given landmark
        """
        if not lm_name in self.landmark_directions:
            self.landmark_directions[lm_name] = get_pixel_direction(
                self.landmark_pixels[lm_name], self.q, self.fov, self.size
            )
        return self.landmark_directions[lm_name]

    def get_landmark_direction_local(self, lm_name):
        """
        Returns the camera-local direction vector of a given landmark
        """
        if not lm_name in self.landmark_directions_local:
            px, py = self.landmark_pixels[lm_name]
            ndc_x = 2 * ((px + 0.5) / self.w) - 1
            ndc_y = 2 * ((py + 0.5) / self.h) - 1
            dir_local_x =  ndc_x * self._tan_hfov_2
            dir_local_z = -ndc_y * self._tan_vfov_2
            dir_local = np.array([dir_local_x, 1.0, dir_local_z])
            self.landmark_directions_local[lm_name] = dir_local
        return self.landmark_directions_local[lm_name]

    def get_pixel(self, world_xyz):
        """
        Returns the on-screen pixel of a given world point
        """
        return get_pixel(world_xyz, self.xyz, self.q, self.fov, self.size)

    def get_pixel_direction(self, pixel):
        """
        Returns the direction vector of a given pixel
        """
        return get_pixel_direction(pixel, self.q, self.fov, self.size)

    def get_point_at_zero_elevation(self, pixel):
        """
        Returns the point at which a ray through a given pixel intersects the ground plane
        """
        if pixel[1] <= self.get_horizon():
            raise ValueError("Pixel must be below the horizon")
        direction = self.get_pixel_direction(pixel)
        t  = -self.z / direction[2]
        return (self.x + t * direction[0], self.y + t * direction[1], 0)

    def open(self, scale=4, ratio=24/9):
        """
        Opens the camera image for rendering
        """
        self.scale = scale
        self.ratio = ratio
        self.image_h = int(round(self.h * self.scale))
        self.image_w = int(round(self.image_h * self.ratio))
        self.image = Image.new("RGB", (self.image_w, self.image_h), (255, 255, 255))
        og_ratio = self.w / self.h
        image_h = self.image_h
        image_w = int(round(image_h * og_ratio))
        self.offset = int(round((self.image_w - image_w) / 2))
        filename = f"{DIRNAME}/frames/{self.name}.png"
        if os.path.exists(filename):
            self.og_image = Image.open(filename)
            if self.og_image.size != (self.w, self.h):
                raise ValueError(
                    f"{self.name}: camera size is {self.size}, but image size is {self.og_image.size}"
                )
        else:
            self.og_image = Image.new("RGB", self.size, (240, 240, 240))
        self.image.paste(self.og_image.resize((image_w, image_h), Image.LANCZOS), (self.offset, 0))
        self.draw = ImageDraw.Draw(self.image)
        return self

    def project_camera(self, cam_name, opacity=0.5):
        """
        Projects another camera's image into this camera's image
        """
        if not hasattr(self, "image"): self.open()
        image_np = np.array(self.image)
        horizon = self.get_horizon()
        cam = get_camera(cam_name).open()
        cam_image_np = np.array(cam.og_image)
        cam_horizon = cam.get_horizon()
        cam_corners = (
            cam.get_point_at_zero_elevation((0, np.ceil(cam_horizon))),
            cam.get_point_at_zero_elevation((cam.w, np.ceil(cam_horizon))),
            cam.get_point_at_zero_elevation((0, cam.h)),
            cam.get_point_at_zero_elevation((cam.w, cam.h))
        )
        corners = [self.get_pixel(cam_corner) for cam_corner in cam_corners]
        if any(corner is None for corner in corners):
            min_x, max_x = 0, self.image_w
            min_y, max_y = np.ceil(horizon * self.scale), self.image_h
        else:
            min_x = min(corners, key=lambda xy: xy[0])[0] * self.scale + self.offset
            max_x = max(corners, key=lambda xy: xy[0])[0] * self.scale + self.offset
            min_y = min(corners, key=lambda xy: xy[1])[1] * self.scale
            max_y = max(corners, key=lambda xy: xy[1])[1] * self.scale
            min_x = max(min_x, 0)
            max_x = min(max_x, self.image_w)
            min_y = max(min_y, math.ceil(horizon * self.scale))
            max_y = min(max_y, self.image_h)
        print(f"Projecting {cam_name} onto {self.name}")
        for y in tqdm(range(int(min_y), int(max_y))):
            for x in range(int(min_x), int(max_x)):
                point = self.get_point_at_zero_elevation(((x - self.offset) / self.scale, y / self.scale))
                cam_pixel = cam.get_pixel(point)
                if not (cam_pixel is not None and 0 <= cam_pixel[0] < cam.w and 0 <= cam_pixel[1] < cam.h):
                    continue
                rgb = subsample(cam_image_np, cam_pixel)
                image_np[y][x] = image_np[y][x] * (1 - opacity) + np.array(rgb) * opacity
        self.image = Image.fromarray(image_np)
        self.draw = ImageDraw.Draw(self.image)
        return self

    def project_map(self, map_name, map_scale=None, opacity=0.5):
        """
        Projects a map image into this camera's image
        """
        if not hasattr(self, "image"): self.open()
        image_np = np.array(self.image)
        horizon = self.get_horizon()
        min_x, max_x = 0, self.image_w
        min_y, max_y = np.ceil(horizon * self.scale), self.image_h
        m = get_map(map_name).open(scale=map_scale)
        map_image_np = np.array(m.image)
        print(f"Projecting {map_name} onto {self.name}")
        for y in tqdm(range(int(min_y), int(max_y))):
            for x in range(int(min_x), int(max_x)):
                point = self.get_point_at_zero_elevation(((x - self.offset) / self.scale, y / self.scale))
                map_pixel = m.get_map_xy(point[:2])
                if not (0 <= map_pixel[0] < m.image.size[0] and 0 <= map_pixel[1] < m.image.size[1]):
                    continue
                rgb = subsample(map_image_np, map_pixel)
                image_np[y][x] = image_np[y][x] * (1 - opacity) + np.array(rgb) * opacity
        self.image = Image.fromarray(image_np)
        self.draw = ImageDraw.Draw(self.image)
        return self

    def register(self):
        """
        Adds this camera and its landmarks to gtamapdata's camera and landmark dicts
        """
        if self.name in md.cameras:
            get_camera.cache_clear()
        md.cameras[self.name] = {
            "id": self.id,
            "player": self.player,
            "xyz": self.xyz,
            "ypr": self.ypr,
            "fov": self.fov,
            "size": self.size
        }
        md.pixels[self.name] = self.landmark_pixels
        return self

    def render_all(self):
        """
        Runs all render functions
        """
        if not hasattr(self, "image"): self.open()
        self.render_player()
        self.render_vertical_lines()
        self.render_vanishing_points()
        self.render_distance_circles()
        self.render_cameras()
        self.render_rays()
        self.render_landmarks()
        self.render_pixels()
        self.render_camera_info()
        return self

    def render_camera_info(self):
        """
        Renders camera metadata
        """
        if not hasattr(self, "image"): self.open()
        d = 6 if self.hfov < 1 else 3
        text = (
            f"XYZ ({self.x:.3f}, {self.y:.3f}, {self.z:.3f}) "
            f"YPR ({self.yaw:.3f}, {self.pitch:.3f}, {self.roll:.3f}) "
            f"FOV ({self.hfov:.{d}f}, {self.vfov:.{d}f}) {self.id} {self.name}"
        )
        height = int(32 * self.scale)
        box = draw_box(text, height, (255, 255, 255), self.color)
        self.image.paste(box, (self.offset, self.image_h - height))
        return self

    def render_cameras(self, width=1):
        """
        Renders other cameras at their world positions
        """
        if not hasattr(self, "image"): self.open()
        cameras = [
            get_camera(cam_name) for cam_name in md.cameras
            if normalize_name(cam_name) != normalize_name(self.name)
        ]
        depth = 25
        for cam in sorted(cameras, key=lambda cam: -get_distance(self.xyz, cam.xyz)):
            if cam.hfov < 1: continue
            self.render_line((cam.xyz, (cam.x, cam.y, 0)), cam.color, width // 2)
            corners = (
                get_point(cam.xyz, cam.get_pixel_direction((0, 0)), depth),
                get_point(cam.xyz, cam.get_pixel_direction((cam.w, 0)), depth),
                get_point(cam.xyz, cam.get_pixel_direction((cam.w, cam.h)), depth),
                get_point(cam.xyz, cam.get_pixel_direction((0, cam.h)), depth)
            )
            for i, corner in enumerate(corners):
                self.render_line((cam.xyz, corner), cam.color, width)
                self.render_line((corner, corners[(i + 1) % 4]), cam.color, width)
            xy = self.get_pixel(cam.xyz)
            if xy is not None:
                dist = get_distance(self.xyz, cam.xyz)
                self.draw_label(xy, 10, f"{cam.name} {dist:.0f} m", (255, 255, 255), cam.color)
        return self

    def render_distance_circles(self, width=0.5):
        """
        Renders distance circles on the ground plane
        """
        if not hasattr(self, "image"): self.open()
        start = int(self.yaw - 60)
        stop = int(self.yaw + 60)
        step = 0.1
        for i, d in enumerate((1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000)):
            color = (255, 255, 0) if d == 100000 else [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i % 3]
            for deg in np.arange(start, stop, step * 2):
                rad_a = np.radians(deg + 90)
                rad_b = np.radians(deg + 90 + step)
                line = (
                    (self.x + np.cos(rad_a) * d, self.y + np.sin(rad_a) * d, 0),
                    (self.x + np.cos(rad_b) * d, self.y + np.sin(rad_b) * d, 0)
                )
                self.render_line(line, color, width)
        return self

    def render_landmarks(self, width=2):
        """
        Renders known landmarks at their world positions
        """
        if not hasattr(self, "image"): self.open()
        for lm_name, xyz in md.landmarks.items():
            nomalized = normalize_name(lm_name)
            if nomalized in LANDMARK_OBJECTS:
                LANDMARK_OBJECTS[nomalized].render_on_camera(self)
            else:
                self.render_line((xyz, (xyz[0], xyz[1], 0)), get_color(lm_name), width)
        return self

    def render_line(self, line, fill=(0, 0, 0), width=1):
        """
        Renders a line between world coordinates line[0] and line[1]
        """
        if not hasattr(self, "image"): self.open()
        line = [self.get_pixel(point) for point in line]
        if line[0] is not None and line[1] is not None:
            self.draw_line(line, fill, width)
        return self

    def render_object(self, obj):
        """
        Renders a special landmark object
        """
        if not hasattr(self, "image"): self.open()
        obj.render_on_camera(self)
        return self

    def render_pixels(self, width=1):
        """
        Renders landmark annotations and labels
        """
        if not hasattr(self, "image"): self.open()
        for lm_name, (x, y) in self.landmark_pixels.items():
            color = get_color(lm_name)
            self.draw_circle((x, y), 5, None, color, width)
            name = lm_name.replace("Four Seasons Hotel Miami", "FS")
            self.draw_label((x, y - 5), 5, name, color, (255, 255, 255))
        return self

    def render_player(self, width=1):
        """
        Renders the player, if present
        """
        if not hasattr(self, "image"): self.open()
        if not self.player: return self
        px, py, pz = self.player
        for i, line in enumerate((
            ((px - 1, py, pz), (px + 1, py, pz)),
            ((px, py - 1, pz), (px, py + 1, pz)),
            ((px, py, pz - 1), (px, py, pz + 1))
        )):
            fill = ((255, 0, 0), (0, 255, 0), (0, 0, 255))[i]
            self.render_line(line, fill, width * 4)
        for dz in (-0.1, 0, 0.1):
            for dy in (-0.1, 0, 0.1):
                for dx in (-0.1, 0, 0.1):
                    if dz == 0 or dy == 0 or dx == 0: continue
                    for i, line in enumerate((
                        ((px - dx, py + dy, pz + dz), (px + dx, py + dy, pz + dz)),
                        ((px + dx, py - dy, pz + dz), (px + dx, py + dy, pz + dz)),
                        ((px + dx, py + dy, pz - dz), (px + dx, py + dy, pz + dz))
                    )):
                        fill = ((255, 0, 0), (0, 255, 0), (0, 0, 255))[i]
                        self.render_line(line, fill, width)
        return self

    def render_rays(self, width=0.5):
        """
        Renders rays from other cameras towards annotated landmarks
        """
        if not hasattr(self, "image"): self.open()
        for cam_name in md.cameras:
            if cam_name == self.name: continue
            cam = get_camera(cam_name)
            for lm_name in cam.landmark_pixels:
                if lm_name not in self.landmark_pixels: continue
                if normalize_name(lm_name) in ("Player", "Minimap", "AIWE"): continue
                direction = cam.get_landmark_direction(lm_name)
                m, a, b, _, _ = find_landmark(self.name, cam_name, lm_name)
                # FIXME
                # assert np.allclose(direction, get_direction(cam.xyz, b))
                dist = get_distance(cam.xyz, b)
                length = dist / 10
                lm_color = get_color(lm_name)
                self.render_line((
                    get_point(cam.xyz, direction, dist - length * 0.5),
                    get_point(cam.xyz, direction, dist - length * 0.4)
                ), cam.color, width)
                self.render_line((
                    get_point(cam.xyz, direction, dist - length * 0.4),
                    get_point(cam.xyz, direction, dist + length * 0.5)
                ), lm_color, width)
        return self

    def render_vanishing_points(self, width=0.5):
        """
        Renders lines towards horizontal and vertical vanishing points
        """
        if not hasattr(self, "image"): self.open()
        for a, b in self.lines[0]:
            self.draw_circle(a, 3, None, (255, 255, 0), width)
            self.draw_circle(b, 3, None, (255, 255, 0), width)
            self.draw_line((a, self.get_hvp()), (255, 255, 0), width)
        for a, b in self.lines[1]:
            self.draw_circle(a, 3, None, (255, 255, 0), width)
            self.draw_circle(b, 3, None, (255, 255, 0), width)
            vvp = self.get_vvp() or (a[0], self.h)
            self.draw_line((a, vvp), (255, 255, 0), width)
        return self

    def render_vertical_lines(self, width=0.25):
        """
        Renders vertical lines that align with world verticals
        """
        if not hasattr(self, "image"): self.open()
        start = int(self.yaw - 60)
        stop = int(self.yaw + 60)
        step = 0.5
        for deg in np.arange(start, stop, step):
            rad = np.radians(deg + 90)
            xy = (self.x + np.cos(rad) * 10, self.y + np.sin(rad) * 10)
            line = (
                (xy[0], xy[1], self.z + 10),
                (xy[0], xy[1], self.z - 10)
            )
            self.render_line(line, (255, 255, 0), width)
        return self

    def save(self, filename, crop=None):
        """
        Saves the current camera image
        """
        if not hasattr(self, "image"): self.open()
        print(f"Writing {filename}", end=" ... ", flush=True)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.image.resize((
            int(round(self.image.size[0] / self.scale)),
            int(round(self.image.size[1] / self.scale))
        ), Image.LANCZOS).save(filename)
        print("Done")
        return self

    def set_fov(self, fov):
        """
        Sets horizontal and vertical fov
        """
        if fov[0] is not None:
            self.hfov = fov[0]
            self.vfov = get_vfov(self.hfov, self.size)
        else:
            self.vfov = fov[1]
            self.hfov = get_hfov(self.vfov, self.size)
        self.fov = self.hfov, self.vfov
        self._tan_hfov_2 = np.tan(np.radians(self.hfov) / 2)
        self._tan_vfov_2 = np.tan(np.radians(self.vfov) / 2)
        self.clear_landmark_directions(include_local=True)
        return self

    def set_q(self, q):
        """
        Sets quaternion
        """
        self.q = q
        self.yaw, self.pitch, self.roll = get_ypr(self.q)
        self.clear_landmark_directions()
        return self

    def set_ypr(self, ypr):
        """
        Sets yaw, pitch and roll
        """
        self.ypr = ypr
        self.yaw, self.pitch, self.roll = ypr
        self.q = get_q(self.ypr)
        self.clear_landmark_directions()
        return self

    def set_size(self, size):
        """
        Sets image size
        """
        self.size = size
        self.w, self.h = self.size
        self.clear_landmark_directions(include_local=True)
        return self

    def set_xyz(self, xyz):
        """
        Sets camera position
        """
        self.xyz = xyz
        self.xy = self.xyz[:2]
        self.x, self.y, self.z = self.xyz
        return self

    def test_lines(self):
        """
        Test if horizontal and vertical lines agree with pitch
        """
        pitch_h = self._get_pitch_from_hlines()
        pitch_v = self._get_pitch_from_vlines()
        if pitch_h is None and pitch_v is None:
            print(f"{self.name}: Pitch is {self.pitch:.3f}, no lines defined")
        if pitch_h is not None:
            print(f"{self.name}: Pitch is {self.pitch:.3f}, ", end="")
            if f"{self.pitch:.3f}" == f"{pitch_h:.3f}":
                print("horizontal lines agree")
            else:
                print(f"but horizontal lines suggest {pitch_h:.3f}")
        if pitch_v is not None:
            print(f"{self.name}: Pitch is {self.pitch:.3f}, ", end="")
            if f"{self.pitch:.3f}" == f"{pitch_v:.3f}":
                text = ("line agrees", "lines agree")[len(self.lines[1]) > 1]
                print(f"vertical {text}")
            else:
                text = ("line suggests", "lines suggest")[len(self.lines[1]) > 1]
                print(f"but vertical {text} {pitch_v:.3f}")
        return self

    def test_player(self):
        """
        Test if player pixel agrees with yaw
        """
        print(f"{self.name}: Yaw is {self.yaw:.3f}, ", end="")
        if not self.player:
            print("no player defined")
        elif not "Player" in self.landmark_pixels:
            print("no player pixel defined")
        else:
            yaw = self.yaw
            self.calibrate_yaw("Player", self.player)
            player_yaw = self.yaw
            self.set_ypr((yaw, self.pitch, self.roll))
            if f"{self.yaw:.3f}" == f"{player_yaw:.3f}":
                print("player pixel agrees")
            else:
                print(f"but player pixel suggests {player_yaw:.3f}")
        return self


@lru_cache(maxsize=None)
def get_camera(name):
    """
    Returns a camera by name
    """
    cam = md.cameras[name]
    return Camera(
        id=cam["id"],
        name=name,
        player=cam["player"],
        xyz=cam["xyz"],
        ypr=cam["ypr"],
        fov=cam["fov"],
        size=cam["size"],
        pixels=md.pixels.get(name),
        lines=md.lines.get(name)
    )


### MAP ############################################################################################

class Map:

    def __init__(self, name, version, scale, zero, filename):
        self.name = name
        self.version = version
        self.og_scale = scale
        self.scale = self.og_scale
        self.og_zero = zero
        self.zero = self.og_zero
        self.filename = filename
        self.cropped = None
        self.section_name = None

    def __repr__(self):
        return f"<Map {self.name} v{self.version} {self.og_scale} {self.og_zero}>"

    def crop(self, crop, section_name=None):
        """
        Crops the map image
        """
        self.cropped = crop
        self.section_name = section_name
        x0, y0, x1, y1 = self.cropped 
        x0, y0 = self.get_map_xy((x0, y0))
        x1, y1 = self.get_map_xy((x1, y1))
        return self.image.crop((x0, y1, x1, y0))

    def draw_all(self):
        """
        Runs all draw functions
        """
        if not hasattr(self, "image"): self.open()
        self.draw_rays()
        self.draw_cameras()
        self.draw_landmarks()
        return self        

    def draw_camera(self, cam_name, r=8, d=100, _no_marker=False):
        """
        Draws a camera symbol
        """
        if not hasattr(self, "image"): self.open()
        cam = get_camera(cam_name)
        for x in (0, cam.w):
            target_xy = get_point(cam.xyz, cam.get_pixel_direction((x, cam.h / 2)), d)[:2]
            self.draw_line((cam.xy, target_xy), (255, 255, 255), 1)
        if not _no_marker:
            self.draw_circle(cam.xy, r, (255, 255, 255), cam.color, 1, cam.name[0])
        return self

    def draw_cameras(self, r=10, d=100):
        """
        Draws all known cameras
        """
        if not hasattr(self, "image"): self.open()
        cams = sorted(
            [get_camera(cam_name) for cam_name in md.cameras],
            key=lambda cam: (cam.z, cam.y, cam.x)
        )
        for cam in cams:
            self.draw_camera(cam.name, r=r, d=d)
        return self

    def draw_circle(self, xy, r, fill=(255, 255, 255), outline=(0, 0, 0), width=1, text=None):
        """
        Draws a circle at the given image coordinates
        """
        if not hasattr(self, "image"): self.open()
        xy = self.get_map_xy(xy)
        r *= self.scale
        self.draw.circle(xy, r, fill=fill, outline=outline, width=width)
        if text:
            x, y = xy
            font = ImageFont.truetype(f"{DIRNAME}/fonts/Menlo-Regular.ttf", r * 1.6)
            w, h = get_textsize(text, font)
            self.draw.text((x - w * 0.4, y - h * 0.7), text, fill=outline, font=font)
        return self

    def draw_landmark(self, lm_name, r=10):
        """
        Draws a landmark symbol
        """
        if not hasattr(self, "image"): self.open()
        xy = md.landmarks[lm_name][:2]
        color = get_color(lm_name)
        letter = get_letter(lm_name)
        self.draw_circle(xy, r, color, (255, 255, 255), 1, letter)
        return self

    def draw_landmarks(self, r=10):
        """
        Draws all known landmarks
        """
        if not hasattr(self, "image"): self.open()
        landmarks = sorted(
            md.landmarks.items(),
            key=lambda kv: (kv[1][2], kv[1][1], kv[1][0])
        )
        for lm_name, _ in landmarks:
            self.draw_landmark(lm_name, r=r)
            # nomalized = normalize_name(lm_name)
            # if nomalized in LANDMARK_OBJECTS:
            #     LANDMARK_OBJECTS[nomalized].draw_on_map(self)
            # else:
            #     self.draw_landmark(lm_name, r=r)
        return self

    def draw_line(self, line, fill=(0, 0, 0), width=1):
        """
        Draws a line between world coordinates line[0] and line[1]
        """
        if not hasattr(self, "image"): self.open()
        x0, y0 = self.get_map_xy(line[0])
        x1, y1 = self.get_map_xy(line[1])
        self.draw.line((x0, y0, x1, y1), fill=fill, width=width)
        return self

    def draw_map_info(self, image, height=32):
        """
        Draws map metadata
        """
        if not hasattr(self, "image"): self.open()
        if self.cropped:
            sw = self.cropped[0], self.cropped[1]
            ne = self.cropped[2], self.cropped[2]
        else:
            sw = self.get_world_xy((0, image.size[1]))
            ne = self.get_world_xy((image.size[0], 0))
        section_name = f" {self.section_name.upper()}" if self.section_name else "" 
        text = (
            f"SW ({sw[0]:.3f}, {sw[1]:.3f}) "
            f"NE ({ne[0]:.3f}, {ne[1]:.3f}) "
            f"SCALE {self.scale:.3f} PX/M "
            f"{self.name.upper()} V{self.version}{section_name}"
        )
        height = int(height * self.scale)
        box = draw_box(text, height, (255, 255, 255), (128, 128, 128))
        image.paste(box, (0, image.size[1] - height))
        return self

    def draw_object(self, obj):
        """
        Draws a special landmark object
        """
        if not hasattr(self, "image"): self.open()
        obj.draw_on_map(self)
        return self

    def draw_rays(self, r=6):
        """
        Draws all rays from cameras towards landmarks, and symbols at their intersections
        """
        if not hasattr(self, "image"): self.open()
        cameras = sorted(
            [get_camera(cam_name) for cam_name in md.cameras],
            key=lambda cam: (cam.z, cam.y, cam.x)
        )
        rays = {}
        for cam in cameras:
            for lm_name in cam.landmark_pixels:
                if normalize_name(lm_name) in ("Player", "Minimap", "AIWE"): continue
                direction = cam.get_landmark_direction(lm_name)
                target_xy = get_point(cam.xyz, direction, 10000)[:2]
                ray = (cam.xy, target_xy)
                color = get_color(lm_name)
                self.draw_line(ray, color, 1)
                rays[lm_name] = rays.get(lm_name, []) + [ray]
        for lm_name, lm_rays in rays.items():
            color = get_color(lm_name)
            letter = get_letter(lm_name)
            for i, ray_a in enumerate(lm_rays):
                for j, ray_b in enumerate(lm_rays):
                    if i >= j: continue
                    inter = intersect_lines_2d(ray_a, ray_b)
                    if not inter: continue
                    self.draw_circle(inter, r, color, (255, 255, 255), 1, letter)
        return self

    def draw_rectangle(self, xy0, xy1, fill=(255, 255, 255), outline=(0, 0, 0), width=1):
        """
        Draws a rectangle with SW and NE world coordinates xy0 and xy1
        """
        if not hasattr(self, "image"): self.open()
        x0, y1 = self.get_map_xy(xy0)
        x1, y0 = self.get_map_xy(xy1)
        self.draw.rectangle((x0, y0, x1, y1), fill=fill, outline=outline, width=width)
        return self

    def get_map_xy(self, xy):
        """
        Returns the map xy of a given world xy
        """
        return (
            self.zero[0] + xy[0] * self.scale,
            self.zero[1] - xy[1] * self.scale
        )

    def get_world_xy(self, xy):
        """
        Returns the world xy of a given map xy
        """
        return (
            (xy[0] - self.zero[0]) / self.scale,
            (self.zero[1] - xy[1]) / self.scale
        )

    def open(self, scale=None, add_padding=False):
        """
        Opens the map image for drawing
        """
        self.image = Image.open(self.filename).convert("L").convert("RGB")
        if add_padding:
            km = int(self.scale * 1000)
            self.og_zero = tuple(np.asarray(self.og_zero) + km)
            self.zero = self.og_zero
            size = tuple(np.asarray(self.image.size) + 2 * km)
            image = Image.new("RGB", size, (128, 128, 128))
            draw = ImageDraw.Draw(image)
            for dx in range(km * -16, km * 16 + 1, km):
                x = self.zero[0] + dx
                if 0 <= x < image.size[0]:
                    draw.line((x, 0, x, image.size[1]), fill=(112, 112, 112), width=1)
            for dy in range(km * -16, km * 16 + 1, km):
                y = self.zero[1] + dy
                if 0 <= x < image.size[1]:
                    draw.line((0, y, image.size[0], y), fill=(112, 112, 112), width=1)
            image.paste(self.image, (km, km))
            self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.og_size = self.image.size
        self.size = self.og_size
        if scale:
            self.scale = scale
            self.zero = (
                self.og_zero[0] / self.og_scale * self.scale,
                self.og_zero[1] / self.og_scale * self.scale
            )
            self.size = (
                int(round(self.og_size[0] / self.og_scale * self.scale)),
                int(round(self.og_size[1] / self.og_scale * self.scale))
            )
            print(f"Resizing map to {self.size}", end=" ... ", flush=True)
            self.image = self.image.resize(self.size, Image.LANCZOS)
            print("Done")
            self.draw = ImageDraw.Draw(self.image)
        return self 

    def project_camera(self, cam_names, area=None, r=(0, 10000)):
        """
        Projects a camera image onto the map
        """
        if not hasattr(self, "image"): self.open()
        if type(cam_names) is str: cam_names = [cam_names]
        cams = [get_camera(cam_name).open() for cam_name in cam_names]
        cam_images_np = [np.array(cam.og_image) for cam in cams]
        if area:
            map_x0, map_y0 = self.get_map_xy((area[0], area[3]))
            map_x1, map_y1 = self.get_map_xy((area[2], area[1]))
            map_x1 = min(map_x1, self.size[0])
            map_y1 = min(map_y1, self.size[1])
        else:
            map_x0, map_y0 = 0, 0
            map_x1, map_y1 = self.size
        pixels = {}
        print(f"Projecting {' + '.join(cam_names)} onto {self.name}")
        for map_y in tqdm(range(map_y0, map_y1)):
            for map_x in range(map_x0, map_x1):
                map_xy = map_x, map_y
                world_xy = self.get_world_xy(map_xy)
                world_x, world_y = world_xy
                for i, cam in enumerate(cams):
                    bearing = get_bearing(cam.xy, world_xy)
                    delta = (bearing - cam.yaw + 180) % 360 - 180
                    if abs(delta) > cam.hfov / 2:
                        continue  # not in the cone of vision
                    distance = math.dist(cam.xy, world_xy)
                    if not (r[0] <= distance <= r[1]):
                        continue  # not within the distance
                    cam_pxy = cam.get_pixel((world_x, world_y, 0))
                    if cam_pxy is None:
                        continue  # not in front of the camera
                    cam_px, cam_py = cam_pxy
                    if not (0 <= cam_px < cam.w and 0 <= cam_py < cam.h):
                        continue  # not in the image
                    rgb = subsample(cam_images_np[i], cam_pxy)
                    pixels[map_xy] = pixels.get(map_xy, []) + [rgb]
        image_np = np.array(self.image)
        for (map_x, map_y), rgbs in tqdm(pixels.items(), total=len(pixels)):
            rgb = tuple(np.mean(rgbs, axis=0).astype(np.uint8))
            image_np[map_y][map_x] = rgb
        self.image = Image.fromarray(image_np)
        self.draw = ImageDraw.Draw(self.image)
        return self

    def project_camera_parallel(self, cam_names, area=None, r=(0, 10000)):
        """
        Projects a camera image onto the map (multi-threaded)
        """

        if not hasattr(self, "image"): self.open()
        if type(cam_names) is str: cam_names = [cam_names]
        cams = [get_camera(cam_name).open() for cam_name in cam_names]
        cam_images_np = [np.array(cam.og_image) for cam in cams]
        if area:
            map_x0, map_y0 = self.get_map_xy((area[0], area[3]))
            map_x1, map_y1 = self.get_map_xy((area[2], area[1]))
            map_x0 = int(max(map_x0, 0))
            map_y0 = int(max(map_y0, 0))
            map_x1 = int(min(map_x1, self.size[0]))
            map_y1 = int(min(map_y1, self.size[1]))
        else:
            map_x0, map_y0 = 0, 0
            map_x1, map_y1 = self.size

        pixels = {}
        print(f"Projecting {' + '.join(cam_names)} onto {self.name}")
        cam_values = [
            (cam.xyz, cam.q, cam.ypr, cam.fov, cam.size)
            for cam in cams
        ]
        pool_args = [
            (self.scale, self.zero, map_y, map_x0, map_x1, r, cam_values, cam_images_np)
            for map_y in range(map_y0, map_y1)
        ]
        with multiprocessing.Pool() as pool:
            for results in tqdm(
                pool.imap_unordered(_project_camera_parallel, pool_args),
                total=len(pool_args)
            ):
                for map_xy, rgbs in results.items():
                    pixels[map_xy] = rgbs

        image_np = np.array(self.image)
        for (map_x, map_y), rgbs in tqdm(pixels.items(), total=len(pixels)):
            rgb = tuple(np.mean(rgbs, axis=0).astype(np.uint8))
            image_np[map_y][map_x] = rgb
        self.image = Image.fromarray(image_np)
        self.draw = ImageDraw.Draw(self.image)
        return self

    def save(self, filename, crop=None, section_name=None, map_info_height=None):
        """
        Saves the current map image
        """
        if not hasattr(self, "image"): self.open()
        image = self.crop(crop, section_name) if crop else self.image
        if map_info_height is not None:
            self.draw_map_info(image, height=map_info_height)
        else:
            self.draw_map_info(image)
        print(f"Writing {filename}", end=" ... ", flush=True)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        image.save(filename)
        print("Done")
        return self


def get_map(name):
    """
    Returns a map by name
    """
    m = md.maps[name]
    return Map(
        name=name,
        version=m["version"],
        scale=m["scale"],
        zero=m["zero"],
        filename=m["filename"],
    )

def _project_camera_parallel(args):
    """
    Camera projection worker function
    """
    map_scale, map_zero, map_y, map_x0, map_x1, r, cam_values, cam_images_np = args
    get_world_xy = lambda xy: (
        (xy[0] - map_zero[0]) / map_scale,
        (map_zero[1] - xy[1]) / map_scale
    )
    pixels = {}
    for map_x in range(map_x0, map_x1):
        map_xy = map_x, map_y
        for i, (cam_xyz, cam_q, cam_ypr, cam_fov, cam_size) in enumerate(cam_values):
            world_xy = get_world_xy(map_xy)
            world_x, world_y = world_xy
            bearing = get_bearing(cam_xyz[:2], world_xy)
            delta = (bearing - cam_ypr[0] + 180) % 360 - 180
            if abs(delta) > cam_fov[0] / 2:
                continue  # not in the cone of vision
            distance = math.dist(cam_xyz[:2], world_xy)
            if not (r[0] <= distance <= r[1]):
                continue  # not within the distance
            cam_pxy = get_pixel((world_x, world_y, 0), cam_xyz, cam_q, cam_fov, cam_size)
            if cam_pxy is None:
                continue  # not in front of the camera
            cam_px, cam_py = cam_pxy
            if not (0 <= cam_px < cam_size[0] and 0 <= cam_py < cam_size[1]):
                continue  # not in the image
            rgb = subsample(cam_images_np[i], cam_pxy)
            pixels[map_xy] = pixels.get(map_xy, []) + [rgb]
    return pixels


### LANDMARKS #####################################################################################

LANDMARK_OBJECTS = {}

class Landmark:

    def __init__(self, name):
        self.name = name
        self.color = get_color(self.name)
        LANDMARK_OBJECTS[self.name] = self


class FourSeasons(Landmark):

    def __init__(
        self,
        fs40ne=(-800.000, -1273.000, 189.137),
        fs40nw=(-848.707, -1254.789, 189.137),
        fs40w=(-858.163, -1280.079, 189.137),
        fs40e=(-809.456, -1298.290, 189.137),
        fs56ne=(-802.124, -1273.968, 253.608),
        fs56nw=(-847.739, -1256.913, 253.608),
        fs56sw=(-863.612, -1299.367, 253.608),
        fs56se=(-817.997, -1316.422, 253.608),
        fs57ne=(-802.124, -1273.968, 258.306),
        hb8se=(-815.574, -1309.942, 60.196),
        hb28se=(-816.865, -1313.394, 140.784),
        hb58se=(-814.289, -1306.504, 263.568),
        hb58ne=(-813.449, -1304.257, 262.428),
    ):
        super().__init__("Four Seasons Hotel Miami")
        self.fs40ne = fs40ne
        self.fs40nw = fs40nw
        self.fs40w = fs40w
        self.fs40e = fs40e
        self.fs56ne = fs56ne
        self.fs56nw = fs56nw
        self.fs56sw = fs56sw
        self.fs56se = fs56se
        self.fs57ne = fs57ne
        self.hb8se = hb8se
        self.hb28se = hb28se
        self.hb58se = hb58se
        self.hb58ne = hb58ne
        self._construct()
        self.floor_height = (self.fs56ne[2] - self.fs40ne[2]) / 16
        self.penthouse_height = (self.fs57ne[2] - self.fs56ne[2])

    def __repr__(self):
        center = ((np.array(self.fs56ne) + np.array(self.fs56sw)) / 2)[:2]
        return (
            f"<{self.name}\n"
            f"Center: ({center[0]:.3f}, {center[1]:.3f})\n"
            f"Orientation: {get_bearing(self.fs56se[:2], self.fs56ne[:2]):.3f} deg\n"
            f"Size (East-West): {math.dist(self.fs56ne, self.fs56nw):.3f} m\n"
            f"Size (North-South): {math.dist(self.fs56ne, self.fs56se):.3f} m\n"
            f"Height (Rooftop): {self.fs56ne[2]:.3f} m\n"
            f"Height (Penthouse): {self.fs57ne[2]:.3f} m\n"
            f"Height (Handlebar): {self.hb58sw[2]:.3f} m\n"
            f"Floor height: {self.floor_height:.3f} m\n"
            f"Penthouse height: {self.penthouse_height:.3f} m>"
        )

    def _args(self):
        return "\n".join([
            f"    {arg}=(" + ", ".join([
                f"{v:.3f}"
                for v in getattr(self, arg)
            ]) + "),"
            for arg in (
                "fs40ne", "fs40nw", "fs40w", "fs40e",
                "fs56ne", "fs56nw", "fs56sw", "fs56se",
                "fs57ne", "hb8se", "hb28se", "hb58se", "hb58ne"
            )
        ])

    def _construct(self):
        dir_n = get_direction(self.fs40e, self.fs40ne)
        dir_s = get_direction(self.fs40ne, self.fs40e)
        dir_w = get_direction(self.fs40ne, self.fs40nw)
        # 56th floor
        self.fs56w = intersect_ray_and_plane(
            (self.fs56nw, dir_s),
            (self.fs40w, dir_n)
        )
        self.fs56e = intersect_ray_and_plane(
            (self.fs56ne, dir_s),
            (self.fs40e, dir_n)
        )
        # 57th floor
        self.fs57nw = (self.fs56nw[0], self.fs56nw[1], self.fs57ne[2])
        self.fs57w = (self.fs56sw[0], self.fs56sw[1], self.fs57ne[2])
        self.fs57e = (self.fs56se[0], self.fs56se[1], self.fs57ne[2])
        # handlebars
        self.hb8sw = get_point(
            self.hb8se, dir_w, math.dist(self.fs56ne, self.fs56nw)
        )
        self.hb28sw = get_point(
            self.hb28se, dir_w, math.dist(self.fs56ne, self.fs56nw)
        )
        self.hb58sw = get_point(
            self.hb58se, dir_w, math.dist(self.fs56ne, self.fs56nw)
        )
        self.hb58nw = get_point(
            self.hb58ne, dir_w, math.dist(self.fs56ne, self.fs56nw)
        )

    def _get_hbs_at_floor(self, side, floor):
        hb8 = np.array(self.hb8se if side == "e" else self.hb8sw)
        hb28 = np.array(self.hb28se if side == "e" else self.hb28sw)
        hb58 = np.array(self.hb58se if side == "e" else self.hb58sw)
        if floor < 8:
            return self._get_point_at_floor(hb8, floor)
        if floor < 28:
            t = (floor - 8) / 20
            return tuple((hb8 * (1 - t) + hb28 * t).tolist())
        t = (floor - 28) / 30
        return tuple((hb28 * (1 - t) + hb58 * t).tolist())

    def _get_point_at_floor(self, point, floor):
        return (point[0], point[1], self._get_z(floor))

    def _get_z(self, floor):
        if floor == -1:
            return 0
        if floor <= 56:
            return self.fs56ne[2] - self.floor_height * (56 - floor)
        return self.fs57ne[2]

    def _landmarks(self):
        return "\n".join([
            f'    "Four Seasons Hotel Miami ({corner})": (' + ", ".join([
                f"{v:.3f}"
                for v in point
            ]) + f"),  # {comment}"
            for corner, point, comment in (
                ("BE", self.hb58se, "Handlebar (SE)"),
                ("BW", self.hb58sw, "Handlebar (SW)"),
                ("E", self.fs57e, "Penthouse (SE)"),
                ("NE", self.fs57ne, "Penthouse (NE)"),
                ("NW", self.fs57nw, "Penthouse (NW)"),
                ("SE", self.fs56se, "Rooftop (SE)"),
                ("SW", self.fs56sw, "Penthouse (SW)"),
                ("W", self.fs57e, "Penthouse (SW)"),
            )
        ])

    def draw_on_map(self, m, width=2):
        m.draw_line((self.fs40ne, self.fs40nw), self.color, width // 2)
        m.draw_line((self.fs40nw, self.fs40w), self.color, width // 2)
        m.draw_line((self.fs40w, self.fs40e), self.color, width // 2)
        m.draw_line((self.fs40e, self.fs40ne), self.color, width // 2)
        m.draw_line((self.fs56ne, self.fs56nw), self.color, width)
        m.draw_line((self.fs56nw, self.fs56sw), self.color, width)
        m.draw_line((self.fs56sw, self.fs56se), self.color, width)
        m.draw_line((self.fs56se, self.fs56ne), self.color, width)
        m.draw_line((self.hb58nw, self.hb58ne), self.color, width // 2)
        m.draw_line((self.hb58sw, self.hb58se), self.color, width // 2)
        return self

    def render_on_camera(self, cam):
        distances = [math.dist(cam.xy, corner[:2]) for corner in (
           self.fs57ne, self.fs57nw, self.fs56sw, self.fs56se, 
        )]
        hidden = distances.index(max(distances))
        thin, bold = 0.25, 1.0
        for bottom, top, has_box, has_south in (
            (-1, 0, 0, 1),
            (0, 8, 1, 1),
            (8, 16, 0, 1),
            (16, 24, 1, 1),
            (24, 32, 0, 1),
            (32, 40, 1, 1),
            (40, 56, 0, 1),
            (56, 57, 0, 0)
        ):
            for floor in range(bottom, top + 1):
                ne = self._get_point_at_floor((self.fs56ne, self.fs40ne)[has_box], floor)
                nw = self._get_point_at_floor((self.fs56nw, self.fs40nw)[has_box], floor)        
                wo = self._get_point_at_floor((self.fs56w, self.fs40w)[has_box], floor)
                wi = self._get_point_at_floor(self.fs56w, floor)
                hbnw = self._get_point_at_floor(self.hb58nw, floor)
                hbsw = self._get_hbs_at_floor("w", floor)
                sw = self._get_point_at_floor((self.fs56w, self.fs56sw)[has_south], floor)
                se = self._get_point_at_floor((self.fs56e, self.fs56se)[has_south], floor)
                hbse = self._get_hbs_at_floor("e", floor)
                hbne = self._get_point_at_floor(self.hb58ne, floor)
                ei = self._get_point_at_floor(self.fs56e, floor)
                eo = self._get_point_at_floor((self.fs56e, self.fs40e)[has_box], floor)
                width = bold if floor % 2 == 0 and has_south else thin
                if hidden not in (0, 1):  # from north
                    cam.render_line((ne, nw), self.color, thin)
                if hidden not in (1, 2):  # from west
                    cam.render_line((nw, wo), self.color, thin)
                    if floor <= 8:
                        cam.render_line((wi, sw), self.color, width)
                    elif floor < 28:
                        cam.render_line((wi, hbnw), self.color, bold)
                        cam.render_line((hbsw, sw), self.color, width)
                    elif has_south:
                        cam.render_line((wi, hbnw), self.color, bold)
                        cam.render_line((hbnw, sw), self.color, width)
                if hidden == 0:  # from southwest
                    cam.render_line((wo, wi), self.color, thin)
                if hidden not in (2, 3):  # from south
                    cam.render_line((sw, se), self.color, width)
                if hidden == 1:  # from southeast
                    cam.render_line((ei, eo), self.color, thin)
                if hidden not in (3, 0):  # from east
                    if floor <= 8:
                        cam.render_line((se, ei), self.color, width)
                    elif floor < 28:
                        cam.render_line((se, hbse), self.color, width)
                        cam.render_line((hbne, ei), self.color, bold)
                    elif has_south:
                        cam.render_line((se, hbne), self.color, width)
                        cam.render_line((hbne, ei), self.color, bold)
                    cam.render_line((eo, ne), self.color, thin)
                if floor == top: continue
                if hidden != 0:  # from northeast
                    cam.render_line((ne, self._get_point_at_floor(ne, floor + 1)), self.color, thin)
                if hidden != 1:  # ftom northwest
                    cam.render_line((nw, self._get_point_at_floor(nw, floor + 1)), self.color, thin)
                if hidden not in (1, 2):  # from west
                    cam.render_line((wo, self._get_point_at_floor(wo, floor + 1)), self.color, thin)
                    cam.render_line((wi, self._get_point_at_floor(wi, floor + 1)), self.color, thin)
                if hidden != 2:  # from southwest
                    cam.render_line((sw, self._get_point_at_floor(sw, floor + 1)), self.color, thin)
                if hidden != 3:  # from southeast
                    cam.render_line((se, self._get_point_at_floor(se, floor + 1)), self.color, thin)
                if hidden not in (3, 0):  # from east
                    cam.render_line((ei, self._get_point_at_floor(ei, floor + 1)), self.color, thin)
                    cam.render_line((eo, self._get_point_at_floor(eo, floor + 1)), self.color, thin)
            cam.render_line((self.hb58nw, self._get_point_at_floor(self.hb58nw, 56)), self.color, bold)
            cam.render_line((self.hb58nw, self.hb58ne), self.color, bold)
            cam.render_line((self.hb58ne, self._get_point_at_floor(self.hb58ne, 56)), self.color, bold)
            cam.render_line((self.hb58sw, self._get_hbs_at_floor("w", 56)), self.color, bold)
            cam.render_line((self.hb58sw, self.hb58se), self.color, bold)
            cam.render_line((self.hb58se, self._get_hbs_at_floor("e", 56)), self.color, bold)
            if hidden not in (1, 2):  # from west
                cam.render_line((self.hb58nw, self._get_point_at_floor(self.hb58nw, 8)), self.color, bold)
                cam.render_line((self.hb58sw, self.hb28sw), self.color, bold)
                cam.render_line((self.hb28sw, self.hb8sw), self.color, bold)
            if hidden not in (3, 0):  # from east
                cam.render_line((self.hb58ne, self._get_point_at_floor(self.hb58ne, 8)), self.color, bold)
                cam.render_line((self.hb58se, self.hb28se), self.color, bold)
                cam.render_line((self.hb28se, self.hb8se), self.color, bold)
        return self


class SunshineSkywayBridge(Landmark):

    def __init__(
        self,
        nt=(-6843.266, 4580.690, 141.185),
        st=(-6759.214, 4351.692, 141.185),
        rz=31.185
    ):
        super().__init__("Sunshine Skyway Bridge")
        self.nt = nt
        self.st = st
        self.rz = rz
        self._construct()

    def _construct(self):
        self.direction = get_direction(self.st, self.nt)
        length = 110
        self.rs = get_point((self.st[0], self.st[1], self.rz), -self.direction, length)
        self.rn = get_point((self.nt[0], self.nt[1], self.rz), self.direction, length)

    def draw_on_map(self, m, width=1):
        m.draw_line((self.rs, self.rn), self.color, width * 2)
        m.draw_circle(self.nt, width * 5, self.color, (255, 255, 255), width)
        m.draw_circle(self.st, width * 5, self.color, (255, 255, 255), width)

    def render_on_camera(self, cam):
        cam.render_line((self.nt, (self.nt[0], self.nt[1], 0)), fill=self.color, width=4)
        cam.render_line((self.st, (self.st[0], self.st[1], 0)), fill=self.color, width=4)
        cam.render_line((self.rs, self.rn), fill=self.color, width=2)
        n_cables = 10
        gap = (self.nt[2] - self.rz) / n_cables
        for pillar in (self.nt, self.st):
            for direction in (self.direction, -self.direction):
                for i in range(n_cables):
                    base_point = (pillar[0], pillar[1], self.rz)
                    road_point = get_point(base_point, direction, (i + 1) * gap)
                    pillar_point = get_point(base_point, [0, 0, 1], (i + 1) * gap)
                    cam.render_line((road_point, pillar_point), fill=self.color, width=0.5)
        return self


### AIWE ##########################################################################################

class AIWE:

    def __init__(self, scale=0.68, point=(-6420.1, 3062.3), pixel=(290, 306)):
        self.scale = scale
        self.point = point
        self.pixel = pixel
        self.west, self.north = self.get_world_xy((0, 0))

    def get_aiwe_xy(self, world_xy):
        return (
            (world_xy[0] - self.west) * self.scale,
            (self.north - world_xy[1]) * self.scale
        )

    def get_world_xy(self, aiwe_xy):
        return (
            self.point[0] + (aiwe_xy[0] - self.pixel[0]) / self.scale,
            self.point[1] - (aiwe_xy[1] - self.pixel[1]) / self.scale
        )


### FIND ##########################################################################################

def find_camera(
    cam_name, lm_names, rays,
    line, radius, step,
    z_limits, pitch_range, hfov_range,
    map_name, map_scale, map_area,
    projection_area,
    basename
):
    """
    Finds the optimal camera position and settings within a given map region,
    constrained by ranges for pitch and horizontal fov, using a list of known
    landmark positions and a list of rays from known cameras towards visible
    landmarks. The minimized loss is the mean squared angular delta between
    rays and their targets, in arcminutes. Renders the log loss landscape of
    the results, and the camera view after optimal calibration.
    """

    cam = get_camera(cam_name)
    # these targets are (lm_name, point)
    targets = [
        (lm_name, md.landmarks[lm_name] if lm_name in md.landmarks else get_camera(lm_name).xyz)
        for lm_name in lm_names
    ]
    # these targets are (lm_name, ray)
    for other_cam_name, lm_name in rays:
        other_cam = get_camera(other_cam_name)
        targets.append((lm_name, (
            other_cam.xyz,
            other_cam.get_landmark_direction(lm_name)
        )))
    n_points = len(lm_names)
    (x_min, y_min), (x_max, y_max) = get_bounding_box(line)
    xys = [
        (x, y)
        for x in np.arange(x_min - radius, x_max + radius + step, step)
        for y in np.arange(y_min - radius, y_max + radius + step, step)
        if get_distance_to_line_segment((x, y), line) <= radius
    ]
    pitch_values = list(np.arange(*pitch_range))
    hfov_values = list(np.arange(*hfov_range))
    best_loss = float("inf")
    local_loss = []
    best_cam = None

    pool_args = [
        (cam, xy, z_limits, pitch_values, hfov_values, targets, n_points)
        for xy in xys
    ]
    with multiprocessing.Pool() as pool:
        for loss, deltas, cam in tqdm(
            pool.imap_unordered(_find_camera, pool_args),
            total=len(pool_args)
        ):
            local_loss.append((cam.xy, loss))
            if loss < best_loss:
                best_loss = loss
                best_cam = cam
                delta_string = "[" + ", ".join([f"{v:.6f}" for v in deltas]) + "]"
                print(f"{loss=:.6f}\ndeltas={delta_string}\n{cam}\n", flush=True)

    cam.set_xyz(best_cam.xyz).set_ypr(best_cam.ypr).set_fov(best_cam.fov).register()
    for other_cam_name, lm_name in sorted(rays, key=lambda kv: kv[1]):
        (x, y, z), a, b, d, _ = find_landmark(cam_name, other_cam_name, lm_name)
        print(f'    "{lm_name}": ({x:.3f}, {y:.3f}, {z:.3f}),  # {d=:.3f} via {cam_name} & {other_cam_name}')

    m = get_map(map_name).open(scale=map_scale, add_padding=True)
    for (x, y), loss in local_loss:
        if loss == float("inf"): continue
        log_loss = math.log10(loss)
        # 1 = green, 10 = yellow, 100 = red, ...
        rgb = get_rgb((120 - log_loss * 60) % 360)
        m.draw_rectangle(
            (x - step / 2, y - step / 2),
            (x + step / 2, y + step + 2),
            rgb, None, 0
        )
    m.draw_camera(cam_name, d=10000, _no_marker=True)
    other_cam_names = list(set(other_cam_name for other_cam_name, lm_name in rays))
    for other_cam_name in other_cam_names:
        m.draw_camera(other_cam_name, d=10000)
    for lm_name in lm_names:
        point_xy = get_point(cam.xyz, cam.get_landmark_direction(lm_name), 10000)[:2]
        color = get_color(lm_name)
        m.draw_line((cam.xy, point_xy), color, 1)
        if lm_name in md.landmarks:
            m.draw_landmark(lm_name)
        else:
            m.draw_camera(lm_name, d=10000)
    for other_cam_name, lm_name in rays:
        color = get_color(lm_name)
        for c in (cam, get_camera(other_cam_name)):
            point_xy = get_point(c.xyz, c.get_landmark_direction(lm_name), 10000)[:2]
            m.draw_line((c.xy, point_xy), color, 1)
    os.makedirs(os.path.dirname(basename), exist_ok=True)
    m.save(f"{basename} map.png", map_area)

    cam.render_all().save(f"{basename} camera.png")

    if projection_area:
        m = get_map(map_name)
        m.project_camera_parallel(cam_name, area=projection_area)
        m.save(f"{basename} projection.png", projection_area)

    return cam, best_loss


def _find_camera(args):
    """
    Camera search worker function
    """

    cam, xy, z_limits, pitch_values, hfov_values, targets, n_points = args
    cam.set_xyz((xy[0], xy[1], cam.z))
    n_targets = len(targets)
    best_loss = float("inf")
    best_values = None

    for pitch in pitch_values:
        cam.set_ypr((cam.yaw, pitch, cam.roll))
        for hfov in hfov_values:
            cam.set_fov((hfov, None))
            for p in range(n_points):
                cam.calibrate_yaw_and_z(*targets[p])  # lm_name, point
                if z_limits and not z_limits[0] <= cam.z <= z_limits[1]:
                    continue
                deltas = []
                loss = 0
                threshold = best_loss * n_targets
                for i, (lm_name, target) in enumerate(targets):
                    fn = intersect_ray_and_point if i < n_points else intersect_rays
                    cam_ray = (cam.xyz, cam.get_landmark_direction(lm_name))
                    angle = fn(cam_ray, target)[-1]
                    delta = angle * 60 # arcminutes
                    deltas.append(delta)
                    loss += delta ** 2
                    if loss >= threshold:
                        break
                loss /= n_targets
                if loss < best_loss:
                    best_loss = loss
                    best_deltas = deltas
                    best_values = cam.xyz, cam.ypr, cam.fov

    if best_values is None:
        raise RuntimeError("No camera found.")
    xyz, ypr, fov = best_values
    cam.set_xyz(xyz).set_ypr(ypr).set_fov(fov)
    return best_loss, best_deltas, cam


def find_four_seasons(
    line=((-800.0, -1280.0), (-800.0, -1280.0)),
    radius=10,
    step=1,
    ts_pitch_limits=(-0.3, -0.1),
    ms_pitch_limits=(-10.1, -9.7),
    size_ew_range=(30.0, 61.0, 1.0),
    aspect_ratio_limits=(1.25, 2.5),
    orientation_range=(335.0, 345.1, 0.1),
    map_name="rickrick",
    map_scale=5.0,
    map_area=(-1250, -1750, -250, -750),
    basename="four seasons"
):
    """
    Finds the Four Seasons landmark, given two known cameras.
    """

    ts_name = "Tennis Stadium (4K)"
    ts_cam = get_camera(ts_name)
    ms_name = "Metro (SE) (A) (4K)"
    ms_cam = get_camera(ms_name)

    # check that markup aligns with pitch
    for lm_name, anchor_name in (
        ("Four Seasons Hotel Miami (32NE)", "Four Seasons Hotel Miami (40NE)"),
        ("Four Seasons Hotel Miami (56NE)", "Four Seasons Hotel Miami (NE)")
    ):
        lm_x, lm_y = ts_cam.landmark_pixels[lm_name]
        lm_x_new = intersect_lines_2d(
            (ts_cam.landmark_pixels[anchor_name], ts_cam.get_vvp()),
            ((0, lm_y), (ts_cam.w, lm_y))
        )[0]
        lm_xy_string = f"{lm_x:.3f}, {lm_y:.3f}"
        lm_xy_new_string = f"{lm_x_new:.3f}, {lm_y:.3f}"
        if lm_xy_string != lm_xy_new_string:
            raise ValueError(
                f"In {ts_name}, {lm_name} is {lm_xy_string}, but should be {lm_xy_new_string}."
            )

    (x_min, y_min), (x_max, y_max) = get_bounding_box(line)
    xys = [
        (x, y)
        for x in np.arange(x_min - radius, x_max + radius + step, step)
        for y in np.arange(y_min - radius, y_max + radius + step, step)
        if get_distance_to_line_segment((x, y), line) <= radius
    ]

    best_loss = float("inf")
    local_loss = []
    best_values = None

    pool_args = [(
        x, y, ts_cam, ms_cam,
        ts_pitch_limits, ms_pitch_limits,
        size_ew_range, aspect_ratio_limits,
        orientation_range
    ) for x, y in xys]
    with multiprocessing.Pool() as pool:
        for loss, deltas, ts_cam, ms_cam, values in tqdm(
            pool.imap_unordered(_find_four_seasons, pool_args, chunksize=1),
            total=len(pool_args)
        ):
            if loss == float("inf"):
                continue
            fs40ne = values[0]
            local_loss.append((fs40ne[:2], loss))
            if loss < best_loss:
                best_loss = loss
                best_ts_cam = ts_cam
                best_ms_cam = ms_cam
                best_values = values
                delta_string = "[" + ", ".join([f"{v:.6f}" for v in deltas]) + "]"
                fs_string = "\n".join([
                    f"{name}=(" + ", ".join([f"{v:.3f}" for v in values[i]]) + ")"
                    for i, name in enumerate((
                        "fs40ne", "fs40nw", "fs40w", "fs40e",
                        "fs56ne", "fs56sw", "fs56se"
                    ))
                ])
                print(
                    f"{loss=:.6f}\ndeltas={delta_string}\n{ts_cam}\n{ms_cam}\n{fs_string}\n",
                    flush=True
                )

    ts_cam.set_xyz(best_ts_cam.xyz).set_ypr(best_ts_cam.ypr).set_fov(best_ts_cam.fov).register()
    ms_cam.set_xyz(best_ms_cam.xyz).set_ypr(best_ms_cam.ypr).set_fov(best_ms_cam.fov).register()

    # construct four seasons
    fs40ne, fs40nw, fs40w, fs40e, fs56ne, fs56sw, fs56se = best_values
    floor_height = (fs56ne[2] - fs40ne[2]) / 16
    dir_w = get_direction(fs40ne, fs40nw)
    fs40w = get_point(fs40e, dir_w, math.dist(fs40ne, fs40nw)) # FIXME: is this needed? 
    fs56nw = get_point(fs56ne, dir_w, math.dist(fs56se, fs56sw))
    fs57ne, hb8se, hb28se, hb58se, hb58ne = [
        intersect_ray_and_plane(
            (ts_cam.xyz, ts_cam.get_landmark_direction(f"Four Seasons Hotel Miami ({corner})")),
            (fs56ne, dir_w)
        )
        for corner in ("NE", "HB8SE", "HB28SE", "HB58SE", "HB58NE")
    ]
    fs57ne = (fs56ne[0], fs56ne[1], fs57ne[2])
    hb8se = (hb8se[0], hb8se[1], fs40ne[2] - 32 * floor_height)
    hb28se = (hb28se[0], hb28se[1], fs40ne[2] - 12 * floor_height)
    fs = FourSeasons(
        fs40ne=fs40ne,
        fs40nw=fs40nw,
        fs40w=fs40w,
        fs40e=fs40e,
        fs56ne=fs56ne,
        fs56nw=fs56nw,
        fs56sw=fs56sw,
        fs56se=fs56se,
        fs57ne=fs57ne,
        hb8se=hb8se,
        hb28se=hb28se,
        hb58se=hb58se,
        hb58ne=hb58ne
    )
    print(fs)
    print(fs._args())
    print(fs._landmarks())

    # render map
    m = get_map(map_name).open(scale=map_scale)
    for (x, y), loss in local_loss:
        if loss == float("inf"):
            rgb = (128, 128, 128)
        else:
            log_loss = math.log10(loss)
            # 1 = green, 10 = yellow, 100 = red, ...
            rgb = get_rgb((120 - log_loss * 60) % 360)
        m.draw_rectangle(
            (x - step / 2, y - step / 2),
            (x + step / 2, y + step + 2),
            rgb, None, 0
        )
    for cam, corner in (
        (ts_cam, "40NE"),
        (ts_cam, "40E"),
        (ts_cam, "56NE"),
        (ts_cam, "SW"),
        (ts_cam, "SE"),
        (ms_cam, "40NE"),
        (ms_cam, "40NW"),
        (ms_cam, "40W")
    ):
        target = get_point(
            cam.xyz,
            cam.get_landmark_direction(f"Four Seasons Hotel Miami ({corner})"),
            10000
        )
        m.draw_line((cam.xy, target[:2]), cam.color, 1)
    m.draw_camera(ts_name)
    m.draw_camera(ms_name)
    m.draw_object(fs)
    m.save(f"{basename} map.png", map_area, map_info_height=16)

    # render cameras
    for cam in (ts_cam, ms_cam):
        cam.open()
        cam.render_player()
        cam.render_vertical_lines()
        cam.render_distance_circles()
        cam.render_pixels()
        cam.render_object(fs)
        cam.render_camera_info()
        cam.save(f"{basename} camera {cam.name}.png")


def _find_four_seasons(args):
    """
    Four Seasons search worker function
    """

    (
        x, y, ts_cam, ms_cam,
        ts_pitch_limits, ms_pitch_limits,
        size_ew_range, aspect_ratio_limits,
        orientation_range
    ) = args

    best_loss = float("inf")
    best_deltas = None
    best_values = None

    lm_name = "Four Seasons Hotel Miami (40NE)"
    fs40ne = (x, y, 0)
    ts_cam.calibrate_yaw(lm_name, fs40ne)
    ms_cam.calibrate_yaw(lm_name, fs40ne)
    zs = [[], []]
    for i, (cam, pitch_limits) in enumerate((
        (ts_cam, ts_pitch_limits),
        (ms_cam, ms_pitch_limits)
    )):
        for pitch in pitch_limits:
            cam.set_ypr((cam.yaw, pitch, cam.roll))
            lm_dir = cam.get_landmark_direction(lm_name)
            point = intersect_rays(
                (fs40ne, (0, 0, 1)),
                (cam.xyz, lm_dir)
            )[1]
            zs[i].append(point[2])
    low = max(min(zs[0]), min(zs[1]))
    high = min(max(zs[0]), max(zs[1]))
    if low > high:
        return best_loss, best_deltas, ts_cam, ms_cam, best_values
    z_values = (low, (low + high) * 0.5, high)

    for z in z_values:

        fs40ne = (x, y, z)
        ts_cam.calibrate_yaw_and_pitch(lm_name, fs40ne)
        ms_cam.calibrate_yaw_and_pitch(lm_name, fs40ne)

        for size_ew in np.arange(*size_ew_range):
            for size_ns in np.arange(
                np.floor(size_ew / aspect_ratio_limits[1]),
                np.ceil(size_ew / aspect_ratio_limits[0]),
                size_ew_range[2]
            ):
                for orientation in np.arange(*orientation_range):

                    # construct remaining points
                    dir_w = get_direction_from_angles((orientation + 90) % 360)
                    dir_sw = get_direction_from_angles((orientation + 135) % 360)
                    dir_s = get_direction_from_angles((orientation + 180) % 360)
                    dir_se = get_direction_from_angles((orientation + 225) % 360)
                    fs40e = get_point(fs40ne, dir_s, size_ns)
                    fs40nw = get_point(fs40ne, dir_w, size_ew)
                    fs40w = get_point(fs40nw, dir_s, size_ns)
                    fs32ne = intersect_rays(
                        (fs40ne, (0, 0, -1)),
                        (ts_cam.xyz, ts_cam.get_landmark_direction("Four Seasons Hotel Miami (32NE)"))
                    )[1]
                    floor_height = (fs40ne[2] - fs32ne[2]) / 8
                    fs56ne_box = (fs40ne[0], fs40ne[1], fs40ne[2] + 16 * floor_height)
                    fs56nw_box = (fs40nw[0], fs40nw[1], fs40nw[2] + 16 * floor_height)
                    fs56ne = intersect_rays(
                        (fs56ne_box, dir_sw),
                        (ts_cam.xyz, ts_cam.get_landmark_direction("Four Seasons Hotel Miami (56NE)")),
                    )[1]
                    fs56se = intersect_rays(
                        (fs56ne, dir_s),
                        (ts_cam.xyz, ts_cam.get_landmark_direction("Four Seasons Hotel Miami (SE)")),
                    )[1]
                    fs56nw = get_point(fs56nw_box, dir_se, math.dist(fs56ne_box, fs56ne))
                    fs56sw = get_point(fs56nw, dir_s, math.dist(fs56ne, fs56se))

                    loss = 0
                    deltas = []
                    tests = [
                        (ts_cam, fs40ne, "Four Seasons Hotel Miami (40NE)"),
                        (ts_cam, fs40e, "Four Seasons Hotel Miami (40E)"),
                        (ts_cam, fs56ne, "Four Seasons Hotel Miami (56NE)"),
                        (ts_cam, fs56se, "Four Seasons Hotel Miami (SE)"),
                        (ts_cam, fs56sw, "Four Seasons Hotel Miami (SW)"),
                        (ms_cam, fs40ne, "Four Seasons Hotel Miami (40NE)"),
                        (ms_cam, fs40nw, "Four Seasons Hotel Miami (40NW)"),
                        (ms_cam, fs40w, "Four Seasons Hotel Miami (40W)"),
                    ]
                    for i, (cam, point, lm_name_) in enumerate(tests):
                        direction = cam.get_landmark_direction(lm_name_)
                        d = intersect_ray_and_point((cam.xyz, direction), point)[-1]
                        deltas.append(d)
                        loss += d ** 2
                    loss /= len(tests)

                    if loss < best_loss:
                        best_loss = loss
                        best_deltas = deltas
                        best_values = (
                            ts_cam.ypr, ms_cam.ypr,
                            fs40ne, fs40nw, fs40w, fs40e,
                            fs56ne, fs56sw, fs56se
                        )

    ts_ypr, ms_ypr = best_values[:2]
    ts_cam.set_ypr(ts_ypr)
    ms_cam.set_ypr(ms_ypr)
    return best_loss, best_deltas, ts_cam, ms_cam, best_values[2:]


def find_landmark(cam_name_a, cam_name_b, lm_name):
    """
    Finds a landmark, given two known cameras.
    Returns midpoint, closest point on ray a, closest point on ray b, distance, angular delta.
    """
    cam_a = get_camera(cam_name_a)
    cam_b = get_camera(cam_name_b)
    return intersect_rays(
        (cam_a.xyz, cam_a.get_landmark_direction(lm_name)),
        (cam_b.xyz, cam_b.get_landmark_direction(lm_name))
    )


### GEOMETRY ######################################################################################

def get_angle_delta(angle_a, angle_b):
    d = np.radians(angle_b - angle_a)
    return np.degrees(np.arctan2(np.sin(d), np.cos(d)))

def get_angles_from_direction(direction):
    x, y, z = np.asarray(direction, dtype=float)
    bearing = np.degrees(np.arctan2(-x, y)) % 360
    elevation = np.degrees(np.arctan2(z, np.hypot(x, y)))
    return bearing, elevation

def get_angular_delta(ray, point):
    # FIXME: unused?
    r_org, r_dir = ray
    v = get_direction(r_org, point)
    r_dir = np.asarray(r_dir) / np.linalg.norm(r_dir)
    cos_theta = np.clip(np.dot(r_dir, v), -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

def get_bearing(xy_a, xy_b):
    xa, ya = xy_a
    xb, yb = xy_b
    dx, dy = xb - xa, yb - ya
    angle = (np.degrees(np.arctan2(dy, dx)) - 90) % 360
    return float(angle)

def get_bounding_box(pixels):
    pixels = np.asarray(pixels)
    x_min, y_min = pixels.min(axis=0)
    x_max, y_max = pixels.max(axis=0)
    return (x_min, y_min), (x_max, y_max)

def get_direction(point_a, point_b):
    v = np.asarray(point_b) - np.asarray(point_a)
    norm = np.linalg.norm(v)
    if norm == 0:
        return np.zeros_like(v)
    return v / norm

def get_direction_from_angles(bearing, elevation=0.0):
    b_rad = np.radians(bearing)
    e_rad = np.radians(elevation)
    x = -np.sin(b_rad) * np.cos(e_rad)
    y =  np.cos(b_rad) * np.cos(e_rad)
    z =  np.sin(e_rad)
    return x, y, z

def get_distance(point_a, point_b):
    return np.linalg.norm(np.array(point_a) - np.array(point_b))

def get_distance_to_line_segment(point, line):
    point = np.asarray(point)
    a = np.asarray(line[0])
    b = np.asarray(line[1])
    ab = b - a
    ap = point - a
    dot_ab_ab = np.dot(ab, ab)
    t = np.dot(ap, ab) / dot_ab_ab if dot_ab_ab != 0.0 else 0.0
    t = np.clip(t, 0.0, 1.0)
    closest = a + t * ab
    return np.linalg.norm(point - closest)

def get_hfov(vfov, size):
    ratio = size[0] / size[1]
    return np.degrees(2 * np.arctan(np.tan(np.radians(vfov) / 2) * ratio))

def get_vfov(hfov, size):
    ratio = size[0] / size[1]
    return np.degrees(2 * np.arctan(np.tan(np.radians(hfov) / 2) / ratio))

def get_pixel(world_xyz, cam_xyz, q, fov, size):
    hfov, vfov = np.radians(fov[0]), np.radians(fov[1])
    w, h = size
    rot = get_rotation(tuple(q))
    delta = np.array(world_xyz) - np.array(cam_xyz)
    cam_dir = rot.inv().apply(delta)
    if cam_dir[1] <= 0:
        return None  # behind the camera
    ndc_x = cam_dir[0] / cam_dir[1] / np.tan(hfov / 2)
    ndc_y = cam_dir[2] / cam_dir[1] / np.tan(vfov / 2)
    px =      (ndc_x + 1) * 0.5  * w - 0.5
    py = (1 - (ndc_y + 1) * 0.5) * h - 0.5
    if not (np.isfinite(px) and np.isfinite(py)):
        return None  # invalid projection
    return np.array([px, py])

def get_pixel_direction(pixel, q, fov, size):
    x, y = pixel
    hfov, vfov = np.radians(fov[0]), np.radians(fov[1])
    w, h = size
    ndc_x = 2 * ((x + 0.5) / w) - 1
    ndc_y = 2 * ((y + 0.5) / h) - 1
    cam_x =  ndc_x * np.tan(hfov / 2)
    cam_z = -ndc_y * np.tan(vfov / 2)
    cam_dir = np.array([cam_x, 1.0, cam_z])
    rot = get_rotation(tuple(q))
    world_dir = rot.apply(cam_dir)
    return world_dir / np.linalg.norm(world_dir)

def get_point(point, direction, distance):
    return np.asarray(point) + distance * np.asarray(direction)

def get_q(ypr):
    return R.from_euler("ZXY", ypr, degrees=True).as_quat()

@lru_cache(maxsize=256)
def get_rotation(q):
    return R.from_quat(q)

def get_ypr(q):
    yaw, pitch, roll = R.from_quat(q).as_euler("ZXY", degrees=True)
    return (yaw % 360, pitch, roll)

def intersect_lines_2d(line_a, line_b):
    a0, a1 = np.asarray(line_a)
    b0, b1 = np.asarray(line_b)
    dir_a = a1 - a0
    dir_b = b1 - b0
    denom = np.cross(dir_a, dir_b)
    if np.isclose(denom, 0):
        return None  # parallel
    t = np.cross((b0 - a0), dir_b) / denom
    inter = a0 + t * dir_a
    return float(inter[0]), float(inter[1])

def intersect_ray_and_point(ray, point):
    r_org, r_dir = ray
    r_org = np.asarray(r_org)
    r_dir = np.asarray(r_dir) / np.linalg.norm(r_dir)
    point = np.asarray(point)
    diff = point - r_org
    proj_length = np.dot(diff, r_dir)
    closest_point = r_org + proj_length * r_dir
    distance = np.linalg.norm(point - closest_point)
    p_dir = get_direction(r_org, point)
    cos_theta = np.clip(np.dot(r_dir, p_dir), -1.0, 1.0)
    angle = np.degrees(np.arccos(cos_theta))
    return closest_point, distance, angle

def intersect_ray_and_plane(ray, plane, eps=1e-8):
    r_org, r_dir = ray
    p_org, p_normal = plane
    r_org = np.asarray(r_org)
    r_dir = np.asarray(r_dir)
    p_org = np.asarray(p_org)
    p_normal = np.asarray(p_normal)
    denom = np.dot(p_normal, r_dir)
    if abs(denom) < eps:
        return None  # parallel
    distance = np.dot(p_normal, p_org - r_org) / denom
    point = r_org + distance * r_dir
    return point

def intersect_rays(ray_a, ray_b, eps=1e-8):
    (org_a, dir_a), (org_b, dir_b) = ray_a, ray_b
    org_a, dir_a = np.asarray(org_a, dtype=float), np.asarray(dir_a, dtype=float)
    org_b, dir_b = np.asarray(org_b, dtype=float), np.asarray(dir_b, dtype=float)
    dir_a, dir_b = dir_a / np.linalg.norm(dir_a), dir_b / np.linalg.norm(dir_b)
    dot_ab = np.dot(dir_a, dir_b)
    diff = org_b - org_a
    dot_ap = np.dot(dir_a, diff)
    dot_bp = np.dot(dir_b, diff)
    denom = 1 - dot_ab ** 2
    if abs(denom) < eps:
        # parallel
        if np.linalg.norm(np.cross(dir_a, diff)) < eps:
            # colinear, return midpoint of origins
            mid = org_a + 0.5 * np.dot(diff, dir_a) * dir_a
            return mid, mid, mid, 0.0, 0.0
        t_a = 0.0
        t_b = dot_bp
    else:
        t_a = (dot_ap - dot_ab * dot_bp) / denom
        t_b = (dot_ab * dot_ap - dot_bp) / denom
    point_a = org_a + t_a * dir_a
    point_b = org_b + t_b * dir_b
    midpoint = 0.5 * (point_a + point_b)
    distance = np.linalg.norm(point_a - point_b)
    miss_a = point_b - org_a
    miss_b = point_a - org_b
    miss_a /= np.linalg.norm(miss_a)
    miss_b /= np.linalg.norm(miss_b)
    delta_a = np.degrees(np.arccos(np.clip(np.dot(miss_a, dir_a), -1.0, 1.0)))
    delta_b = np.degrees(np.arccos(np.clip(np.dot(miss_b, dir_b), -1.0, 1.0)))
    angle = 0.5 * (delta_a + delta_b)
    return midpoint, point_a, point_b, distance, angle

def _q_mul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array([
        aw*bw - ax*bx - ay*by - az*bz,
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw
    ])


### UTILITIES #####################################################################################

def draw_box(text, height, color, text_color):
    height = int(round(height))
    font = ImageFont.truetype(f"{DIRNAME}/fonts/Menlo-Regular.ttf", height * 0.75)
    w, h = get_textsize(text, font)
    margin = (height - h) / 2
    width = int(w + 2 * margin)
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)
    draw.text((margin, margin // 2), text, fill=text_color, font=font)
    return image

def get_color(name):
    name = normalize_name(name)
    sha1 = hashlib.sha1(name.encode("utf-8")).hexdigest()[-6:]
    return tuple(int(int(sha1[i * 2:i * 2 + 2], 16) * 0.75) for i in range(3))

def get_letter(name):
    if name.startswith("Pin "):
        return name.split(" ")[-1][0]
    if re.search("\\([A-Z0-9]+\\)$", name):
        return name.split("(")[-1][0]
    return re.sub("^The ", "", name)[0]

def get_rgb(hue, s=1.0, v=1.0):
    return tuple([int(v * 255) for v in colorsys.hsv_to_rgb(hue / 360, s, v)])

def get_textsize(text, font):
    image = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(image)
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l, b - t

def normalize_name(name):
    for _ in range(3):
        name = re.sub(" \\([A-Z0-9\\?]+\\)$", "", name)
        if not name.endswith(")"):
            break
    return name

def subsample(image_np, xy):
    h, w = image_np.shape[:2]
    x, y = xy
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1
    pixels = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    inv_distances = [2 ** 0.5 - math.dist((x, y), pxy) for pxy in pixels]
    inv_distances = [d / sum(inv_distances) for d in inv_distances]  # normalize
    rgbs = [
        image_np[py][px] if px < w and py < h else (0, 0, 0)
        for px, py in pixels
    ]
    return tuple([
        int(round(sum(rgb[c] * inv_distances[i] for i, rgb in enumerate(rgbs))))
        for c in range(3)
    ])


FS = FourSeasons()
SSB = SunshineSkywayBridge()
