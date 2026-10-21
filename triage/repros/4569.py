"""https://github.com/isl-org/Open3D/issues/4569
VoxelGrid.create_from_point_cloud_within_bounds does not care for bounds.
Expected: only points inside [min_bound, max_bound] are voxelized.
Actual: every point is voxelized; bounds only set the origin. Root cause:
cpp/open3d/geometry/VoxelGridFactory.cpp VoxelGrid::CreateFromPointCloudWithinBounds
(no bounds check in the point loop). Verdict: CONFIRMED."""
import numpy as np
import open3d as o3d

pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(2000, 3)))
vg = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(
    pc, 0.1, np.array([0., 0, 0]), np.array([0.5, 0.5, 0.5]))
idx = np.array([v.grid_index for v in vg.get_voxels()])
if idx.max() >= 5:
    print(f"BUG REPRODUCED: voxels outside bounds exist (max grid index {idx.max(0).tolist()}, expected <= 4)")
else:
    print("OK: voxels limited to bounds")
