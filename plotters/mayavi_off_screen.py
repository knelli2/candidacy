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


def save(image_name: str, do_print=True, size=image_size):
    if not image_name.endswith(".png"):
        image_name += ".png"
    mlab.options.offscreen = True
    mlab.savefig(os.path.join(image_dir, image_name), size=size)
    if do_print:
        print("done")


def save_close(image_name: str, size=image_size):
    save(image_name=image_name, size=size)
    mlab.close()


def save_clear(image_name: str, size=image_size):
    save(image_name=image_name, size=size)
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


def plot_flat_top(name: str, frame: int, height: int, color: tuple):
    fig, filename = start(name, frame)

    x, y, z_bottom, z_top = all_flat_top_from_bottom(
        level=height, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(filename)


def sync_async_frame_1(name: str):
    plot_flat_top(name, 1, 0, white)


def sync_async_frame_2(name: str):
    plot_flat_top(name, 2, 1, green)


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
    plot_flat_top("sync", 4, 1, red)


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


def plot_staggered(
    name: str, frame: int, level: int, color: tuple, size: tuple = image_size
):
    fig, filename = start(name, frame)

    x, y, z_bottom, z_top = staggered_height_from_bottom(
        level=level, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)

    set_scene()

    save_clear(filename, size=size)


def async_frame_11():
    plot_staggered(name="async", frame=11, level=5, color=red)


global_state_size = (1200, 1000)


def plot_global_state_bar_no_save(fig, height: int, color: tuple):
    x = np.array([-1.25])
    y = np.array([1.0])
    z_bottom = np.array([0.0])
    z_top = squash * np.array([height])
    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)


def plot_staggered_with_global_state(
    frame: int,
    level: int,
    global_state_height: int,
    global_state_color: tuple,
):
    fig, filename = start("global_state", frame)

    x, y, z_bottom, z_top = staggered_height_from_bottom(
        level=level, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=green, figure=fig)
    set_line_width(bar)

    plot_global_state_bar_no_save(
        fig, height=global_state_height, color=global_state_color
    )

    set_scene()

    save_clear(filename, size=global_state_size)


def plot_flat_top_with_global_state(
    frame: int,
    height: int,
    color: tuple,
    global_state_height: int,
    global_state_color: tuple,
):
    fig, filename = start("global_state", frame)

    x, y, z_bottom, z_top = all_flat_top_from_bottom(
        level=height, squash_factor=squash
    )

    bar = mlab.barchart(x, y, z_bottom, z_top, color=color, figure=fig)
    set_line_width(bar)

    plot_global_state_bar_no_save(
        fig, height=global_state_height, color=global_state_color
    )

    set_scene()

    save_clear(filename, size=global_state_size)


def global_state_frame_1():
    plot_flat_top_with_global_state(
        frame=1,
        height=2,
        color=green,
        global_state_height=3,
        global_state_color=purple,
    )


def global_state_frame_2():
    plot_flat_top_with_global_state(
        frame=2,
        height=3,
        color=green,
        global_state_height=3,
        global_state_color=purple,
    )


def global_state_frame_3():
    plot_flat_top_with_global_state(
        frame=3,
        height=3,
        color=red,
        global_state_height=3,
        global_state_color=purple,
    )


def global_state_frame_4():
    plot_flat_top_with_global_state(
        frame=4,
        height=3,
        color=green,
        global_state_height=6,
        global_state_color=blue,
    )


def global_state_frame_5():
    plot_flat_top_with_global_state(
        frame=5,
        height=4,
        color=green,
        global_state_height=6,
        global_state_color=blue,
    )


def global_state_frame_6():
    plot_staggered_with_global_state(
        frame=6, level=5, global_state_height=3, global_state_color=purple
    )


def global_state_frame_7():
    fig, filename = start("global_state", 7)

    x, y, z_bottom, z_top = manhattan_distance_less_equal(
        distance=1, level=3, squash_factor=squash
    )
    bar = mlab.barchart(x, y, z_bottom, z_top, color=green, figure=fig)
    set_line_width(bar)
    x, y, z_bottom, z_top = manhattan_distance_greater(
        distance=1, level=3, squash_factor=squash
    )
    bar = mlab.barchart(x, y, z_bottom, z_top, color=red, figure=fig)
    set_line_width(bar)

    plot_global_state_bar_no_save(fig, height=3, color=purple)

    set_scene()

    save_clear(filename, size=global_state_size)


def global_state_frame_8():
    plot_staggered_with_global_state(
        frame=8, level=3, global_state_height=6, global_state_color=blue
    )


def global_state_frame_9():
    plot_staggered_with_global_state(
        frame=9, level=4, global_state_height=6, global_state_color=blue
    )


# For some reason the first image doesn't render properly so we put a dummy
# image here instead
test_off_screen_render()

# Global state
global_state_frame_1()
global_state_frame_2()
global_state_frame_3()
global_state_frame_4()
global_state_frame_5()
global_state_frame_6()
global_state_frame_7()
global_state_frame_8()
global_state_frame_9()

exit()

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
