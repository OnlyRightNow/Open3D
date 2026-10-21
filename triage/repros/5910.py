"""https://github.com/isl-org/Open3D/issues/5910
filter_smooth_laplacian() created nan values when applied to bunny mesh
Expected: no NaN. Actual (0.16): NaN vertices (inverse-distance weight 1/0 for coincident vertices).
0.20 adds an epsilon in TriangleMesh::FilterSmoothLaplacian (1/(d+1e-12)).
Verdict: FIXED
"""
import numpy as np, open3d as o3d
meshes = []
try:
    meshes.append(("bunny", o3d.io.read_triangle_mesh(o3d.data.BunnyMesh().path)))
except Exception as e:
    print("bunny unavailable:", e)
# Synthetic: two coincident (duplicate) vertices joined by an edge -> zero-length edge
m = o3d.geometry.TriangleMesh.create_sphere(1.0, 20)
v = np.asarray(m.vertices); t = np.asarray(m.triangles)
v2 = np.vstack([v, v[t[0, 0]]]); t2 = np.vstack([t, [t[0, 1], t[0, 2], len(v)]])
t2 = np.vstack([t2, [t[0, 0], len(v), t[0, 1]]])
meshes.append(("zero-length-edge", o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(v2), o3d.utility.Vector3iVector(t2))))
bad = []
for name, mesh in meshes:
    s = mesh.filter_smooth_laplacian(number_of_iterations=1, lambda_filter=0.1)
    n = int(np.isnan(np.asarray(s.vertices)).sum())
    print(name, "NaN count:", n)
    if n: bad.append(name)
print("BUG REPRODUCED: NaN in " + ",".join(bad) if bad else "OK: no NaN after filter_smooth_laplacian")
