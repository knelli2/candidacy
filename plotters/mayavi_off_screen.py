import numpy as np
from staggered import *
from mayavi import mlab
import os

image_dir = "/home/knelli/Documents/research/candidacy/images"

# True for everything
squash = 0.5
image_size = (1000, 1000)
focalpoint = [1, 1, 1.25]
mlab.view()


def set_scene():
    mlab.view(azimuth=-135, elevation=65, distance=10, focalpoint=focalpoint)


def save(image_name: str):
    if not image_name.endswith(".png"):
        image_name += ".png"
    mlab.options.offscreen = True
    mlab.savefig(os.path.join(image_dir, image_name), size=image_size)


def save_close(image_name: str):
    save(image_name=image_name)
    mlab.close()


def save_clear(image_name: str):
    save(image_name=image_name)
    mlab.clf()


def test_off_screen_render():
    fig = mlab.figure(bgcolor=transparent)

    x = np.array([0])
    y = np.array([0])
    z_bottom = np.array([0])
    z_top = np.array([1])

    bar = mlab.barchart(x, y, z_bottom, z_top, color=green, figure=fig)

    save("blah")

    mlab.close()
    os.remove(os.path.join(image_dir, "blah.png"))


def sync_async_frame_1_and_2(name: str, height: int, color: str):
    filename = f"{name}_{height+1}"
    print(f"Rendering {filename}...")

    fig = mlab.figure(bgcolor=white)

    x, y, z_bottom, z_top = all_flat_top_from_bottom(
        level=height, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(f"{name}_{height+1}")


def sync_async_frame_1(name: str):
    sync_async_frame_1_and_2(name, 0, white)


def sync_async_frame_2(name: str):
    sync_async_frame_1_and_2(name, 1, green)


# For some reason the first image doesn't render properly so we put a dummy
# image here instead
test_off_screen_render()
sync_async_frame_1("async")
sync_async_frame_1("sync")
sync_async_frame_2("async")
sync_async_frame_2("sync")
