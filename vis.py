import os
import time
import numpy as np

import open3d as o3d
from functools import partial

PATH = './results'

ZOOM = 1

COLORS = { 
    "person": [0,255,0],
    "chair": [0,191,255],
    "mouse": [80.0,127.0,255.0],
    "keyboard": [99,49,222],
    "phone": [191,226,191],
    "cup": [208,224,64],
    "laptop": [237,149,100],
    "tv": [255,204,204]
}


## Utility functions

def denormalize(x):
	return x*255

def normalize(x):
	return x/255

def is_close(a, b):
	tmp = np.isclose(a, b, atol=1)  # 1
	if False not in tmp:
		return True
	else:
		return False

# # Dummy function
# def filter(vis):
# 	view_ctl = vis.get_view_control()
# 	for i in range(0, 50000):
# 		#pcd.colors[i] = [0,0,0]
# 		norm_pcd.colors[i] = [0,0,0]

# 	vis.update_geometry(norm_pcd)
# 	# vis.remove_geometry(pcd)
# 	# vis.add_geometry(norm_pcd)
# 	vis.update_renderer()
# 	vis.poll_events()
# 	vis.run()

# Filter function
def filter(vis, cls):

	if cls == '1':
		for i, color in enumerate(pcd.colors):
			color = color*255
			res = is_close(list(color), COLORS["mouse"][::-1])
			if res == True:
				pcd.colors[i] = [1,1,1]

	if cls == '2':
		for i, color in enumerate(pcd.colors):
			color = color*255
			res = is_close(list(color), COLORS["keyboard"][::-1])
			if res == True:
				pcd.colors[i] = [1,1,1]

	print("filtering done...")
	vis.update_geometry(pcd)
	vis.poll_events()
	vis.run()
	vis.destroy_window()


# Read point clouds
# #pcd = o3d.io.read_point_cloud(os.path.join(PATH, 'points.ply'))
pcd = o3d.io.read_point_cloud(os.path.join(PATH, 'output.ply'))
poses = o3d.io.read_line_set(os.path.join(PATH, 'camera.ply'))

vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()

vis.add_geometry(pcd)
vis.add_geometry(poses)
vis.poll_events()
vis.update_renderer()


def zoom_in(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM -= .03
    view_ctl.set_zoom(ZOOM)
    return False

def zoom_out(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM += .03
    view_ctl.set_zoom(ZOOM)
    return False

def rotate_view_left(vis):
    ctr = vis.get_view_control()
    ctr.rotate(5.0, 0.0)
    return False

def rotate_view_right(vis):
    ctr = vis.get_view_control()
    ctr.rotate(- 5.0, 0.0)
    return False

def rotate_view_up(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, -5.0)
    return False

def rotate_view_down(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, 5.0)
    return False


view_ctl = vis.get_view_control()
view_ctl.set_up((0, -1, 0))
view_ctl.set_zoom(.5)

vis.register_key_callback(ord("W"), zoom_in)
vis.register_key_callback(ord("S"), zoom_out)

vis.register_key_callback(ord("A"), rotate_view_left)
vis.register_key_callback(ord("D"), rotate_view_right)

vis.register_key_callback(ord("Q"), rotate_view_up)
vis.register_key_callback(ord("E"), rotate_view_down)

# #vis.register_key_callback(ord("O"), filter)

# # vis.register_key_callback(ord("O"), partial(filter, denorm_pcd=denorm_pcd, norm_pcd=norm_pcd, cls='1'))

vis.register_key_callback(ord("6"), partial(filter, cls='1'))
vis.register_key_callback(ord("7"), partial(filter, cls='2'))

vis.run()
vis.destroy_window()