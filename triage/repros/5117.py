"""https://github.com/isl-org/Open3D/issues/5117 - TriangleMesh.is_self_intersecting returns wrong result
Expected: False (the two triangles do not intersect; independent edge/triangle test confirms, and the rotated
mesh returns False). Actual: True. Verdict on 0.20: CONFIRMED. One vertex of T1 lies ~1e-10 from T2's plane;
the Moller NoDivTriTriIsect epsilon/coplanarity handling (geometry/IntersectionTest.cpp TriangleTriangle3d) misreports."""
import numpy as np, open3d as o3d
V = [[0., 0.13918686, 1.], [0., 0., 1.1270161], [1., 0., 1.0284119], [1., 1.1269569, 0.], [1., 0.03113556, 1.], [2., 1.0189056, 0.]]
m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(V), o3d.utility.Vector3iVector([[0, 1, 2], [3, 4, 5]]))
a = m.is_self_intersecting(); s = np.sqrt(.5)
b = m.rotate(np.array([[1, 0, 0], [0, s, s], [0, -s, s]]), center=(0, 0, 0)).is_self_intersecting()
print(f"BUG REPRODUCED: is_self_intersecting={a}, after rotation={b}" if a != b else f"OK: {a} / {b}")
