from panda3d.core import GeomVertexData, GeomVertexFormat, GeomTriangles, Geom, GeomNode, NodePath

from array import array



class ProceduralMesh:
    __slots__=(
        'verts',
        'gtris',
        'tri_array',
        'vert_data',
        'tri_data'
        )

    V3N3 = GeomVertexFormat.get_v3n3()
    def __init__(self, format=V3N3, verts=[], tris=[]):
        self.verts = GeomVertexData("vertex_data", GeomVertexFormat.get_v3n3(), Geom.UH_static)

        self.gtris = GeomTriangles( Geom.UH_static )
        self.gtris.set_index_type( Geom.NT_uint32 )
        self.tri_array = self.gtris.modify_vertices()

        self.vert_data = array('f', verts)
        self.tri_data = array('I', tris)

    def set_data(self, verts, tris):
        self.vert_data.extend(verts)
        self.tri_data.extend(tris)

    def create_mesh(self):
        #Each element is verts+normal, divide by 3 to get the x,y,z of each, then divide by 2 to combine normals hence 5:
        row_count = int(len(self.vert_data)/5)
        self.verts.unclean_set_num_rows( row_count )
        memview = memoryview( self.verts.modify_array(0) ).cast('B').cast('f')
        memview[:] = self.vert_data

        self.gtris.reserve_num_vertices( len(self.tri_data) )
        self.tri_array.unclean_set_num_rows( len(self.tri_data) )
        memview = memoryview(self.tri_array).cast('B').cast('I')
        memview[:] = self.tri_data

        geom = Geom( self.verts )
        geom.add_primitive( self.gtris )
        geom_node = GeomNode('geom')
        geom_node.add_geom(geom)
        mesh = NodePath(geom_node)
        mesh.set_tag('copy', '')
        return mesh





