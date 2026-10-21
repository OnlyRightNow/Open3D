"""https://github.com/isl-org/Open3D/issues/6939 - Mesh vertices shape inconsistency after STL round trip
Expected: same vertex count after write/read STL. Actual: vertices inflated (shared vertices not re-merged).
Verdict on 0.20: CONFIRMED. Root cause: io/file_format/FileASSIMP.cpp ReadTriangleMeshUsingASSIMP -
aiProcess_JoinIdenticalVertices does not merge STL vertices with different per-face normals.
Workaround: mesh.merge_close_vertices(1e-9)."""
import os, tempfile, open3d as o3d
m = o3d.geometry.TriangleMesh.create_sphere(); m.compute_triangle_normals()
f = os.path.join(tempfile.mkdtemp(), "s.stl"); o3d.io.write_triangle_mesh(f, m); m2 = o3d.io.read_triangle_mesh(f)
a, b = len(m.vertices), len(m2.vertices)
print(f"BUG REPRODUCED: {a} vertices -> {b} after STL round trip (triangles {len(m.triangles)} -> {len(m2.triangles)})" if a != b else "OK")
