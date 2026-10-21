"""https://github.com/isl-org/Open3D/issues/6642
Writing custom attributes works for .ply files but fails for .pcd files.
Expected: custom attribute (intensities) survives a .pcd write/read round trip.
Actual on 0.13: attribute missing. On 0.20 it round-trips correctly. Verdict: FIXED."""
import os, tempfile
import numpy as np
import open3d as o3d

d = tempfile.mkdtemp()
pcd = o3d.t.geometry.PointCloud(o3d.core.Tensor(np.random.rand(100, 3), dtype=o3d.core.float32))
inten = np.random.rand(100, 1).astype(np.float32)
pcd.point["intensities"] = o3d.core.Tensor(inten)
p = os.path.join(d, "t.pcd")
o3d.t.io.write_point_cloud(p, pcd)
r = o3d.t.io.read_point_cloud(p)
if "intensities" in r.point and np.allclose(r.point.intensities.numpy(), inten):
    print("OK: custom attribute round-trips through .pcd")
else:
    print(f"BUG REPRODUCED: attribute lost: {r}")
