"""https://github.com/isl-org/Open3D/issues/6043
Tensor API can't write .pcd files beyond 2.1 GB.
Expected: o3d.t.io.write_point_cloud writes 2**31//12+1 float32 points (just over 2 GiB).
Actual on 0.20: writes 2147483832 bytes and reads back all points. Needs ~5 GB RAM and 2.2 GB disk.
Verdict: FIXED."""
import os, tempfile
import numpy as np
import open3d as o3d
N = 2**31 // 12 + 1
pos = np.zeros((N, 3), np.float32); pos[-1] = [1, 2, 3]
pc = o3d.t.geometry.PointCloud(); pc.point.positions = o3d.core.Tensor.from_numpy(pos)
p = os.path.join(tempfile.mkdtemp(), "big.pcd")
try:
    ok = o3d.t.io.write_point_cloud(p, pc)
    r = o3d.t.io.read_point_cloud(p)
    good = ok and r.point.positions.shape[0] == N and np.allclose(r.point.positions[-1].numpy(), [1, 2, 3])
    print("OK: wrote %d bytes and read back" % os.path.getsize(p) if good else "BUG REPRODUCED: write/read mismatch")
except Exception as e:
    print("BUG REPRODUCED: %s" % e)
finally:
    if os.path.exists(p): os.remove(p)
