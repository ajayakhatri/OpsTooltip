# OpsTooltip
Creates tooltip for nodes and elements from OpenSeesPy with mplcursors.

<img src="demo.gif" alt="demo of OpsTooltip" height="350px">

## Description
- This script enables users to obtain information about nodes and elements by hovering over them. Initially, it generates a JSON file containing information about geometry i.e. nodes and elements. Subsequently, the script reads the node and element data from the JSON file. Finally, it utilizes [mplcursors](https://github.com/anntzer/mplcursors) to create tooltips, providing insights when users hover over nodes and elements during visualization.

- Users can display tooltip for elements and nodes with `get_tooltips_for_elements` and `get_tooltips_for_nodes` functions, respectively. In addition, custom texts can be added with `add_custom_text` function.

- The script uses Matplotlib's **ax** object as input, facilitating seamless integration with [opsvis](https://github.com/sewkokot/opsvis) (OpenSeesPy postprocessing and plotting module). Examples of 2D and 3D models are give in `example2D.py` and `example3D.py`, respectively.

```
# Example
# create a figure
fig = plt.figure()
ax1 = fig.add_subplot(111)

# use ax in plot_model
opsv.plot_model(ax=ax1)

# add custom texts
add_custom_text("element", 1, "This is element no.1.")
add_custom_text("node", 3, "This is a fixed support.\n This is node no.3")

# use the previous ax to generate tooltips
get_tooltips_for_elements(ax1)
get_tooltips_for_nodes(ax1)
```

Note:
- The tooltips are functional when figure is shown in a new window. You can use `%matplotlib qt` to change default inline display to a windows display in your Jupyter Notebook.
- You will require mplcursors, openseespy and numpy libraries. You can install these with a pip command `pip install -r requirements.txt`.

