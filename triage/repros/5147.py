"""https://github.com/isl-org/Open3D/issues/5147
create_from_depth_image doesn't scale when dtype=np.float32.
Expected: float32 depth is divided by depth_scale like uint16. Actual on 0.15: not scaled.
Verdict: FIXED on 0.20 (float32 and uint16 give identical z; depth_trunc applies).
"""
import numpy as np, open3d as o3d
K = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
z = {}
for dt in (np.uint16, np.float32):
    d = o3d.geometry.Image(np.full((480, 640), 12345, dtype=dt))
    p = o3d.geometry.PointCloud.create_from_depth_image(d, K, depth_scale=10000.0, depth_trunc=100.0)
    z[dt] = np.asarray(p.points)[:, 2].max()
    nt = len(o3d.geometry.PointCloud.create_from_depth_image(d, K, depth_scale=10000.0, depth_trunc=1.0).points)
    print(dt.__name__, "max z", z[dt], "points with depth_trunc=1:", nt)
ok = abs(z[np.float32] - 1.2345) < 1e-4 and abs(z[np.uint16] - 1.2345) < 1e-4
print("OK: float32 depth scaled by depth_scale" if ok else "BUG REPRODUCED: float32 not scaled")
