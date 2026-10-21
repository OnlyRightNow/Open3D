"""https://github.com/isl-org/Open3D/issues/5506
cluster_connected_triangles returns arrays of different lengths (0.15 vs 0.13)
Documented behaviour: triangle_clusters has one entry per triangle, cluster_n_triangles and
cluster_area have one entry per cluster, so lengths differ by design.
"""
import numpy as np, open3d as o3d
m = o3d.geometry.TriangleMesh.create_box() + o3d.geometry.TriangleMesh.create_sphere().translate((5, 0, 0))
tc, n, area = m.cluster_connected_triangles()
tc, n = np.asarray(tc), np.asarray(n)
print("triangles", len(m.triangles), "triangle_clusters", len(tc), "cluster_n_triangles", n, "areas", len(area))
ok = len(tc) == len(m.triangles) and len(n) == 2 and n.sum() == len(m.triangles)
print("OK: per-triangle labels + per-cluster counts, consistent (works as designed)" if ok
      else "BUG REPRODUCED: inconsistent outputs")
