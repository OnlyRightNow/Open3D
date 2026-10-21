"""https://github.com/isl-org/Open3D/issues/5360 - mesh smoothing creates nan
Expected: no NaN after filter_smooth_taubin/laplacian on a mesh with unreferenced vertices.
Actual (0.15-0.19): NaN vertices. Verdict on 0.20: FIXED."""
import numpy as np, open3d as o3d
m = o3d.geometry.TriangleMesh.create_sphere()
m.vertices = o3d.utility.Vector3dVector(np.vstack([np.asarray(m.vertices), [[5, 5, 5]]]))  # unreferenced vertex
bad = [n for n, f in [("taubin", lambda: m.filter_smooth_taubin(2)), ("laplacian", lambda: m.filter_smooth_laplacian(2))]
       if np.isnan(np.asarray(f().vertices)).any()]
print("BUG REPRODUCED: NaN in " + ",".join(bad) if bad else "OK: no NaN after smoothing mesh with unreferenced vertex")
