"""https://github.com/isl-org/Open3D/issues/6088
Negative value returned by open3d.geometry.VoxelGrid.get_voxel().
Expected: points inside the grid map to non-negative indices matching Voxel.grid_index.
Actual on 0.20: in-grid points give indices in [0, max grid_index]. The report queried the unscaled positions
after scaling the cloud, so out-of-grid points correctly got negative indices (not a bug). Verdict: FIXED (not reproducible)."""
import numpy as np
import open3d as o3d
pts = np.random.rand(200, 3) * 3
g = o3d.geometry.VoxelGrid.create_from_point_cloud(o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pts)), 0.05)
idx = np.array([g.get_voxel(p) for p in pts])
gi = {tuple(v.grid_index) for v in g.get_voxels()}
ok = idx.min() >= 0 and all(tuple(i) in gi for i in idx)
print("OK: all indices non-negative and match grid_index" if ok else "BUG REPRODUCED: idx min %d" % idx.min())
