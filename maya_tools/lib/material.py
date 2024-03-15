import pymel.core as pm

def get_transparent_material():
    """ Assign a transparent material to a given selection of faces"""
    #TODO return the transparent material if it already exists
    shader = pm.shadingNode("lambert", asShader=True, name="temp-transparent-cap")
    shader.color.set((1, 0.5, 0.5))
    shader.transparency.set((0.5, 0.5, 0.5))
    
    sg = pm.sets(renderable=True, noSurfaceShader=True, empty=True)
    pm.connectAttr(shader + ".outColor", sg +".surfaceShader", force=True)
    return sg


def get_lambert1():
    """ Returns the default lambert1 material from the scene. If no default material exists, one is created. """

    lambert1 = pm.ls("lambert1")
    if lambert1:
        return lambert1[0]
    else:
        return  pm.shadingNode("lambert1", asShader=True)
    
def get_assigned_materials(mesh):
    """ returns a list of materials assigned to a given mesh"""
    mesh = self.mesh_selection
    assigned_materials = []
    shading_engines = mesh.listConnections(type="shadingEngine")
    for shading_engine in shading_engines:
        assigned_materials.extend(shading_engine.surfaceShader.listConnections())
    return assigned_materials

def assign_material(mesh, material):
    face_selection_string = str(mesh[0]) + ".f[0:9]"
    mesh_shape = pm.PyNode(str(mesh[0])).getShape()
    print(material)
    pm.sets(mesh_shape, edit=True, forceElement=material)