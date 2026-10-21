"""https://github.com/isl-org/Open3D/issues/5301 - VoxelGrid cannot be created from Octree
Expected: many voxels. Actual: 1 voxel. Verdict on 0.20: CONFIRMED. Root cause: geometry/VoxelGrid.cpp
VoxelGrid::CreateFromOctree does voxel_size_ = min(voxel_size_, leaf size) with default voxel_size_ = 0, so all
indices are floor(x/0) -> same voxel."""
import open3d as o3d
pc = o3d.geometry.TriangleMesh.create_sphere().sample_points_uniformly(20000)
oc = o3d.geometry.Octree(max_depth=6); oc.convert_from_point_cloud(pc)
vg = oc.to_voxel_grid(); n = len(vg.get_voxels())
print(f"BUG REPRODUCED: to_voxel_grid gave {n} voxel(s), voxel_size={vg.voxel_size}" if n <= 1 else f"OK: {n} voxels")
