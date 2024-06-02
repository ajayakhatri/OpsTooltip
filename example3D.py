import openseespy.opensees as ops
import matplotlib.pyplot as plt
from opsTooltip import *
import opsvis as opsv


##################################################################

# Statics of a 3d 3-element cantilever beam
# Original code taken from:  https://opsvis.readthedocs.io/en/latest/ex_3d_3el_cantilever.html

##################################################################

ops.wipe()

ops.model('basic', '-ndm', 3, '-ndf', 6)

b = 0.2
h = 0.4

A, Iz, Iy, J = 0.04, 0.0010667, 0.0002667, 0.01172

E = 25.0e6
G = 9615384.6

# Lx, Ly, Lz = 4., 3., 5.
Lx, Ly, Lz = 4., 4., 4.

ops.node(1, 0., 0., 0.)
ops.node(2, 0., 0., Lz)
ops.node(3, Lx, 0., Lz)
ops.node(4, Lx, Ly, Lz)

ops.fix(1, 1, 1, 1, 1, 1, 1)

lmass = 200.

ops.mass(2, lmass, lmass, lmass, 0.001, 0.001, 0.001)
ops.mass(3, lmass, lmass, lmass, 0.001, 0.001, 0.001)
ops.mass(4, lmass, lmass, lmass, 0.001, 0.001, 0.001)

gTTagz = 1
gTTagx = 2
gTTagy = 3

coordTransf = 'Linear'
ops.geomTransf(coordTransf, gTTagz, 0., -1., 0.)
ops.geomTransf(coordTransf, gTTagx, 0., -1., 0.)
ops.geomTransf(coordTransf, gTTagy, 1., 0., 0.)

ops.element('elasticBeamColumn', 1, 1, 2, A, E, G, J, Iy, Iz, gTTagz)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, G, J, Iy, Iz, gTTagx)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, G, J, Iy, Iz, gTTagy)


fig_wi_he = 30., 20.
ele_shapes = {1: ['circ', [h]],
              2: ['rect', [b, h]],
              3: ['I', [b, h, b/10., h/6.]]}

fig = plt.figure()
ax1 = fig.add_subplot(111, projection="3d")
opsv.plot_extruded_shapes_3d(ele_shapes, fig_wi_he=fig_wi_he, ax=ax1)


# Adding custom texts
add_custom_text("element", 1, "Hello, this is element 1")
add_custom_text("node", 2, "Hello, this is node 2")

get_tooltips_for_elements(ax1)
get_tooltips_for_nodes(ax1)

plt.show()

wipe()

exit()
