"""https://github.com/isl-org/Open3D/issues/5516
Error in creating voxelgrid from triangulated mesh.
Expected: single triangle (0,0,0),(100,0,0),(100,100,1) with voxel 3 covers all surface samples
(reported 68 voxels on old versions).
Actual on 0.20: 628 voxels, 100% coverage. Verdict: FIXED."""
import numpy as np
import open3d as o3d
m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(np.array([[0, 0, 0], [100, 0, 0], [100, 100, 1]], float)),
                              o3d.utility.Vector3iVector([(0, 1, 2)]))
g = o3d.geometry.VoxelGrid.create_from_triangle_mesh(m, 3)
cov = np.mean(g.check_if_included(m.sample_points_uniformly(5000).points))
print(("OK: %d voxels, coverage %.3f" % (len(g.get_voxels()), cov)) if cov == 1.0 else "BUG REPRODUCED: coverage %.3f" % cov)
