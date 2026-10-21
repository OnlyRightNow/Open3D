"""https://github.com/isl-org/Open3D/issues/5717
printing t.pipelines.registration.RegistrationResult throws RuntimeError
Expected: print(result) works. Actual (0.16): RuntimeError: invalid type specifier.
"""
import numpy as np, open3d as o3d
pts = np.random.rand(500, 3).astype(np.float32)
src = o3d.t.geometry.PointCloud(o3d.core.Tensor(pts))
dst = o3d.t.geometry.PointCloud(o3d.core.Tensor(pts + 0.01))
res = o3d.t.pipelines.registration.icp(src, dst, 0.07)
try:
    print(res)
    print("OK: printing t RegistrationResult works")
except Exception as e:
    print("BUG REPRODUCED:", type(e).__name__, e)
