"""https://github.com/isl-org/Open3D/issues/6993 - Segfault in o3d.utility.Vector3dVector() (numpy 2 + 0.17/0.18)
Expected: Vector3dVector(np.ndarray) works. Actual: segfault. Verdict on 0.20: FIXED."""
import subprocess, sys
r = subprocess.run([sys.executable, "-c", "import open3d as o3d,numpy as np;v=o3d.utility.Vector3dVector(np.random.rand(5,3));print(len(v),np.__version__)"], capture_output=True, text=True)
print(f"OK: {r.stdout.strip()} (len, numpy)" if r.returncode == 0 else f"BUG REPRODUCED: exit code {r.returncode}")
