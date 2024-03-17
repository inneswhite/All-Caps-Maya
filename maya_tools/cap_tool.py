import pymel.core as pm
from math import *
import ui.dialog as dialog
import importlib
from enum import Enum

importlib.reload(dialog)
pm.stackTrace(state=True)


class Cap_Type(Enum):
    fan = "fan"
    strip = "strip"
    grid = "grid"
    max_area = "max_area"
    undefined = "undefined"


class MayaCap:
    """A class containing all Maya functionality for the cap tool."""

    selection_is_made = False
    base_edges = None
    base_mesh = None
    base_vertices = None
    cap_mesh = None
    rotation_offset = 0
    undoChunk = None
    print("still updates?")

    def populate_selections(self):
        """Populate the class selection variables"""

        self.base_edges = pm.ls(selection=True, flatten=True)
        self.base_mesh = pm.PyNode(self.base_edges[0].split(".")[0])
        self.base_vertices = pm.ls(
            pm.polyListComponentConversion(
                self.base_edges, fromEdge=True, toVertex=True
            ),
            flatten=True,
        )

    def shift_array(self, arr, shift_value):
        shift_value = shift_value * -1
        return arr[shift_value:] + arr[:shift_value]

    def enable_xray(self, mesh, bool):
        pm.select(mesh)
        pm.displaySurface(mesh, xRay=bool)

    def form_cap(self, faces):
        pm.select(faces)
        transform = pm.polyUnite(constructionHistory=False)
        pm.polyMergeVertex(distance=0.001)
        return transform[0]

    def merge_cap(self):
        pm.select([self.cap_mesh, self.base_mesh])
        base_name = self.base_mesh.name()
        print(
            "Cap Mesh in merge_cap() = {}\n and base mesh = {}".format(
                self.cap_mesh, self.base_mesh
            )
        )
        pm.polyUnite(constructionHistory=False, name=base_name)
        pm.polyMergeVertex(distance=0.001)
        # Return to object mode
        pm.select(clear=True)
        pm.select(base_name)

    def validate_selection(self):
        # TODO Validate number of edges (only even allowed)
        selection = pm.ls(selection=True, flatten=True)
        if len(selection) > 4 or self.selection_is_made:
            return True
        else:
            return False

    def create_fan_cap(self):
        """ """
        # TODO Warning pop-up for non-edge selection
        # TODO Block non-even edge selections

        # Convert edge selection to vertices and find
        halfway_vert_i = floor(len(self.base_vertices) * 0.5)
        cap_center_pos = (
            pm.pointPosition(self.base_vertices[0])
            + pm.pointPosition(self.base_vertices[halfway_vert_i])
        ) / 2

        # create first face manually (as it spans first and last index)
        prime_vert = pm.pointPosition(self.base_vertices[-1])
        next_vert = pm.pointPosition(self.base_vertices[0])
        cap_faces = [pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center_pos])]

        # iterate through vertices to generate triangle face to center
        for vert_index in range(0, len(self.base_vertices) - 1):
            prime_vert = pm.pointPosition(self.base_vertices[vert_index])
            next_vert = pm.pointPosition(self.base_vertices[vert_index + 1])
            cap_faces.append(
                pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center_pos])
            )

        # combine all new faces into a single mesh
        self.cap_mesh = self.form_cap(cap_faces)

    def create_strip_cap(self):
        vertices_len = len(self.base_vertices)
        last_vert_i = vertices_len - 1

        halfway_vert_i = floor(vertices_len * 0.5)

        vertices_pos = []
        for vertex in self.base_vertices:
            vertices_pos.append(pm.pointPosition(vertex))

        cap_faces = []
        n_faces = floor((vertices_len - 2) * 0.25)

        # draw faces on right side
        for vert_index in range(0, n_faces):
            cap_faces.append(
                pm.polyCreateFacet(
                    p=[
                        vertices_pos[vert_index],
                        vertices_pos[vert_index + 1],
                        vertices_pos[halfway_vert_i - (vert_index + 1)],
                        vertices_pos[halfway_vert_i - vert_index],
                    ]
                )
            )

        # max-min index face
        cap_faces.append(
            pm.polyCreateFacet(
                p=[
                    vertices_pos[0],
                    vertices_pos[halfway_vert_i],
                    vertices_pos[halfway_vert_i + 1],
                    vertices_pos[last_vert_i],
                ]
            )
        )

        # left-side
        for vert_index in range(1, n_faces):
            cap_faces.append(
                pm.polyCreateFacet(
                    p=[
                        vertices_pos[last_vert_i - vert_index],
                        vertices_pos[last_vert_i - vert_index + 1],
                        vertices_pos[halfway_vert_i + vert_index],
                        vertices_pos[halfway_vert_i + vert_index + 1],
                    ]
                )
            )

        # if multiple of 4, last face is a tri.
        if vertices_len % 4 == 0:
            quarter_vert_i = floor(halfway_vert_i * 0.5)
            three_quarter_vert_i = halfway_vert_i + quarter_vert_i
            cap_faces.append(
                pm.polyCreateFacet(
                    p=[
                        vertices_pos[quarter_vert_i],
                        vertices_pos[quarter_vert_i + 1],
                        vertices_pos[quarter_vert_i - 1],
                    ]
                )
            )
            cap_faces.append(
                pm.polyCreateFacet(
                    p=[
                        vertices_pos[three_quarter_vert_i],
                        vertices_pos[three_quarter_vert_i + 1],
                        vertices_pos[three_quarter_vert_i - 1],
                    ]
                )
            )

        self.cap_mesh = self.form_cap(cap_faces)

    def create_grid_cap(self):
        vertices_count = len(self.base_vertices)
        last_vert_i = vertices_count - 1

        halfway_vert_i = floor(vertices_count * 0.5)

        vertices_pos = []
        for vertex in self.base_vertices:
            vertices_pos.append(pm.pointPosition(vertex))

        cap_faces = []
        n_faces = floor((vertices_count - 2) * 0.25) - 1

        # create new verts down the middle
        middle_verts = []
        for vert_i in range(0, n_faces + 1):
            middle_verts.append(
                (vertices_pos[vert_i] + vertices_pos[halfway_vert_i - vert_i]) * 0.5,
            )

        for vert_i in range(0, (n_faces)):
            middle_verts.append(
                (
                    vertices_pos[last_vert_i - vert_i]
                    + vertices_pos[halfway_vert_i + (vert_i + 1)]
                )
                * 0.5,
            )

        # Draw grid faces
        # right faces
        for f in range(0, n_faces):
            cap_faces.extend(
                [
                    # bottom-right
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[f],
                            vertices_pos[f + 1],
                            middle_verts[f + 1],
                            middle_verts[f],
                        ]
                    ),
                    # top-right
                    pm.polyCreateFacet(
                        p=[
                            middle_verts[f],
                            middle_verts[f + 1],
                            vertices_pos[halfway_vert_i - 1 - f],
                            vertices_pos[halfway_vert_i - f],
                        ]
                    ),
                ]
            )

            # left starters
        cap_faces.extend(
            [
                pm.polyCreateFacet(
                    p=[
                        vertices_pos[0],
                        middle_verts[0],
                        middle_verts[n_faces + 1],
                        vertices_pos[last_vert_i],
                    ]
                ),
                pm.polyCreateFacet(
                    p=[
                        middle_verts[0],
                        vertices_pos[halfway_vert_i],
                        vertices_pos[halfway_vert_i + 1],
                        middle_verts[n_faces + 1],
                    ]
                ),
            ]
        )

        #   bottom - left
        for f in range(1, n_faces):
            cap_faces.extend(
                [
                    # top-left
                    pm.polyCreateFacet(
                        p=[
                            middle_verts[n_faces + f],
                            vertices_pos[halfway_vert_i + f],
                            vertices_pos[halfway_vert_i + f + 1],
                            middle_verts[n_faces + f + 1],
                        ]
                    ),
                    # bottom-left
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[last_vert_i - f + 1],
                            middle_verts[n_faces + f],
                            middle_verts[n_faces + 1 + f],
                            vertices_pos[last_vert_i - f],
                        ]
                    ),
                ]
            )

        # end faces
        quarter_vert_i = floor(halfway_vert_i * 0.5)
        three_quarter_vert_i = halfway_vert_i + quarter_vert_i
        if vertices_count % 4 == 0:
            cap_faces.extend(
                [
                    # top-right
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[quarter_vert_i],
                            vertices_pos[quarter_vert_i + 1],
                            vertices_pos[quarter_vert_i + 2],
                            middle_verts[n_faces],
                        ]
                    ),
                    # bottom-right
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[quarter_vert_i],
                            middle_verts[n_faces],
                            vertices_pos[quarter_vert_i - 2],
                            vertices_pos[quarter_vert_i - 1],
                        ]
                    ),
                    # top-left
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[three_quarter_vert_i],
                            vertices_pos[three_quarter_vert_i + 1],
                            vertices_pos[three_quarter_vert_i + 2],
                            middle_verts[n_faces * 2],
                        ]
                    ),
                    # bottom-left
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[three_quarter_vert_i],
                            middle_verts[n_faces * 2],
                            vertices_pos[three_quarter_vert_i - 2],
                            vertices_pos[three_quarter_vert_i - 1],
                        ]
                    ),
                ]
            )
        # right
        elif vertices_count % 2 == 0:
            floor_quart_vert = floor(quarter_vert_i)
            floor_3_quart_vert = floor(three_quarter_vert_i)
            cap_faces.extend(
                [
                    # right-top-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_quart_vert - 1],
                            vertices_pos[floor_quart_vert],
                            middle_verts[n_faces],
                        ]
                    ),
                    # right-mid-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_quart_vert],
                            vertices_pos[floor_quart_vert + 1],
                            middle_verts[n_faces],
                        ]
                    ),
                    # right-bottom-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_quart_vert + 1],
                            vertices_pos[floor_quart_vert + 2],
                            middle_verts[n_faces],
                        ]
                    ),
                    # left-top-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_3_quart_vert - 1],
                            vertices_pos[floor_3_quart_vert],
                            middle_verts[n_faces * 2],
                        ]
                    ),
                    # left-mid-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_3_quart_vert],
                            vertices_pos[floor_3_quart_vert + 1],
                            middle_verts[n_faces * 2],
                        ]
                    ),
                    # left-bottom-tri
                    pm.polyCreateFacet(
                        p=[
                            vertices_pos[floor_3_quart_vert + 1],
                            vertices_pos[floor_3_quart_vert + 2],
                            middle_verts[n_faces * 2],
                        ]
                    ),
                ]
            )
        self.cap_mesh = self.form_cap(cap_faces)

    def create_max_area_cap(self):
        self.selection_is_made = True
        pass

    def confirm_cap(self):
        """# TODO"""
        pm.undoInfo(closeChunk=True)

    def revert_state(self):
        pm.undoInfo(closeChunk=True)
        pm.undo()

    def create_cap(self, cap_type: Cap_Type, rot_offset=0):
        """Performs the generic operations required for all cap types, before building the cap type defined in the argument

        Args:
            cap_type (Cap_Type): Determines the cap type to build (fan, strip, grid or max_area)
        """
        # If a cap is already made, revert it, else it is the first time a cap has been made: populate the selection params and start the undo chunk
        if self.selection_is_made:
            pm.undoInfo(closeChunk=True)
            pm.undo()

            # pm.select(self.base_edges)
        self.selection_is_made = True
        pm.undoInfo(chunkName="Create_Cap", openChunk=True, infinity=True)
        self.populate_selections()

        self.rotation_offset = rot_offset

        # link up possible cap types to respective methods
        cap_types = {
            "fan": self.create_fan_cap,
            "strip": self.create_strip_cap,
            "grid": self.create_grid_cap,
            "max_area": self.create_max_area_cap,
            "undefined": lambda: dialog.critical("Cap Type Undefined"),
        }
        cap_selection = cap_types[cap_type.value]

        if cap_selection:
            cap_selection()
        else:
            dialog.critical(
                "Could not find corresponding cap type for {} ".format(cap_type.value)
            )

        self.merge_cap()


maya_cap = MayaCap()

if __name__ == "__main__":

    maya_cap.create_cap(Cap_Type.grid)
