import numpy as np
import numpy.testing as npt
from PIL import ImageColor

# Colorblind friendly colors as hex and rgb
colors_hex = [
    "55f068",
    "4c9cf0",
    "c44e52",
    "8172b3",
    "937860",
    "da8bc3",
    "8c8c8c",
    "ccb974",
    "64b5cd",
]
colors_rgb = [
    tuple(np.array(ImageColor.getcolor(f"#{c}", "RGB")) / 256)
    for c in colors_hex
]

# Useful individual colors
white = (1, 1, 1)
black = (0, 0, 0)
green = colors_rgb[0]
blue = colors_rgb[1]
red = colors_rgb[2]
purple = colors_rgb[3]
brown = colors_rgb[4]
pink = colors_rgb[5]
silver = colors_rgb[6]
gold = colors_rgb[7]
cyan = colors_rgb[8]

# Global defaults. Note make sure to copy all_x and all_y
transparent = None
bottom = 0
global_squash_factor = 1.0
all_x = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]).ravel()
all_y = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]]).ravel()


def set_line_width(bar):
    bar.actor.property.edge_visibility = True
    bar.actor.property.line_width = 6.0


def all_flat_top_from_bottom(level: int, squash_factor=global_squash_factor):
    z_bottom = squash_factor * np.full_like(all_x, bottom)
    z_top = squash_factor * np.full_like(all_x, level)

    return all_x, all_y, z_bottom, z_top


def staggered_height_from_bottom(
    level: int, squash_factor=global_squash_factor
):
    assert level > bottom, f"Level {level} must be greater than bottom {bottom}"

    z_bottom = np.full_like(all_x, bottom)
    z_top = all_x + all_y + 1

    for i, z in enumerate(z_top):
        if z > level:
            z_top[i] = level

    return (
        all_x.copy(),
        all_y.copy(),
        squash_factor * z_bottom,
        squash_factor * z_top,
    )


def filter_negative_one(input_list):
    return np.array([ll for ll in input_list if ll != -1])


def staggered_height_from(
    new_bottom: int, level: int, squash_factor=global_squash_factor
):
    assert (
        level > new_bottom
    ), f"Level {level} must be greater than new bottom {new_bottom}"

    if new_bottom == bottom:
        return staggered_height_from_bottom(level, squash_factor)

    x, y, _, short_z_top = staggered_height_from_bottom(new_bottom, 1.0)
    x, y, _, tall_z_top = staggered_height_from_bottom(level, 1.0)

    z_top = tall_z_top

    for i, (z_short, z_tall) in enumerate(zip(short_z_top, tall_z_top)):
        if z_short == z_tall:
            x[i] = -1
            y[i] = -1
            z_top[i] = -1

    x = filter_negative_one(x)
    y = filter_negative_one(y)
    z_top = filter_negative_one(z_top)

    z_bottom = np.full_like(x, new_bottom)

    return x, y, squash_factor * z_bottom, squash_factor * z_top


def check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level):
    npt.assert_array_equal(x0, x1, err_msg=f"x not equal, level={level}")
    npt.assert_array_equal(y0, y1, err_msg=f"y not equal, level={level}")
    npt.assert_array_equal(
        z_bottom0, z_bottom1, err_msg=f"z_bottom not equal, level={level}"
    )
    npt.assert_array_equal(
        z_top0, z_top1, err_msg=f"z_top not equal, level={level}"
    )


