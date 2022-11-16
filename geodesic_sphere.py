from math import sqrt
from matplotlib.pyplot import axes, show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class GeodesicSphere:

    golden_ratio = (1 + sqrt(5)) / 2
    faces = {  # These are the faces of a regular icosahedron.
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
                face1 = (v1, mid_point1, mid_point3)
                face2 = (mid_point1, v2, mid_point2)
                face3 = (mid_point2, mid_point3, v3)
                face4 = (mid_point1, mid_point2, mid_point3)
                self.f.remove(face)
                self.f.update([face1, face2, face3, face4])
        return None
    
    def plot(self) -> None:
        ax = axes(projection='3d')
        for face in self.f:
            ax.add_collection3d(Poly3DCollection(verts=[face], facecolors='white', edgecolor='black'))
        ax.axis('off')
        ax.grid(visible=None)
        ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
        ax.set_aspect('equal', 'box')
        show()
        return None


if __name__ == '__main__':
    geodesic_sphere = GeodesicSphere(1)
    geodesic_sphere.plot()
