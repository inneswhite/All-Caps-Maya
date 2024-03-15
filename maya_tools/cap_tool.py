import pymel.core as pm 
from math import *
import ui.dialog as dialog
import importlib

importlib.reload(dialog)
pm.stackTrace(state=True)

class MayaCap:
    """ A class containing all Maya functionality for the cap tool. """

    def get_edge_selection(self):
        """ Return the edge selection in the current Maya scene """

        selected_edges = pm.ls(selection=True, flatten=True)
        return selected_edges


    def get_mesh_selection(self, edges: list):
        """ Return the mesh selection in the current Maya scene
        
        Args:
            edges (list): A list of the selected edges in the scene
        """
        # TODO accept other types of selection (i.e mesh, vertex, face etc.)
        # TODO return a list of all selected meshes
        mesh = pm.PyNode(edges[0].split('.')[0])
        return mesh

    def enable_xray(self, mesh, bool):
        pm.select(mesh)
        pm.displaySurface(mesh, xRay=bool)

    def form_cap(self, faces):
        pm.select(faces)
        transform = pm.polyUnite(constructionHistory=False)
        pm.polyMergeVertex(distance=0.001)
        return transform[0]


    def validate_selection(self):
        #TODO Validate number of edges (only even allowed)
        selection = pm.ls(selection=True, flatten=True)
        if len(selection) > 4:
            return True
        else:
            return False

    def create_fan_cap(self):
        """
        
        """
        # TODO Warning pop-up for non-edge selection
        # TODO Block non-even edge selections

        self.edge_selection = self.get_edge_selection()

        # Convert edge selection to vertices and find 
        vertices = pm.ls(pm.polyListComponentConversion(self.edge_selection, fromEdge=True, toVertex=True), flatten=True)
        halfway_vert_i = floor(len(vertices) * 0.5)
        cap_center_pos = (pm.pointPosition(vertices[0]) + pm.pointPosition(vertices[halfway_vert_i])) / 2

        # create first face manually (as it spans first and last index)
        prime_vert = pm.pointPosition(vertices[-1])
        next_vert = pm.pointPosition(vertices[0])
        cap_faces = [pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center_pos])]

        # iterate through vertices to generate triangle face to center
        for vert_index in range(0, len(vertices)-1):
            prime_vert = pm.pointPosition(vertices[vert_index])
            next_vert = pm.pointPosition(vertices[vert_index + 1])
            cap_faces.append(pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center_pos]))

        # combine all new faces into a single mesh
        self.cap_mesh = self.form_cap(cap_faces)
        self.enable_xray(self.cap_mesh, True)

    def create_strip_cap(self):
        self.edge_selection = self.get_edge_selection()
        vertices = pm.ls(pm.polyListComponentConversion(self.edge_selection, fromEdge=True, toVertex=True), flatten=True)
        vertices_len = len(vertices)
        last_vert_i = vertices_len - 1
        
        halfway_vert_i = floor(vertices_len * 0.5)

        vertices_pos = []
        for vertex in vertices:
            vertices_pos.append(pm.pointPosition(vertex))

        cap_faces = []
        n_faces = floor((vertices_len - 2) * 0.25)
        print(n_faces)
        # right-side
        for vert_index in range(0, n_faces):
            cap_faces.append(pm.polyCreateFacet
                             (p=[vertices_pos[vert_index], vertices_pos[vert_index + 1], vertices_pos[halfway_vert_i - (vert_index + 1)], vertices_pos[halfway_vert_i - vert_index]]))
        
        # max-min index face
        cap_faces.append(pm.polyCreateFacet(p=[vertices_pos[0], vertices_pos[halfway_vert_i], vertices_pos[halfway_vert_i + 1], vertices_pos[last_vert_i]]))

        # left-side
        for vert_index in range(1, n_faces):
            cap_faces.append(pm.polyCreateFacet(p=[vertices_pos[last_vert_i - vert_index], vertices_pos[last_vert_i - vert_index + 1], vertices_pos[halfway_vert_i + vert_index], vertices_pos[halfway_vert_i + vert_index + 1]]))
            
        # if multiple of 4, last face is a tri.
        if vertices_len % 4 == 0:
            quarter_vert_i = floor(halfway_vert_i * 0.5)
            three_quarter_vert_i = halfway_vert_i + quarter_vert_i
            cap_faces.append(pm.polyCreateFacet
                             (p=[vertices_pos[quarter_vert_i], vertices_pos[quarter_vert_i + 1], vertices_pos[quarter_vert_i - 1]]))
            cap_faces.append(pm.polyCreateFacet
                             (p=[vertices_pos[three_quarter_vert_i], vertices_pos[three_quarter_vert_i + 1], vertices_pos[three_quarter_vert_i - 1]]))
        
        self.cap_mesh = self.form_cap(cap_faces)
        self.enable_xray(self.cap_mesh, True)

    def create_grid_cap(self):
        pass

    def create_optimal_cap(self):
        pass

    def confirm_cap(self):
        """ Merge the generated cap mesh into the original mesh """
        if not pm.objExists(self.cap_mesh):
            dialog.critical("Error while finding cap mesh.")
            return
        self.enable_xray(self.cap_mesh, False)

maya_cap = MayaCap()
