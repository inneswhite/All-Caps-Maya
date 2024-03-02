import pymel.core as pm 
import math 
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

    def enable_xray(self, mesh):
        pm.displaySurface(mesh, xRay=True)

    def valid_selection(self):
        selection = pm.ls(selection=True, flatten=True)
        if len(selection) > 1:
            return True
        else:
            return False

    def create_fan_cap(self):
        """
        
        """
        # TODO Warning pop-up for non-edge selection
        # TODO Block non-even edge selections

        self.edge_selection = self.get_edge_selection()
        self.mesh_selection = self.get_mesh_selection(self.edge_selection)
        # get all the faces
        mesh_faces = pm.ls(pm.polyListComponentConversion(self.edge_selection, fromEdge=True, toFace=True), flatten=True)
        pm.select(mesh_faces[-1])

        # Select vertices from edge ring
        vertices = pm.ls(pm.polyListComponentConversion(self.edge_selection, fromEdge=True, toVertex=True), flatten=True)

        # create fan cap
        half_vertices = math.floor(len(vertices) * 0.5)

        #pdb.set_trace()
        cap_center = (pm.pointPosition(vertices[0]) + pm.pointPosition(vertices[half_vertices])) / 2
        pm.select(vertices[0])

        prime_vert = pm.pointPosition(vertices[-1])
        next_vert = pm.pointPosition(vertices[0])
        cap_faces = [pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center])]

        for vert_index in range(0, len(vertices)-1):
            prime_vert = pm.pointPosition(vertices[vert_index])
            next_vert = pm.pointPosition(vertices[vert_index + 1])
            cap_faces.append(pm.polyCreateFacet(p=[prime_vert, next_vert, cap_center]))

        pm.select(cap_faces)
        self.cap_mesh = pm.polyUnite(constructionHistory=False)

        self.enable_xray(self.cap_mesh)


    def create_strip_cap(self):
        vertices = pm.ls(pm.polyListComponentConversion(self.edge_selection, fromEdge=True, toVertex=True), flatten=True)
        
        pass

    def confirm_cap(self):
        """ Merge the generated cap mesh into the original mesh """
        if not pm.objExists(self.cap_mesh):
            dialog.critical("Error while finding cap mesh.")
            return
        pm.select(self.mesh_selection, add=True)
        pm.polyUnite(constructionHistory=False)
        pm.polyMergeVertex(distance=0.001)

maya_cap = MayaCap()