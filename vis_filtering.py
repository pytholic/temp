import os
import time
import numpy as np

import open3d as o3d

from functools import partial
from collections import defaultdict


# Define paths and variables

PATH = "./results"
ZOOM = 1
COLORS = {
    "person": [0, 255, 0],
    "chair": [0, 191, 255],
    "mouse": [80.0, 127.0, 255.0],
    "keyboard": [99, 49, 222],
    "phone": [191, 226, 191],
    "cup": [208, 224, 64],
    "laptop": [237, 149, 100],
    "tv": [255, 204, 204],
    "car": [255, 0, 0],
    "airplane": [0, 0, 255],
}


# Utility functions


def denormalize(x):
    """
    Function to denormalize the pixel values.
    """
    return x * 255


def normalize(x):
    """
    Function to normalize pixel values.
    """
    return x / 255


def is_close(a, b):
    """
    Function to check if pixel values are approximately same.
    """
    tmp = np.isclose(a, b, atol=5)  # 1
    if False not in tmp:
        return True
    else:
        return False


def get_indices(pcd, category):
    """
    Function to collect indices of a category from point cloud for filtering.
    """
    indices = []
    colors_original = {}
    for i, color in enumerate(pcd.colors):
        color = color * 255  # denormalize
        res = is_close(list(color), COLORS[category][::-1])
        if res == False:
            indices.append(i)
            colors_original[i] = color / 255  # normalize

    return indices, colors_original


def filter(vis, cls):
    """
    Function to filter the desired objects.
    """
    global cnt_dict
    cnt_dict[f"{cls}"] += 1

    # Set mask color if count is odd
    if cnt_dict[f"{cls}"] % 2 != 0:
        for i in idx_dict[f"{cls}"][0]:
            pcd.colors[i] = [0.9, 0.9, 0.9]  # light gray color
        print(f"{cls} filtering done...")

    # Set default color if count is even
    else:
        for i in idx_dict[f"{cls}"][0]:
            pcd.colors[i] = idx_dict[f"{cls}"][1][i]
        print(f"{cls} filtering removed...")

    vis.update_geometry(pcd)


def show_original(vis):
    """
    Function to reset and show original point cloud.
    """

    global cnt_dict

    for v in idx_dict.values():
        for i in v[0]:
            pcd.colors[i] = v[1][i]

    cnt_dict = {key: 0 for key in cnt_dict}  # set counts to 0

    print("Showing original...")
    vis.update_geometry(pcd)


def zoom_in(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM -= 0.03
    view_ctl.set_zoom(ZOOM)
    return False


def zoom_out(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM += 0.03
    view_ctl.set_zoom(ZOOM)
    return False


def rotate_view_left(vis):
    ctr = vis.get_view_control()
    ctr.rotate(5.0, 0.0)
    return False


def rotate_view_right(vis):
    ctr = vis.get_view_control()
    ctr.rotate(-5.0, 0.0)
    return False


def rotate_view_up(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, -5.0)
    return False


def rotate_view_down(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, 5.0)
    return False


# Read point clouds
pcd = o3d.io.read_point_cloud(os.path.join(PATH, "output.ply"))
poses = o3d.io.read_line_set(os.path.join(PATH, "camera.ply"))


# Create counter and indices dict
cnt_dict = defaultdict()  # defaultdict for easy increment
idx_dict = dict()  # save background indices for each class
for k, v in COLORS.items():
    cnt_dict[k] = 0
    idx_dict[k] = get_indices(pcd, k)


# Visualization
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()


view_ctl = vis.get_view_control()
view_ctl.set_up((0, -1, 0))
view_ctl.set_zoom(0.5)

vis.register_key_callback(ord("W"), zoom_in)
vis.register_key_callback(ord("S"), zoom_out)

vis.register_key_callback(ord("A"), rotate_view_left)
vis.register_key_callback(ord("D"), rotate_view_right)

vis.register_key_callback(ord("Q"), rotate_view_up)
vis.register_key_callback(ord("E"), rotate_view_down)

for i, (k, v) in enumerate(COLORS.items()):
    vis.register_key_callback(ord(str(i)), partial(filter, cls=k))

vis.register_key_callback(ord("`"), show_original)

vis.add_geometry(pcd)
vis.add_geometry(poses)
vis.poll_events()
vis.update_renderer()

vis.run()
vis.destroy_window()
