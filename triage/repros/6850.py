"""https://github.com/isl-org/Open3D/issues/6850 - Segfault with IntVector(np.array([0,0,0]))
Expected: no crash (TypeError or conversion). Actual (0.18 dev): segfault. Verdict on 0.20: FIXED (raises TypeError
'Format mismatch'; int32 arrays work; alpha shape with alpha=0 also no longer crashes)."""
import subprocess, sys
codes = {"int64": "import open3d as o3d,numpy as np;o3d.utility.IntVector(np.array([0,0,0]))",
         "int32": "import open3d as o3d,numpy as np;print(o3d.utility.IntVector(np.array([0,0,0],dtype=np.int32)))",
         "alpha0": "import open3d as o3d,numpy as np;p=o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(100,3)));o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(p,0.0)"}
rc = {k: subprocess.run([sys.executable, "-c", c], capture_output=True).returncode for k, c in codes.items()}
crash = [k for k, v in rc.items() if v < 0]
print(f"BUG REPRODUCED: crash in {crash}" if crash else f"OK: no segfault, exit codes {rc} (int64 -> TypeError exit 1)")
