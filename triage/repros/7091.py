"""https://github.com/isl-org/Open3D/issues/7091 - Merging empty tensor point cloud fails
Expected: t.PointCloud() + pcd == pcd (like legacy). Actual: IndexError (_Map_base::at) / RuntimeError missing positions.
Verdict on 0.20: CONFIRMED. Root cause: t/geometry/PointCloud.cpp PointCloud::Append calls GetPointPositions() on empty cloud."""
import numpy as np, open3d as o3d
e = o3d.t.geometry.PointCloud(); p = o3d.t.geometry.PointCloud(o3d.core.Tensor(np.random.rand(2, 3).astype(np.float32)))
errs = []
for name, f in [("empty+p", lambda: e + p), ("p+empty", lambda: p + e)]:
    try: f()
    except Exception as ex: errs.append(f"{name}: {type(ex).__name__}")
print("BUG REPRODUCED: " + "; ".join(errs) if errs else "OK: merge with empty cloud works")
