"""https://github.com/isl-org/Open3D/issues/6111
create_from_triangle_mesh only judges the intersection with the triangle edge, not the triangle surface.
Expected: all surface samples of a box fall in occupied voxels (voxel_size 0.005).
Actual on 0.20: 100% coverage. Verdict: FIXED."""
import numpy as np
import open3d as o3d
b = o3d.geometry.TriangleMesh.create_box()
g = o3d.geometry.VoxelGrid.create_from_triangle_mesh(b, 0.005)
cov = np.mean(g.check_if_included(b.sample_points_uniformly(20000).points))
print(("OK: coverage %.3f" % cov) if cov == 1.0 else "BUG REPRODUCED: coverage %.3f" % cov)
