"""https://github.com/isl-org/Open3D/issues/2766
VoxelGrid.create_from_point_cloud_within_bounds behaviour.
Expected: only points inside [min_bound, max_bound] are voxelized. Actual: max_bound is ignored (only used for
an overflow check); points outside the bounds create voxels with out-of-range/negative indices.
(The reporter's scaling complaint itself is expected: a larger surface needs more samples.)
Verdict: CONFIRMED (VoxelGrid::CreateFromPointCloudWithinBounds in cpp/open3d/geometry/VoxelGridFactory.cpp).
"""
import numpy as np, open3d as o3d
p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.array([[0.1, 0.1, 0.1], [5, 5, 5], [-3, 0, 0]])))
vg = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(p, 0.25, [-0.5] * 3, [0.5] * 3)
idx = [v.grid_index.tolist() for v in vg.get_voxels()]
print("voxel indices:", idx, "(valid range 0..3)")
bad = [i for i in idx if min(i) < 0 or max(i) > 3]
print("BUG REPRODUCED: out-of-bounds points voxelized: %s" % bad if bad else "OK: only in-bounds voxels")
