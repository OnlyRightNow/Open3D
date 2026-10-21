"""https://github.com/isl-org/Open3D/issues/5922
Boolean result not accurate.
Expected: boolean ops give clean results; union of a box with an identical copy is the box.
Actual: union of a box with its clone returns an empty mesh (coplanar faces are not handled
by VTK's boolean filter); the reporter's dog-minus-box artifacts need their STL (not tested).
Root cause: cpp/open3d/t/geometry/TriangleMesh.cpp BooleanOperation (vtkBooleanOperationPolyDataFilter).
Verdict: CONFIRMED (coplanar case)."""
import open3d as o3d

b = o3d.t.geometry.TriangleMesh.create_box()
r = b.boolean_union(b.clone())
n = r.vertex.positions.shape[0]
print("BUG REPRODUCED: union of box with its clone is empty" if n == 0 else f"OK: {n} vertices")
