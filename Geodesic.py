import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from colour import Color
from numpy import array, dot, sqrt, unique, vstack

def distance( p1, p2 ):
    return sqrt( ( p1 - p2 ).dot( p1 - p2 ) )

def average( p1, p2 ):
    return ( p1 + p2 ) / 2

def geodesic( r, f ):
    '''
    Returns a list of polygons and vertices that make
    up a geodesic sphere of radius r and frequency f.
    '''
    def tesselate( p, f ):
        for i in range( f ):
            new_vertices = unique( array(
                [ average( vertex1, vertex2 )
                  for vertex1 in p for vertex2 in p
                  if round( distance( vertex1, vertex2 ), i ) == 1 / ( 2**i ) ]
                ), axis = 0 )
            p = vstack( ( p, new_vertices ) )
        return p

    def edges( p, f ):
        edges = unique( array(
            [ unique( [ vertex1, vertex2 ], axis = 0 )
              for vertex1 in p for vertex2 in p
              if  round( distance( vertex1, vertex2 ), f ) == 1 / ( 2**f ) ]
            ), axis = 0 )
        return edges    

    def polygons( p, f ):
        polygons = unique( array(
            [ unique( [ vertex1, vertex2, vertex3 ], axis = 0 )
              for vertex1 in p for vertex2 in p for vertex3 in p
              if  round( distance( vertex1, vertex2 ), f ) == 1 / ( 2**f )
              and round( distance( vertex2, vertex3 ), f ) == 1 / ( 2**f )
              and round( distance( vertex3, vertex1 ), f ) == 1 / ( 2**f ) ]
            ), axis = 0 )
        return polygons

    def project( p, r ):
        return array( [ ( r * vertex ) / sqrt( ( vertex ).dot( vertex ) )
                        for vertex in p ] )
    
    goldenratio = ( 1 + sqrt( 5 ) ) / 2
    icosahedron = array([
        [ 0.0            ,  0.5            ,  goldenratio / 2 ],
        [ 0.0            , -0.5            ,  goldenratio / 2 ],
        [ 0.0            ,  0.5            , -goldenratio / 2 ],
        [ 0.0            , -0.5            , -goldenratio / 2 ],
        [ 0.5            ,  goldenratio / 2,  0.0             ],
        [-0.5            ,  goldenratio / 2,  0.0             ],
        [ 0.5            , -goldenratio / 2,  0.0             ],
        [-0.5            , -goldenratio / 2,  0.0             ],
        [ goldenratio / 2,  0.0            ,  0.5             ],
        [ goldenratio / 2,  0.0            , -0.5             ],
        [-goldenratio / 2,  0.0            ,  0.5             ],
        [-goldenratio / 2,  0.0            , -0.5             ]   
        ])
    
    tesselation   = tesselate( icosahedron, f )
    edges         = [ project( edge, r ) for edge in edges( tesselation, f ) ]
    triangulation = polygons ( tesselation, f )
    projection    = [ project( polygon, r ) for polygon in triangulation ]
    return projection, edges, project( tesselation, r )

polys, edges, p = geodesic( 1, 1 )
x = p[:,0]
y = p[:,1]
z = p[:,2]

colors = list( Color( 'grey' ).range_to( Color( 'yellow' ), len( polys ) ) )
ax = plt.axes( projection = '3d' )
i = 0
for poly in polys:
    ax.add_collection3d( Poly3DCollection( verts = [ poly ],
                                           facecolors = str( colors[ i ] ),
                                           edgecolor = 'black' ) )
    i += 1
ax.add_collection3d( Line3DCollection( segments = [ edge for edge in edges ],
                                       colors = 'black', linewidths = 1,
                                       linestyles = ':', alpha = 0.4 ) )
ax.scatter( x, y, z, c = 'red' )
ax.axis( 'off' )
ax.grid( b = None )
plt.show()
