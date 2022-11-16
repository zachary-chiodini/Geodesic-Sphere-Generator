from math import sqrt
from matplotlib.pyplot import axes, show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Union


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

    def __init__(self, frequency: int = 0, hollow: bool = False, thinness_factor: int = 0):
        self.w = int(frequency)
        self.t = int(thinness_factor)
        self.p = self.verts.copy()
        self.f = self.faces.copy()
        self._tesselate()
        self._project()
        if hollow:
            self._hollow()

    def _hollow(self) -> None:
        for face in self.f.copy():
            v1, v2, v3 = face
            cp = ((v1[0] + v2[0] + v3[0]) / 3, (v1[1] + v2[1] + v3[1]) / 3, (v1[2] + v2[2] + v3[2]) / 3)
            shrunken_face = [0.0, 0.0, 0.0]
            for i, v in enumerate(face):
                x, y, z = (v[0] + cp[0]) / 2, (v[1] + cp[1]) / 2, (v[2] + cp[2]) / 2
                for _ in range(self.t):
                    x, y, z = (v[0] + x) / 2, (v[1] + y) / 2, (v[2] + z) / 2
                shrunken_face[i] = (x, y, z)
            self.f.remove(face)
            face1 = (v1, v2, shrunken_face[1], shrunken_face[0])
            face2 = (v2, v3, shrunken_face[2], shrunken_face[1])
            face3 = (v3, v1, shrunken_face[0], shrunken_face[2])
            self.f.update([face1, face2, face3])
        return None

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
                mid_point1 = ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2)
                mid_point2 = ((v2[0] + v3[0]) / 2, (v2[1] + v3[1]) / 2, (v2[2] + v3[2]) / 2)
                mid_point3 = ((v3[0] + v1[0]) / 2, (v3[1] + v1[1]) / 2, (v3[2] + v1[2]) / 2)
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
    GeodesicSphere(frequency=2, hollow=True, thinness_factor=1).plot()
