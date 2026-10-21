"""https://github.com/isl-org/Open3D/issues/6450
The vertices are redundant when loading a triangle mesh from stl file.
Expected: a closed box written to STL reads back with 8 shared vertices and is watertight.
Actual: 24 vertices (one per face corner), is_watertight() False. STL per-face normals make
ASSIMP's aiProcess_JoinIdenticalVertices keep corners distinct.
Verdict: CONFIRMED (cpp/open3d/io/file_format/FileASSIMP.cpp: ReadTriangleMeshUsingASSIMP)."""
import os, tempfile
import open3d as o3d
b = o3d.geometry.TriangleMesh.create_box()
b.compute_triangle_normals()
p = os.path.join(tempfile.mkdtemp(), "b.stl")
o3d.io.write_triangle_mesh(p, b)
r = o3d.io.read_triangle_mesh(p)
if len(r.vertices) != 8 or not r.is_watertight():
    print("BUG REPRODUCED: STL box read with %d vertices, watertight=%s (expected 8, True)" % (len(r.vertices), r.is_watertight()))
else:
    print("OK: STL vertices merged")
