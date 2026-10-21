"""https://github.com/isl-org/Open3D/issues/6458
Errors with registration_icp and registration_generalized_icp.
Reported (0.17): registration_icp + ColoredICP estimator segfaults; registration_icp + GICP estimator errors
on missing covariances.
On 0.20: GICP estimator works through registration_icp; ColoredICP without colors raises a clean RuntimeError,
with colors+normals it converges. registration_generalized_icp only accepting the GICP estimator is by its signature.
Verdict: FIXED."""
import subprocess, sys
code = r'''
import numpy as np, open3d as o3d
R = o3d.pipelines.registration
m = o3d.geometry.TriangleMesh.create_sphere(); m.compute_vertex_normals()
s = m.sample_points_uniformly(2000); t = o3d.geometry.PointCloud(s).translate((0.01, 0, 0))
print("gicp", R.registration_icp(s, t, 0.05, np.eye(4), R.TransformationEstimationForGeneralizedICP()).fitness)
try:
    R.registration_icp(s, t, 0.05, np.eye(4), R.TransformationEstimationForColoredICP())
except RuntimeError:
    print("colored-no-colors: clean error")
'''
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
print(r.stdout.strip())
print("OK: no crash, exit code 0" if r.returncode == 0 else "BUG REPRODUCED: exit code %d" % r.returncode)
