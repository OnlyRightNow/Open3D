"""https://github.com/isl-org/Open3D/issues/5842
PoissonRecon output should not depend on 'width' if 'depth' is given.
Expected (per docs: "width ... is ignored if depth is specified"): identical meshes for
different width values with the same depth.
Actual: width > 0 recomputes depth from width (GetPointXForm(..., width, scale, depth) writes
depth by reference), so output changes drastically. Root cause:
cpp/open3d/geometry/SurfaceReconstructionPoisson.cpp Execute (the `if (width > 0.0f)` branch).
Verdict: CONFIRMED."""
import numpy as np
import open3d as o3d

np.random.seed(0)
pc = o3d.geometry.TriangleMesh.create_sphere(1.0, 30).sample_points_uniformly(3000)
pc.estimate_normals()
pc.orient_normals_consistent_tangent_plane(10)
n = {}
for w in [0.0, 0.05, 0.5]:
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pc, depth=6, width=w, scale=1.1)
    n[w] = len(mesh.vertices)
if len(set(n.values())) > 1:
    print(f"BUG REPRODUCED: vertex count depends on width at fixed depth=6: {n}")
else:
    print(f"OK: width ignored: {n}")
