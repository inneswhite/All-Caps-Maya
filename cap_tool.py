import pymel.core as pm 
import math 

def create_fan_cap():
    # get selected edges
    selected_edges = pm.ls(selection=True, flatten=True)
    mesh = pm.PyNode(selected_edges[0].split('.')[0])

    pm.select(mesh)
    # TODO Warning pop-up for non-edge selection
    # TODO Block non-even edge selections

    # get all the faces
    mesh_faces = pm.ls(pm.polyListComponentConversion(selected_edges, fromEdge=True, toFace=True), flatten=True)
    pm.select(mesh_faces[-1])

    # Select vertices from edge ring
    vertices = pm.ls(pm.polyListComponentConversion(selected_edges, fromEdge=True, toVertex=True), flatten=True)

    # create fan cap
    half_vertices = math.floor(len(vertices) * 0.5)
    """ for vert_index in range(1, half_vertices):
        origin_vert = vertices[vert_index]
        opposite_vert = vertices[vert_index + half_vertices]
        pm.polyConnectComponents(origin_vert, opposite_vert) """

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
    pm.select(mesh, add=True)
    pm.polyUnite(constructionHistory=False)
    pm.polyMergeVertex(distance=0.001)