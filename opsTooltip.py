import openseespy.opensees as ops
import numpy as np
import mplcursors
import json


class Custom_Text:
    """
    Class for custom_text

    elements_text : dict
    nodes_text : dict
    """
    elements_text: dict = {}
    nodes_text: dict = {}


def get_label_data(label_type):

    def replace_nan_in_text(content):
        """
        Extracts geometry information (nodes and elements) information from JSON file.
        To locate correct nodes and elements position, string from the following link is used. 
        https://github.com/zhuminjie/OpenSeesPy/blob/26dcd5f867fbd22134f6414bf7c35fc8a353512d/DEVELOPER/core/Domain.cpp#L2199-L2233
        """

        # Find the starting point of the "geometry" section
        node_start = content.find('\t\t\"nodes\": [\n')
        element_start = content.find('\t\t\"elements\": [\n')
        element_end = content.find('\n\t}\n', element_start)
        geometry_content = content[node_start:element_end]
        text = "{\n"
        text += geometry_content
        text += "\n}"
        return text

    def process_json_file(input_file):
        # Read the JSON file as text
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        #  Extracts nodes and elements information from JSON file.
        modified_text = replace_nan_in_text(text)
        # # Parse the modified text into a JSON object
        data = json.loads(modified_text)
        return data

    file_name = f"opsTooltip-json-temp-file.json"
    try:
        ops.printModel('-JSON', '-file', file_name)
        data = process_json_file(file_name)

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None

    except TypeError as e:
        print(f"TypeError: {e}")
        return None

    if not data:
        return None
    else:
        if label_type == "node":
            nodes_src = data["nodes"]
            return nodes_src
        elif label_type == "element":
            elements_src = data["elements"]
            return elements_src


def add_custom_text(obj_type: str, tag: int, text: str):
    """
    obj_type: element or node
    tag: element tag or node tag
    text: custom text for the element or the node
    """
    if obj_type == "element":
        Custom_Text.elements_text[tag] = text
    elif obj_type == "node":
        Custom_Text.nodes_text[tag] = text


def get_tooltips_for_elements(ax):
    # get element data from printModel json file.
    data = get_label_data("element")
    if not data:
        return None

    elements_src = data
    ndim = ops.getNDM()[0]

    elements = {}
    element_info_clean = {}
    for n in elements_src:
        clean = ""
        for i in n:
            if i == "name":
                clean += f"Element_tag: {n[i]} \n"
                if n[i] in Custom_Text.elements_text:
                    clean += f"Custom_text: {Custom_Text.elements_text[n[i]]} \n"
            else:
                clean += f"{i}: {n[i]} \n"
        element_info_clean[n["name"]] = clean

    for ele in elements_src:
        elements[ele["name"]] = ele["nodes"]

    def get_Middle_Line(i_coord, j_coord):
        # Interpolation to get the middle 70% of the line segment

        num_points = 100  # Number of points for smooth interpolation
        x_full = np.linspace(i_coord[0], j_coord[0], num_points)
        y_full = np.linspace(i_coord[1], j_coord[1], num_points)
        # Determine the middle 60% range
        start_idx = int(num_points * 0.15)
        end_idx = int(num_points * 0.85)

        x_middle = x_full[start_idx:end_idx]
        y_middle = y_full[start_idx:end_idx]

        if ndim == 2:
            return [x_middle, y_middle]

        elif ndim == 3:
            z_full = np.linspace(i_coord[2], j_coord[2], num_points)
            z_middle = z_full[start_idx:end_idx]
            return [x_middle, y_middle, z_middle]

    for i, ele in enumerate(elements):
        i_coord = ops.nodeCoord(elements[ele][0])
        j_coord = ops.nodeCoord(elements[ele][1])

        if ndim == 2:
            line, = ax.plot(*get_Middle_Line(i_coord, j_coord),
                            color='none', linestyle='-')
            mplcursors.cursor(line, hover=mplcursors.HoverMode.Transient).connect(
                "add", lambda sel, ele=ele: sel.annotation.set_text(element_info_clean[ele]))
        elif ndim == 3:
            line, = ax.plot(*get_Middle_Line(i_coord, j_coord),
                            color='none', linestyle='-')
            mplcursors.cursor(line, hover=mplcursors.HoverMode.Transient).connect(
                "add", lambda sel, ele=ele: sel.annotation.set_text(element_info_clean[ele]))
        else:
            return None
    return ax


def get_tooltips_for_nodes(ax):
    # get element data from printModel json file.
    data = get_label_data("node")
    if not data:
        return None

    nodes_src = data
    ndim = ops.getNDM()[0]

    nodes_x = []
    nodes_y = []
    nodes_z = []
    node_info_clean = []
    for n in nodes_src:
        crd = n["crd"]
        nodes_x.append(crd[0])
        nodes_y.append(crd[1])
        if ndim == 3:
            nodes_z.append(crd[2])
        clean = ""
        for i in n:
            if i == "name":
                clean += f"Node__tag: {n[i]} \n"
                if n[i] in Custom_Text.nodes_text:
                    clean += f"Custom_text: {Custom_Text.nodes_text[n[i]]} \n"
            else:
                clean += f"{i}: {n[i]} \n"
        node_info_clean.append(clean)

    if ndim == 2:
        points = ax.scatter(nodes_x, nodes_y, marker='o', color='none')
    elif ndim == 3:
        points = ax.scatter(nodes_x, nodes_y, nodes_z,
                            marker='o', color='none')
    else:
        return None
    cursor = mplcursors.cursor(points, hover=mplcursors.HoverMode.Transient)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        node_info_clean[sel.index]))
