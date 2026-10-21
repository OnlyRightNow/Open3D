"""https://github.com/isl-org/Open3D/issues/7201
Combining legacy point clouds with `+` is slower than numpy concatenation + re-wrap.
Expected: pcd1 + pcd2 at least as fast as numpy round trip.
Actual (0.20, 2M pts): `+` ~0.2-0.6 s vs numpy ~0.6-2.5 s, i.e. `+` is faster.
Verdict: FIXED
"""
import time
import numpy as np
import open3d as o3d

V = o3d.utility.Vector3dVector
a, b = np.random.rand(2_000_000, 3), np.random.rand(2_000_000, 3)
p1, p2 = o3d.geometry.PointCloud(V(a)), o3d.geometry.PointCloud(V(b))
p1.colors, p2.colors = V(a), V(b)
t = time.perf_counter(); p = p1 + p2; t_plus = time.perf_counter() - t
t = time.perf_counter()
q = o3d.geometry.PointCloud(V(np.concatenate([np.asarray(p1.points), np.asarray(p2.points)])))
q.colors = V(np.concatenate([np.asarray(p1.colors), np.asarray(p2.colors)]))
t_np = time.perf_counter() - t
t = time.perf_counter(); p1.transform(np.eye(4)); t_tf = time.perf_counter() - t
print(f"pcd1+pcd2: {t_plus:.3f}s  numpy concat+wrap: {t_np:.3f}s  transform: {t_tf:.3f}s")
if t_plus > 2 * t_np:
    print("BUG REPRODUCED: legacy PointCloud + is much slower than numpy round trip")
else:
    print("OK: legacy PointCloud + is not slower than the numpy round trip")
