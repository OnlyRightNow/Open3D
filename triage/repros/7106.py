"""https://github.com/isl-org/Open3D/issues/7106 - orient_normals_consistent_tangent_plane does not accept lambda
Expected: a usable keyword for the lambda parameter. Actual (0.18): kwarg named `lambda` (Python keyword).
Verdict on 0.20: FIXED (renamed to lambda_penalty by PR #7096)."""
import numpy as np, open3d as o3d
p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(100, 3))); p.estimate_normals()
try:
    p.orient_normals_consistent_tangent_plane(k=5, lambda_penalty=0.1); print("OK: lambda_penalty keyword accepted")
except TypeError as e:
    print("BUG REPRODUCED:", e)
