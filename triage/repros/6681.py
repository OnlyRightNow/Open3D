"""https://github.com/isl-org/Open3D/issues/6681
fill_holes: wrong triangle direction.
Expected: triangles added by t.geometry.TriangleMesh.fill_holes() are wound consistently
with the surrounding mesh (outward normals).
Actual: the cap filling a hole at the top of an outward-oriented sphere points inward
(shared edges traversed in the same direction by both neighbours). Root cause:
cpp/open3d/t/geometry/TriangleMesh.cpp TriangleMesh::FillHoles (vtkFillHolesFilter output
is not re-oriented; PR #6816 proposes vtkPolyDataNormals with ConsistencyOn).
Verdict: CONFIRMED."""
from collections import Counter
import numpy as np
import open3d as o3d

m = o3d.geometry.TriangleMesh.create_sphere(1.0, 20)
T, V = np.asarray(m.triangles), np.asarray(m.vertices)
keep = V[T].mean(1)[:, 2] < 0.7  # cut a hole at the top
m.triangles = o3d.utility.Vector3iVector(T[keep])
m.remove_unreferenced_vertices()
f = o3d.t.geometry.TriangleMesh.from_legacy(m).fill_holes().to_legacy()
f.merge_close_vertices(1e-9)
T = np.asarray(f.triangles)
E = np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]])
dup = sum(k > 1 for k in Counter(map(tuple, E)).values())
if dup:
    print(f"BUG REPRODUCED: {dup} edges traversed twice in the same direction (filled cap flipped)")
else:
    print("OK: filled triangles are consistently oriented")
