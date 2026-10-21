"""https://github.com/isl-org/Open3D/issues/5217
remove_triangles_by_mask doesn't adjust mesh triangle_material_ids.
Expected: triangle_material_ids compacted like triangles/uvs/normals. Actual: left unchanged (length mismatch).
Verdict: CONFIRMED (TriangleMesh::RemoveTrianglesByMask in cpp/open3d/geometry/TriangleMesh.cpp).
"""
import numpy as np, open3d as o3d
m = o3d.geometry.TriangleMesh.create_box()
m.triangle_material_ids = o3d.utility.IntVector(list(range(12)))
m.remove_triangles_by_mask([i % 2 == 0 for i in range(12)])
ids = np.asarray(m.triangle_material_ids)
print("triangles", len(m.triangles), "material ids", ids.tolist())
if len(ids) != len(m.triangles):
    print("BUG REPRODUCED: triangle_material_ids not updated by remove_triangles_by_mask")
else:
    print("OK: material ids compacted", "correct" if ids.tolist() == list(range(1, 12, 2)) else "but wrong values")
