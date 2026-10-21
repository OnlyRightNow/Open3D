"""https://github.com/isl-org/Open3D/issues/6055
Too large bounds in create_from_triangle_mesh_within_bounds.
Expected: voxels restricted to [min_bound, max_bound] = [0,10]^3.
Actual: a sphere extending past the bounds yields voxels from -3 to 13; grid indices are never clamped.
Verdict: CONFIRMED (cpp/open3d/geometry/VoxelGridFactory.cpp: VoxelGrid::CreateFromTriangleMeshWithinBounds)."""
import numpy as np
import open3d as o3d
s = o3d.geometry.TriangleMesh.create_sphere(radius=8).translate((5, 5, 5))
g = o3d.geometry.VoxelGrid.create_from_triangle_mesh_within_bounds(s, 0.1, np.zeros(3), np.full(3, 10.0))
lo, hi = g.get_min_bound(), g.get_max_bound()
if (lo < -1e-9).any() or (hi > 10 + 1e-9).any():
    print("BUG REPRODUCED: voxel grid bounds", lo, hi, "exceed [0,10]")
else:
    print("OK: within bounds")
