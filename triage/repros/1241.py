"""https://github.com/isl-org/Open3D/issues/1241
voxel_down_sample_and_trace does not return the full index of points.
Expected: a mapping from every original point to its voxel. Actual on 0.8: only Mx8 cubic ids.
Verdict: FIXED on 0.20 (third return value lists original indices per voxel, covering all points).
"""
import numpy as np, open3d as o3d
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(1000, 3)))
down, cubic, idx = pcd.voxel_down_sample_and_trace(0.2, pcd.get_min_bound(), pcd.get_max_bound())
allidx = sorted(i for v in idx for i in v)
print("voxels", len(down.points), "cubic", np.asarray(cubic).shape, "traced", len(allidx))
print("OK: every original point traced to a voxel" if allidx == list(range(1000)) else "BUG REPRODUCED")
