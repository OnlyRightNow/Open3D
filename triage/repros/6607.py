"""https://github.com/isl-org/Open3D/issues/6607
Writing a >100M point tensor point cloud to binary PCD fails with "ValueError: vector too long".
Expected: write succeeds and the file reads back with all points.
Actual (0.20): binary PCD writer streams in chunks (t/io/file_format/FilePCD.cpp); write+read succeed.
Verdict: FIXED   (needs ~9 GB RAM and ~3.3 GB disk)
"""
import os
import tempfile
import numpy as np
import open3d as o3d

N = 100_000_000
pcdt = o3d.t.geometry.PointCloud()
pcdt.point.positions = o3d.core.Tensor(np.random.rand(N, 3).astype(np.float32))
pcdt.point.intensities = o3d.core.Tensor(np.random.rand(N, 1).astype(np.float32))
pcdt.point.instance_key = o3d.core.Tensor(np.random.rand(N, 1))
pcdt.point.class_key = o3d.core.Tensor(np.random.rand(N, 1))
with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(__file__))) as td:
    path = os.path.join(td, "big.pcd")
    try:
        ok = o3d.t.io.write_point_cloud(path, pcdt, write_ascii=False)
    except Exception as e:  # reported failure mode
        print("BUG REPRODUCED: write raised", type(e).__name__, e)
        raise SystemExit(0)
    del pcdt
    print("write returned", ok, "file size GB", os.path.getsize(path) / 1e9)
    back = o3d.t.io.read_point_cloud(path)
    n = back.point.positions.shape[0]
    print("read back points:", n, "attrs:", sorted(back.point))
    print("OK: 100M-point binary PCD written and read back" if ok and n == N else
          "BUG REPRODUCED: write/read mismatch")
