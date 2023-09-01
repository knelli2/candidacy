import numpy as np
from staggered import *

def test_off_screen_render():
    from mayavi import mlab

    mlab.options.offscreen = True

    fig = mlab.figure(bgcolor=transparent)

    x = np.array([0])
    y = np.array([0])
    z_bottom = np.array([0])
    z_top = np.array([1])

    bar = mlab.barchart(x, y, z_bottom, z_top, color=green, figure=fig)

    mlab.view(azimuth=-135, elevation=60, distance=15)

    mlab.savefig("blah.png", size=(400,400))

    mlab.close()