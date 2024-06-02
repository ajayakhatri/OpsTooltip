import openseespy.opensees as ops
import matplotlib.pyplot as plt
from opsTooltip import *
import opsvis as opsv

ops.wipe()

ops.model('basic', '-ndm', 2, '-ndf', 3)

# defining nodes
ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, 6.0)
ops.node(3, 7.0, 0.0)
ops.node(4, 7.0, 6.0)

# fixing nodes 1 and 3
ops.fix(1, 1, 1, 1)
ops.fix(3, 1, 1, 1)

ops.geomTransf('Linear', 1)

# defining elements
ops.element('elasticBeamColumn', 1, 1, 2, 2.5e-3, 200.e9, 1.5e-5, 1)
ops.element('elasticBeamColumn', 2, 3, 4, 2.5e-3, 200.e9, 1.5e-5, 1)
ops.element('elasticBeamColumn', 3, 2, 4, 2.5e-3, 200.e9, 1.5e-5, 1)

# create a figure
fig = plt.figure()
ax1 = fig.add_subplot(111)

# using axes in plot_model
opsv.plot_model(ax=ax1)

# Adding custom text
add_custom_text("element", 1, "This is element no.1.")
add_custom_text("node", 3, "This is a fixed support.\n This is node no.3")

# using the previous axes to generate tooltips
get_tooltips_for_elements(ax1)
get_tooltips_for_nodes(ax1)
plt.show()

ops.wipe()
exit()
