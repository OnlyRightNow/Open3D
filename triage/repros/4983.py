"""https://github.com/isl-org/Open3D/issues/4983
orient_normals_consistent_tangent_plane() Infinite Loop.
Expected: runtime similar with or without exactly coplanar regular-grid points.
Actual: 20k box samples + 10k exactly coplanar grid points take ~30 s (Delaunay alone ~33 s); adding 1e-4 noise
gives ~3 s. Qhull "d Qbb Qt" is very slow on degenerate cospherical input; large clouds appear to hang.
Verdict: CONFIRMED (cpp/open3d/geometry/Qhull.cpp: Qhull::ComputeDelaunayTetrahedralization via
EstimateNormals.cpp: PointCloud::OrientNormalsConsistentTangentPlane)."""
import time
import numpy as np
import open3d as o3d
def run(noise):
    pc = o3d.geometry.TriangleMesh.create_box().sample_points_uniformly(20000)
    g = np.stack(np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100)), -1).reshape(-1, 2)
    pc.points.extend(o3d.utility.Vector3dVector(np.c_[g, np.full(len(g), 2.0)] + np.random.randn(len(g), 3) * noise))
    pc.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(30))
    t = time.time(); pc.orient_normals_consistent_tangent_plane(30); return time.time() - t
a, b = run(0.0), run(1e-4)
print("coplanar %.1fs, jittered %.1fs" % (a, b))
print("BUG REPRODUCED: >5x slowdown on exactly coplanar points" if a > 5 * b else "OK: no pathological slowdown")
