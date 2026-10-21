"""https://github.com/isl-org/Open3D/issues/4049
deform_as_rigid_as_possible fails on meshes other than Armadillo ('Failed to build solver (factorize)').
Reporter's mesh has 75000 vertices for 25000 triangles = an unshared-vertex triangle soup.
Expected: ARAP works or gives an actionable error. Actual: connected mesh works; triangle soup -> factorize error.
Verdict: CONFIRMED as usage issue (DeformAsRigidAsPossible in cpp/open3d/geometry/TriangleMeshDeformation.cpp:
singular system for disconnected vertices; error does not hint at merge_close_vertices).
"""
import numpy as np, open3d as o3d
m = o3d.geometry.TriangleMesh.create_sphere(1.0, 30)
V, T = np.asarray(m.vertices), np.asarray(m.triangles)
soup = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(V[T.reshape(-1)]),
                                 o3d.utility.Vector3iVector(np.arange(T.size).reshape(-1, 3)))
res = {}
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Error):
    for name, mm in [("connected", m), ("soup", soup)]:
        VV = np.asarray(mm.vertices)
        st = list(np.where(VV[:, 2] < -0.5)[0]); h = int(np.argmax(VV[:, 2]))
        try:
            out = mm.deform_as_rigid_as_possible(o3d.utility.IntVector(st + [h]),
                o3d.utility.Vector3dVector([VV[i] for i in st] + [VV[h] + 0.3]), max_iter=5)
            res[name] = "moved %d vertices" % (np.linalg.norm(np.asarray(out.vertices) - VV, axis=1) > 1e-3).sum()
        except RuntimeError as e:
            res[name] = "error: " + ("factorize" if "factorize" in str(e) else str(e)[:80])
print(res)
print("BUG REPRODUCED: triangle-soup mesh -> %s" % res["soup"] if "error" in res["soup"] else "OK")