def test_staggered():
    levels = np.arange(1, 6)
    squashes = [0.5, 1.0]

    for level in levels:
        for squash in squashes:
            x0, y0, z_bottom0, z_top0 = staggered_height_from_bottom(
                level, squash
            )
            x1, y1, z_bottom1, z_top1 = staggered_height_from(
                bottom, level, squash
            )

            check_equal(
                x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level
            )

    new_bottom = 1
    level = 2
    squash = 1.0
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    x1 = np.array([0, 0, 1, 1, 1, 2, 2, 2])
    y1 = np.array([1, 2, 0, 1, 2, 0, 1, 2])
    z_bottom1 = np.full_like(x1, new_bottom)
    z_top1 = np.array([2, 2, 2, 2, 2, 2, 2, 2])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    level = 3
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    z_top1 = np.array([2, 3, 2, 3, 3, 3, 3, 3])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    level = 5
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    z_top1 = np.array([2, 3, 2, 3, 4, 3, 4, 5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    new_bottom = 2
    level = 3
    squash = 0.5
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    x1 = np.array([0, 1, 1, 2, 2, 2])
    y1 = np.array([2, 1, 2, 0, 1, 2])
    z_bottom1 = np.full_like(x1, squash * new_bottom)
    z_top1 = np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    level = 5
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    z_top1 = np.array([1.5, 1.5, 2, 1.5, 2, 2.5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    new_bottom = 4
    level = 5
    x0, y0, z_bottom0, z_top0 = staggered_height_from(new_bottom, level, squash)
    x1 = np.array([2])
    y1 = np.array([2])
    z_bottom1 = np.full_like(x1, squash * new_bottom)
    z_top1 = np.array([2.5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)


def manhattan_distance_comparison(
    distance: int, func, level: int, squash_factor=global_squash_factor
):
    x, y, z_bottom, z_top = staggered_height_from_bottom(level, squash_factor)

    for i in range(3):
        for j in range(3):
            md = i + j
            index = i * 3 + j
            if not func(md, distance):
                x[index] = -1
                y[index] = -1
                z_bottom[index] = -1
                z_top[index] = -1

    x = filter_negative_one(x)
    y = filter_negative_one(y)
    z_bottom = filter_negative_one(z_bottom)
    z_top = filter_negative_one(z_top)

    return x, y, z_bottom, z_top


def manhattan_distance_less(
    distance: int, level: int, squash_factor=global_squash_factor
):
    def func(manhattan_distance, distance):
        return manhattan_distance < distance

    return manhattan_distance_comparison(distance, func, level, squash_factor)


def manhattan_distance_greater(
    distance: int, level: int, squash_factor=global_squash_factor
):
    def func(manhattan_distance, distance):
        return manhattan_distance > distance

    return manhattan_distance_comparison(distance, func, level, squash_factor)


def manhattan_distance_less_equal(
    distance: int, level: int, squash_factor=global_squash_factor
):
    def func(manhattan_distance, distance):
        return manhattan_distance <= distance

    return manhattan_distance_comparison(distance, func, level, squash_factor)


def manhattan_distance_greater_equal(
    distance: int, level: int, squash_factor=global_squash_factor
):
    def func(manhattan_distance, distance):
        return manhattan_distance >= distance

    return manhattan_distance_comparison(distance, func, level, squash_factor)


def test_manhattan():
    distance = 2
    level = 5
    squash = 1.0
    x0, y0, z_bottom0, z_top0 = manhattan_distance_less(distance, level, squash)
    x1 = np.array([0, 0, 1])
    y1 = np.array([0, 1, 0])
    z_bottom1 = np.full_like(x1, bottom)
    z_top1 = np.array([1, 2, 2])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    x0, y0, z_bottom0, z_top0 = manhattan_distance_less_equal(
        distance, level, squash
    )
    x1 = np.array([0, 0, 0, 1, 1, 2])
    y1 = np.array([0, 1, 2, 0, 1, 0])
    z_bottom1 = np.full_like(x1, bottom)
    z_top1 = np.array([1, 2, 3, 2, 3, 3])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    x0, y0, z_bottom0, z_top0 = manhattan_distance_greater(
        distance, level, squash
    )
    x1 = np.array([1, 2, 2])
    y1 = np.array([2, 1, 2])
    z_bottom1 = np.full_like(x1, bottom)
    z_top1 = np.array([4, 4, 5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)

    x0, y0, z_bottom0, z_top0 = manhattan_distance_greater_equal(
        distance, level, squash
    )
    x1 = np.array([0, 1, 1, 2, 2, 2])
    y1 = np.array([2, 1, 2, 0, 1, 2])
    z_bottom1 = np.full_like(x1, bottom)
    z_top1 = np.array([3, 3, 4, 3, 4, 5])

    check_equal(x0, y0, z_bottom0, z_top0, x1, y1, z_bottom1, z_top1, level)
