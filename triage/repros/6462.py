"""https://github.com/isl-org/Open3D/issues/6462
Bug in self-intersection test of triangle mesh.
Expected: two nearly-coplanar triangles that are disjoint (separated by >1.2 units in-plane)
are not reported as self-intersecting.
Actual: is_self_intersecting() is True and get_self_intersecting_triangles() returns [[0, 1]]
(data = reporter's v_array.npy/t_array.npy, inlined). Numerical robustness issue in the
near-coplanar branch. Root cause: cpp/open3d/geometry/IntersectionTest.cpp
IntersectionTest::TriangleTriangle3d. Verdict: CONFIRMED."""
import numpy as np
import open3d as o3d

v = np.array([[103.19999694824219, 310.79998779296875, 171.521728515625],
              [102.25, 310.79998779296875, 174.0],
              [103.19999694824219, 312.0, 171.9130401611328],
              [103.19999694824219, 313.20001220703125, 172.30435180664062],
              [102.4000015258789, 312.0, 174.0],
              [102.55000305175781, 313.20001220703125, 174.0]])
m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(v),
                              o3d.utility.Vector3iVector(np.array([[0, 1, 2], [3, 4, 5]], np.int32)))
# Triangle 0 has y <= 312, triangle 1 has y >= 312, and at y == 312 their z differ (171.9 vs 174).
if m.is_self_intersecting():
    print("BUG REPRODUCED: disjoint triangles flagged as intersecting:",
          np.asarray(m.get_self_intersecting_triangles()).tolist())
else:
    print("OK: not self-intersecting")
