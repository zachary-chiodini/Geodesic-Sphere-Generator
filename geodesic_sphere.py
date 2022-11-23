from math import sqrt
from matplotlib.pyplot import axes, savefig, show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Union


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

    def __init__(self, frequency: int = 0, hollow_factor: int = 0, thickness_factor: Union[float, int] = 0):
        if not (isinstance(frequency, int) and (frequency >= 0)):
            raise ValueError('Frequency must be a positive integer.')
        if not (isinstance(hollow_factor, Union[float, int]) and (0 <= hollow_factor <= 100)):
            raise ValueError('Hollow factor must be a number between 0 and 100 inclusive.')
        if not (isinstance(thickness_factor, Union[float, int]) and (0 <= thickness_factor <= 100)):
            raise ValueError('Thickness factor must be a number between 0 and 100 inclusive.')
        self.w = frequency
        self.h = hollow_factor / 100
        self.t = (100 - thickness_factor) / 100
        self.f = self.faces.copy()
        self._tesselate()
        self._project()
        if hollow_factor:
            self._hollow()

    def _hollow(self) -> None:
        """
        This function hollows the geodesic sphere, giving it a kind of skeletal structure.
        """
        for face in self.f.copy():
            # First find the center of the triangle.
            v1, v2, v3 = face
            center_point = ((v1[0] + v2[0] + v3[0]) / 3, (v1[1] + v2[1] + v3[1]) / 3, (v1[2] + v2[2] + v3[2]) / 3)
            # The hollowed area must exist at the center point and extend to all three vertices as a shrunken void triangle.
            # The range of the shrunken void triangle is from the middle point to each vertex in the outer triangle.
            # Below are 3 vectors pointing from the center point to each vertex on the face.
            # These will be used to make three 3D lines, upon which the center point is at 0 and each vertex is at 1.
            direction1 = ((v1[0] - center_point[0]), (v1[1] - center_point[1]), (v1[2] - center_point[2]))
            direction2 = ((v2[0] - center_point[0]), (v2[1] - center_point[1]), (v2[2] - center_point[2]))
            direction3 = ((v3[0] - center_point[0]), (v3[1] - center_point[1]), (v3[2] - center_point[2]))
            # The hollowness factor h is a float between 0 and 1 inclusive. 
            # The vertices of the shrunken void triangle are calculated from the equation of a 3D line at point h for each vertex of the larger triangle.
            # This creates a smaller "shrunken" triangle within the initial larger triangle.
            shrunken_face = [
				(center_point[0] + self.h * direction1[0], center_point[1] + self.h * direction1[1], center_point[2] + self.h * direction1[2]),
				(center_point[0] + self.h * direction2[0], center_point[1] + self.h * direction2[1], center_point[2] + self.h * direction2[2]),
				(center_point[0] + self.h * direction3[0], center_point[1] + self.h * direction3[1], center_point[2] + self.h * direction3[2])
			]
            self.f.remove(face)
            # Create the skeleton of the hollowed object from the vertices of the outer triangle and inner shrunken void triangle.
            # The space between the outer triangle and inner triangle is filled by inserting two new triangles on each side of the inner triangle.
            # This creates 6 new faces. These new faces are outward facing.
            outer_face1 = (v1, v2, shrunken_face[1])
            outer_face2 = (v1, shrunken_face[1], shrunken_face[0])
            outer_face3 = (v2, v3, shrunken_face[2])
            outer_face4 = (v2, shrunken_face[2], shrunken_face[1])
            outer_face5 = (v3, v1, shrunken_face[0])
            outer_face6 = (v3, shrunken_face[0], shrunken_face[2])
            self.f.update({outer_face1, outer_face2, outer_face3, outer_face4, outer_face5, outer_face6})
            # Create the inward facing triangles by reversing the order of the vertices in each outward facing triangle.
            inner_face1 = tuple(tuple(p * self.t for p in v) for v in outer_face1[::-1])
            inner_face2 = tuple(tuple(p * self.t for p in v) for v in outer_face2[::-1])
            inner_face3 = tuple(tuple(p * self.t for p in v) for v in outer_face3[::-1])
            inner_face4 = tuple(tuple(p * self.t for p in v) for v in outer_face4[::-1])
            inner_face5 = tuple(tuple(p * self.t for p in v) for v in outer_face5[::-1])
            inner_face6 = tuple(tuple(p * self.t for p in v) for v in outer_face6[::-1])
            self.f.update({inner_face1, inner_face2, inner_face3, inner_face4, inner_face5, inner_face6})
            # If the scaling factor t is less than one, the inward facing vertices were scaled down by t, and
            # the space between the outward and inward facing triangles must now be filled with 6 new triangles (2 for each side).
            if self.t < 1:
                v1, v2, v3 = shrunken_face
                inner_shrunken_face = ((v1[0] * self.t, v1[1] * self.t, v1[2] * self.t),
                                       (v2[0] * self.t, v2[1] * self.t, v2[2] * self.t),
                                       (v3[0] * self.t, v3[1] * self.t, v3[2] * self.t))
                side_face1 = (shrunken_face[0], shrunken_face[1], inner_shrunken_face[0])
                side_face2 = (shrunken_face[1], inner_shrunken_face[1], inner_shrunken_face[0])
                side_face3 = (shrunken_face[1], shrunken_face[2], inner_shrunken_face[1])
                side_face4 = (shrunken_face[2], inner_shrunken_face[2], inner_shrunken_face[1])
                
                side_face5 = (shrunken_face[2], shrunken_face[0], inner_shrunken_face[2])
                side_face6 = (shrunken_face[0], inner_shrunken_face[0], inner_shrunken_face[2])
                self.f.update({side_face1, side_face2, side_face3, side_face4, side_face5, side_face6})
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
        (It turns each triangle into a triforce symbol with the center triangle filled.)
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
                self.f.update({face1, face2, face3, face4})
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
        ax.set(xlim=(-0.64, 0.64), ylim=(-0.64, 0.64), zlim=(-0.64, 0.64))
        ax.set_aspect('equal', 'box')
        savefig('geodesic_sphere.png', bbox_inches='tight')
        show()
        return None


if __name__ == '__main__':
    geodesic_sphere = GeodesicSphere(frequency=0, hollow_factor=61.8, thickness_factor=10)
    geodesic_sphere.plot()
    geodesic_sphere.gen_stl_file('geodesic_sphere')
