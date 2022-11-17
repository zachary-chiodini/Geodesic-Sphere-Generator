from math import sqrt
from matplotlib.pyplot import axes, show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class GeodesicSphere:

    golden_ratio = (1 + sqrt(5)) / 2
    # These are the faces of a regular icosahedron.
    faces = {
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-0.5             , -golden_ratio / 2,  0.0              ),
         (-golden_ratio / 2,  0.0             ,  0.5              )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             ,  golden_ratio / 2,  0.0              )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         ( 0.0             , -0.5             , -golden_ratio / 2 ),
         (-0.5             , -golden_ratio / 2,  0.0              )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         (-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             , -0.5              ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( 0.0             , -0.5             , -golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         (-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         (-0.5             ,  golden_ratio / 2,  0.0              )),
        ((-golden_ratio / 2,  0.0             ,  0.5              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 )),
        ((-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              )),
        ((-0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.5             , -golden_ratio / 2,  0.0              ),
         ( 0.0             , -0.5             ,  golden_ratio / 2 )),
        ((-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 )),
        ((-0.5             ,  golden_ratio / 2,  0.0              ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              )),
        (( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             , -0.5              )),
        (( 0.0             , -0.5             , -golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             , -0.5              ),
         ( 0.5             , -golden_ratio / 2,  0.0              )),
        (( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             ,  0.5              ),
         ( 0.0             ,  0.5             ,  golden_ratio / 2 )),
        (( 0.0             , -0.5             ,  golden_ratio / 2 ),
         ( 0.5             , -golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.0             ,  0.5             , -golden_ratio / 2 ),
         ( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              )),
        (( 0.0             ,  0.5             ,  golden_ratio / 2 ),
         ( golden_ratio / 2,  0.0             ,  0.5              ),
         ( 0.5             ,  golden_ratio / 2,  0.0              )),
        (( 0.5             , -golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             , -0.5              ),
         ( golden_ratio / 2,  0.0             ,  0.5              )),
        (( 0.5             ,  golden_ratio / 2,  0.0              ),
         ( golden_ratio / 2,  0.0             ,  0.5              ),
         ( golden_ratio / 2,  0.0             , -0.5              ))
    }

    def __init__(self, frequency: int = 0, hollow: bool = False, thinness_factor: int = 0):
        self.w = int(frequency)
        self.t = int(thinness_factor)
        self.f = self.faces.copy()
        self._tesselate()
        self._project()
        if hollow:
            self._hollow()

    def _hollow(self) -> None:
        """
        This function hollows the geodesic sphere.
        """
        for face in self.f.copy():
            v1, v2, v3 = face
            center_x, center_y, center_z = (v1[0] + v2[0] + v3[0]) / 3, (v1[1] + v2[1] + v3[1]) / 3, (v1[2] + v2[2] + v3[2]) / 3
            shrunken_face = [0.0, 0.0, 0.0]
            for i, v in enumerate(face):
                x, y, z = (v[0] + center_x) / 2, (v[1] + center_y) / 2, (v[2] + center_z) / 2
                for _ in range(self.t):
                    x, y, z = (v[0] + x) / 2, (v[1] + y) / 2, (v[2] + z) / 2
                shrunken_face[i] = (x, y, z)
            self.f.remove(face)
            face1 = (v1, v2, shrunken_face[1])
            face2 = (v1, shrunken_face[1], shrunken_face[0])
            face3 = (v2, v3, shrunken_face[2])
            face4 = (v2, shrunken_face[2], shrunken_face[1])
            face5 = (v3, v1, shrunken_face[0])
            face6 = (v3, shrunken_face[0], shrunken_face[2])
            reversed_faces = [face1[::-1], face2[::-1], face3[::-1], face4[::-1], face5[::-1], face6[::-1]]
            self.f.update([face1, face2, face3, face4, face5, face6, *reversed_faces])
        return None

    def _project(self) -> None:
        """
        This function projects each vertex of each face onto the surface of a sphere of radius 1.
        """
        for face in self.f.copy():
            projected_face = [(), (), ()]
            for i, v in enumerate(face):
                m = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
                projected_face[i] = (v[0] / m, v[1] / m, v[2] / m)
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
                mid_point1 = ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2)
                mid_point2 = ((v2[0] + v3[0]) / 2, (v2[1] + v3[1]) / 2, (v2[2] + v3[2]) / 2)
                mid_point3 = ((v3[0] + v1[0]) / 2, (v3[1] + v1[1]) / 2, (v3[2] + v1[2]) / 2)
                face1 = (v1, mid_point1, mid_point3)
                face2 = (mid_point1, v2, mid_point2)
                face3 = (mid_point2, v3, mid_point3)
                face4 = (mid_point1, mid_point2, mid_point3)
                self.f.remove(face)
                self.f.update([face1, face2, face3, face4])
        return None

    def gen_stl_file(self, name: str) -> None:
        if name.endswith('.stl'):
            solid_name = name.strip('.stl')
            file_name = name
        else:
            solid_name = name
            file_name = f"{name}.stl"
        with open(file_name, 'w') as file:
            file.write(f"solid {solid_name}\n")
            for face in self.f:
                v1, v2, v3 = face
                center_x, center_y, center_z = (v1[0] + v2[0] + v3[0]) / 3, (v1[1] + v2[1] + v3[1]) / 3, (v1[2] + v2[2] + v3[2]) / 3
                magnitude = sqrt(center_x**2 + center_y**2 + center_z**2)
                normal_x, normal_y, normal_z = (center_x / magnitude, center_y / magnitude, center_z / magnitude)
                file.write(f"facet normal {normal_x} {normal_y} {normal_z}\n")
                file.write('\touter loop\n')
                for vertex in face:
                    file.write(f"\t\tvertex {vertex[0]} {vertex[1]} {vertex[2]}\n")
                file.write('\tendloop\n')
                file.write('endfacet\n')
            file.write(f"endsolid {solid_name}")
        return None

    def plot(self) -> None:
        ax = axes(projection='3d')
        ax.add_collection3d(Poly3DCollection(verts=list(self.f), facecolors='white', edgecolor='black'))
        ax.axis('off')
        ax.grid(visible=None)
        ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
        ax.set_aspect('equal', 'box')
        show()
        return None


if __name__ == '__main__':
    geodesic_sphere = GeodesicSphere(frequency=1, hollow=True, thinness_factor=1)
    geodesic_sphere.plot()
    geodesic_sphere.gen_stl_file('geodesic_sphere')
