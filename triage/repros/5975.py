"""https://github.com/isl-org/Open3D/issues/5975
QH5 qhull precision error (qh_merge_twisted) with normal orientation.
Expected: orient_normals_consistent_tangent_plane handles degenerate input without a Qhull error.
Actual: on a planar grid it raises RuntimeError "QH6239 Qhull precision error ... cospherical" (reporter's file
with the QH5 qh_merge_twisted error is not available; same code path).
Verdict: CONFIRMED (cpp/open3d/geometry/Qhull.cpp: Qhull::ComputeDelaunayTetrahedralization runs "d Qbb Qt" without QJ/Qz)."""
import numpy as np
import open3d as o3d
g = np.stack(np.meshgrid(np.linspace(0, 1, 150), np.linspace(0, 1, 150)), -1).reshape(-1, 2)
pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.c_[g, np.zeros(len(g))]))
pc.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(30))
try:
    pc.orient_normals_consistent_tangent_plane(30)
    print("OK: no Qhull error")
except RuntimeError as e:
    print("BUG REPRODUCED: %s" % str(e).splitlines()[0][:120])
