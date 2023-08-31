import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt
from PIL import ImageColor

colors_hex = [
    "4c9cf0",
    "55f068",
    "c44e52",
    "8172b3",
    "937860",
    "da8bc3",
    "8c8c8c",
    "ccb974",
    "64b5cd",
]
colors_rgb = [
    tuple(np.array(ImageColor.getcolor(f"#{c}", "RGB")) / 256) for c in colors_hex
]
white = (1, 1, 1)
black = (0, 0, 0)
transparent = None
c0 = colors_rgb[0]
c1 = colors_rgb[1]

fig = mlab.figure(bgcolor=transparent, size=(500,500))
# fig = mlab.figure()

x_0 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]).ravel()
y_0 = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]]).ravel()
z_bottom_0 = np.zeros_like(x_0)
z_top_0 = np.array([[0.5, 1, 1], [1, 1, 1], [1, 1, 1]]).ravel()

x_1 = np.array([0, 1, 1, 2, 2, 2])
y_1 = np.array([2, 1, 2, 0, 1, 2])
z_bottom_1 = np.array([1, 1, 1, 1, 1, 1])
z_top_1 = np.array([0.5, 0.5, 1, 0.5, 1, 1.5])

bar0 = mlab.barchart(x_0, y_0, z_bottom_0, z_top_0, color=c0, line_width=4.0, figure=fig)
bar1 = mlab.barchart(x_1, y_1, z_bottom_1, z_top_1, color=c1, line_width=4.0, figure=fig)

bar0.actor.property.edge_visibility = True
bar0.actor.property.line_width = 4.0
bar1.actor.property.edge_visibility = True
bar1.actor.property.line_width = 4.0

mlab.view(azimuth=-135, elevation=60, distance=15)

mlab.savefig("blah.png", size=(400,400))
# mlab.show()

mlab.close()
