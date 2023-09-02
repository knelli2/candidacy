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


def start(name: str, frame: int):
    filename = f"{name}_{frame:02}"
    print(f"Rendering {filename} ... ", end="")

    fig = mlab.figure(bgcolor=white)

    return fig, filename


def save(image_name: str, do_print=True):
    if not image_name.endswith(".png"):
        image_name += ".png"
    mlab.options.offscreen = True
    mlab.savefig(os.path.join(image_dir, image_name), size=image_size)
    if do_print:
        print("done")


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

    save("blah", do_print=False)

    mlab.close()
    os.remove(os.path.join(image_dir, "blah.png"))


def sync_async_frame_flat_top(name: str, frame: int, height: int, color: str):
    fig, filename = start(name, frame)

    x, y, z_bottom, z_top = all_flat_top_from_bottom(
        level=height, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(filename)


def sync_async_frame_1(name: str):
    sync_async_frame_flat_top(name, 1, 0, white)


def sync_async_frame_2(name: str):
    sync_async_frame_flat_top(name, 2, 1, green)


def sync_async_split_colors(
    name: str, frame: int, distance: int, level: int, red_green_same_level: bool
):
    fig, filename = start(name, frame)

    x, y, z_bottom, z_top = manhattan_distance_less_equal(
        distance, level, squash_factor=squash
    )
    bar = mlab.barchart(x, y, z_bottom, z_top, color=red, figure=fig)
    set_line_width(bar)
    second_level = level if red_green_same_level else level + 1
    x, y, z_bottom, z_top = manhattan_distance_greater(
        distance, second_level, squash_factor=squash
    )
    bar = mlab.barchart(x, y, z_bottom, z_top, color=green, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(filename)


def sync_async_frame_3(name: str):
    sync_async_split_colors(
        name=name, frame=3, distance=0, level=1, red_green_same_level=True
    )


def sync_frame_4():
    sync_async_frame_flat_top("sync", 4, 1, red)


def async_frame_4():
    sync_async_split_colors(
        name="async", frame=4, distance=0, level=1, red_green_same_level=False
    )


def async_frame_5():
    sync_async_split_colors(
        name="async", frame=5, distance=1, level=2, red_green_same_level=True
    )


def async_frame_6():
    sync_async_split_colors(
        name="async", frame=6, distance=1, level=2, red_green_same_level=False
    )


def async_frame_7():
    sync_async_split_colors(
        name="async", frame=7, distance=2, level=3, red_green_same_level=True
    )


def async_frame_8():
    sync_async_split_colors(
        name="async", frame=8, distance=2, level=3, red_green_same_level=False
    )


def async_frame_9():
    sync_async_split_colors(
        name="async", frame=9, distance=3, level=4, red_green_same_level=True
    )


def async_frame_10():
    sync_async_split_colors(
        name="async", frame=10, distance=3, level=4, red_green_same_level=False
    )


def async_frame_11():
    fig, filename = start("async", 11)

    x, y, z_bottom, z_top = staggered_height_from_bottom(level=5, squash_factor=squash)

    bar = mlab.barchart(x, y, z_bottom, z_top, color=red, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(filename)


# For some reason the first image doesn't render properly so we put a dummy
# image here instead
test_off_screen_render()

# Async
sync_async_frame_1("async")
sync_async_frame_2("async")
sync_async_frame_3("async")
async_frame_4()
async_frame_5()
async_frame_6()
async_frame_7()
async_frame_8()
async_frame_9()
async_frame_10()
async_frame_11()

# Sync
sync_async_frame_1("sync")
sync_async_frame_2("sync")
sync_async_frame_3("sync")
sync_frame_4()
