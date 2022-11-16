from math import sqrt
from matplotlib.pyplot import axes, show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class GeodesicSphere:

    golden_ratio = (1 + sqrt(5)) / 2
    # These are the vertices of a regular icosahedron.
    verts = {
		( golden_ratio / 2,  0.0             ,  0.5              ),
		( golden_ratio / 2,  0.0             , -0.5              ),
		(-golden_ratio / 2,  0.0             ,  0.5              ),
		(-golden_ratio / 2,  0.0             , -0.5              ),
		( 0.5             ,  golden_ratio / 2,  0.0              ),
		(-0.5             ,  golden_ratio / 2,  0.0              ),
		( 0.5             , -golden_ratio / 2,  0.0              ),
		(-0.5             , -golden_ratio / 2,  0.0              ),
		( 0.0             ,  0.5             ,  golden_ratio / 2 ),
		( 0.0             , -0.5             ,  golden_ratio / 2 ),
		( 0.0             ,  0.5             , -golden_ratio / 2 ),
		( 0.0             , -0.5             , -golden_ratio / 2 )
	}
    # These are the faces of a regular icosahedron.
    faces = {
		((-golden_ratio / 2,  0.0             , -0.5              ),
         (-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             , -golden_ratio / 2,  0.0              )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             ,  golden_ratio / 2,  0.0              )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             , -golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         ( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 )),
        ((-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              )),
        ((-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              )),
        ((-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              )),
        ((-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              )),
        (( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             , -0.5              )),
        (( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              )),
        (( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              )),
        (( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.5             , -golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              ),
         ( golden_ratio / 2,  0.0             ,  0.5              ))
	}

    def __init__(self, frequency: int = 0):
        self.w = int(frequency)
        self.p = self.verts.copy()
        self.f = self.faces.copy()
        self._tesselate()
        self._project()

    def _project(self) -> None:
        """
        This function projects each vertex of each face onto the surface of a sphere of radius 1.
        """
        for face in self.f.copy():
            projected_face = []
            for x, y, z in face:
                m = sqrt(x**2 + y**2 + z**2)
                projected_face.append((x / m, y / m, z / m))
            self.f.remove(face)
            self.f.add(tuple(projected_face))
        for vert in self.p.copy():
            x, y, z = vert
            m = sqrt(x**2 + y**2 + z**2)
            projected_vert = (x / m, y / m, z / m)
            self.p.remove(vert)
            self.p.add(projected_vert)
        return None

    def _tesselate(self) -> None:
        """
        This function takes each face of the icosahedron and creates 4 new faces within it.
        """
        for _ in range(self.w):
            for face in self.f.copy():
                v1, v2, v3 = face
                x1, y1, z1 = v1
                x2, y2, z2 = v2
                x3, y3, z3 = v3
                mid_point1 = ((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2)
                mid_point2 = ((x2 + x3) / 2, (y2 + y3) / 2, (z2 + z3) / 2)
                mid_point3 = ((x3 + x1) / 2, (y3 + y1) / 2, (z3 + z1) / 2)
                self.p.update([mid_point1, mid_point2, mid_point3])
                face1 = (v1, mid_point1, mid_point3)
                face2 = (mid_point1, v2, mid_point2)
                face3 = (mid_point2, mid_point3, v3)
                face4 = (mid_point1, mid_point2, mid_point3)
                self.f.remove(face)
                self.f.update([face1, face2, face3, face4])
        return None

    def plot(self) -> None:
        ax = axes(projection='3d')
        ax.scatter(*zip(*self.p), alpha=0)
        ax.add_collection3d(Poly3DCollection(verts=list(self.f), facecolors='white', edgecolor='black'))
        ax.axis('off')
        ax.grid(visible=None)
        ax.set_aspect('equal', 'box')
        show()
        return None


if __name__ == '__main__':
    GeodesicSphere(frequency=1).plot()
