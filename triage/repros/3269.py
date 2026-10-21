"""https://github.com/isl-org/Open3D/issues/3269
Octree.to_voxel_grid() produces an (almost) empty VoxelGrid.
Expected: one voxel per occupied octree leaf. Actual: 'VoxelGrid with 1 voxels' (voxel_size stays 0).
Verdict: CONFIRMED (VoxelGrid::CreateFromOctree in cpp/open3d/geometry/VoxelGrid.cpp: voxel_size_=min(voxel_size_, ...) with voxel_size_ initialised to 0).
"""
import numpy as np, open3d as o3d
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(1000, 3)))
oc = o3d.geometry.Octree(max_depth=6)
oc.convert_from_point_cloud(pcd, size_expand=0.01)
vg = oc.to_voxel_grid()
n = len(vg.get_voxels())
print(vg, "voxel_size", vg.voxel_size)
print("BUG REPRODUCED: octree with 1000 leaves -> %d voxel(s)" % n if n <= 1 else "OK: %d voxels" % n)
