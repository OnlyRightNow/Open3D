"""https://github.com/isl-org/Open3D/issues/7070 - rgbd_odometry.py segfault (numpy>=2 with 0.18)
Expected: create_from_rgbd_image + compute_rgbd_odometry run with numpy 2.x. Actual (0.18): segfault.
Verdict on 0.20: FIXED (runs in subprocess with numpy 2.x, exit code 0)."""
import subprocess, sys
code = '''
import open3d as o3d, numpy as np
c=o3d.geometry.Image((np.random.rand(480,640,3)*255).astype(np.uint8)); d=o3d.geometry.Image((np.random.rand(480,640)*2000+500).astype(np.uint16))
r=o3d.geometry.RGBDImage.create_from_color_and_depth(c,d)
K=o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
o3d.geometry.PointCloud.create_from_rgbd_image(r,K)
o3d.pipelines.odometry.compute_rgbd_odometry(r,r,K,np.identity(4),o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(),o3d.pipelines.odometry.OdometryOption())
print("numpy", np.__version__)
'''
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
print(f"OK: exit 0 ({r.stdout.strip()})" if r.returncode == 0 else f"BUG REPRODUCED: exit code {r.returncode}")
