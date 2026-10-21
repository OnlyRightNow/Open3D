"""https://github.com/isl-org/Open3D/issues/4845
t.geometry.PointCloud.create_from_depth_image crashes with with_normals=True and non-identity extrinsics.
Expected: point cloud. Actual: RuntimeError 'Tensor has dtype Float64, but is expected to have Float32' from Matmul.
Verdict: CONFIRMED (CreatePointCloudWithNormals in cpp/open3d/t/geometry/PointCloud.cpp: extrinsics are cast to
Float64 in CreateFromDepthImage, then Float32 vertex_list.Matmul(cam_to_world) mismatches).
"""
import numpy as np, open3d as o3d
ex = np.eye(4, dtype=np.float32); ex[0, 3] = 1.0
try:
    o3d.t.geometry.PointCloud.create_from_depth_image(
        o3d.t.geometry.Image(o3d.core.Tensor(np.ones((2, 2), np.uint16))),
        o3d.core.Tensor(np.eye(3, dtype=np.float32)), o3d.core.Tensor(ex), with_normals=True)
    print("OK: no error")
except RuntimeError as e:
    import re; print("BUG REPRODUCED:", re.search(r"Tensor has dtype \w+, but is expected to have \w+", str(e)).group(0) if "dtype" in str(e) else str(e)[:200])
