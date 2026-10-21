"""https://github.com/isl-org/Open3D/issues/6710
Boolean intersection fails when one mesh encapsulates the other.
Expected: intersection equals the inner box.
Actual: empty mesh (VTK vtkBooleanOperationPolyDataFilter finds no surface intersection and
returns nothing). Root cause: cpp/open3d/t/geometry/TriangleMesh.cpp BooleanOperation
(no containment handling for non-intersecting surfaces). Verdict: CONFIRMED."""
import open3d as o3d

box1 = o3d.t.geometry.TriangleMesh.create_box()
box2 = o3d.t.geometry.TriangleMesh.create_box()
s = box1.vertex.positions.numpy() - 0.5
box1.vertex.positions = o3d.core.Tensor(s)
box2.vertex.positions = o3d.core.Tensor(s * 10)
r = box1.boolean_intersection(box2)
n = r.vertex.positions.shape[0]
print("BUG REPRODUCED: intersection of nested boxes is empty" if n == 0 else f"OK: {n} vertices")
