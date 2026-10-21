"""https://github.com/isl-org/Open3D/issues/6137
read_triangle_mesh enable_post_processing=false just reduces post processing but does not turn off.
Expected: OBJ with 8 vertices (3 unused) reads back with 8 vertices when enable_post_processing=False.
Actual: 5 vertices; ASSIMP drops unreferenced vertices and always applies aiProcess_JoinIdenticalVertices.
Verdict: CONFIRMED (cpp/open3d/io/file_format/FileASSIMP.cpp: ReadTriangleMeshUsingASSIMP)."""
import os, tempfile
import numpy as np
import open3d as o3d
m = o3d.geometry.TriangleMesh()
m.vertices = o3d.utility.Vector3dVector(np.random.rand(8, 3))
m.triangles = o3d.utility.Vector3iVector([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
p = os.path.join(tempfile.mkdtemp(), "a.obj")
o3d.io.write_triangle_mesh(p, m)
n = len(o3d.io.read_triangle_mesh(p, enable_post_processing=False).vertices)
print(("BUG REPRODUCED: read back %d vertices, expected 8" % n) if n != 8 else "OK: 8 vertices preserved")
