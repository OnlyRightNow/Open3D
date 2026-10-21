"""https://github.com/isl-org/Open3D/issues/1718
deform_as_rigid_as_possible fails with "Failed to build solver (factorize)" on some meshes.
Expected: deformation succeeds, or a clear error naming the bad input (e.g. unreferenced vertices).
Actual (0.20): a single unreferenced, unconstrained vertex makes the Laplacian L singular (empty row,
since W == 0 adds no diagonal) -> "Failed to build solver (factorize)".
Root cause: cpp/open3d/geometry/TriangleMeshDeformation.cpp TriangleMesh::DeformAsRigidAsPossible.
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d


def try_deform(mesh, label):
    v = np.asarray(mesh.vertices)
    static_ids = [int(i) for i in np.where(v[:, 2] < -0.3)[0]]
    handle = int(np.argmax(v[:, 2]))
    ids = static_ids + [handle]
    pos = [v[i] for i in static_ids] + [v[handle] + (0, 0, 0.2)]
    try:
        out = mesh.deform_as_rigid_as_possible(o3d.utility.IntVector(ids), o3d.utility.Vector3dVector(pos), 20)
        ok = np.isfinite(np.asarray(out.vertices)).all()
        print(f"{label}: success, finite vertices={ok}")
        return ok
    except RuntimeError as e:
        print(f"{label}: RuntimeError: {str(e).strip()[-120:]}")
        return False


m = o3d.geometry.TriangleMesh.create_sphere(0.5, 20)
ok_clean = try_deform(o3d.geometry.TriangleMesh(m), "clean sphere")
m2 = o3d.geometry.TriangleMesh(m)
m2.vertices.append([5.0, 5.0, 0.0])  # one unreferenced (isolated) vertex
ok_iso = try_deform(m2, "sphere + 1 unreferenced vertex")
if ok_clean and not ok_iso:
    print("BUG REPRODUCED: ARAP fails on mesh with an unreferenced vertex (singular system)")
else:
    print("OK: ARAP handles the unreferenced vertex")
