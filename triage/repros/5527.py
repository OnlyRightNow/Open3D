"""https://github.com/isl-org/Open3D/issues/5527
open3d.io.read_triangle_mesh() doesn't read properly .obj files (empty mesh since 0.15; 0.14.1 worked)
Expected: an OBJ with quad (or n-gon) faces is triangulated and loaded, as in 0.14 (tinyobjloader).
Actual: 0.15+ reads OBJ via ASSIMP; with the default enable_post_processing=False only
kPostProcessFlags_compulsory is used (cpp/open3d/io/file_format/FileASSIMP.cpp ReadTriangleMeshUsingASSIMP),
which lacks aiProcess_Triangulate, so all non-triangle faces are dropped ("Skipping non-triangle primitive")
and an all-quad model (typical free3d base meshes) loads as an empty mesh. The reporter's file was not
available; this reproduces the symptom with a synthetic quad OBJ.
Even with enable_post_processing=True (aiProcess_Triangulate) the mesh is empty: the check
`assimp_mesh->mPrimitiveTypes != aiPrimitiveType_TRIANGLE` rejects TRIANGLE|NGONEncodingFlag (=20);
ReadModelUsingAssimp in the same file uses the correct bitmask test, so read_triangle_model works.
Verdict: CONFIRMED
"""
import os, tempfile, open3d as o3d
p = os.path.join(tempfile.mkdtemp(), "quad.obj")
open(p, "w").write("v 0 0 0\nv 1 0 0\nv 1 1 0\nv 0 1 0\nv 0 0 1\nv 1 0 1\nv 1 1 1\nv 0 1 1\n"
                   "f 1 4 3 2\nf 5 6 7 8\nf 1 2 6 5\nf 2 3 7 6\nf 3 4 8 7\nf 4 1 5 8\n")  # cube made of quads
m = o3d.io.read_triangle_mesh(p)
m2 = o3d.io.read_triangle_mesh(p, enable_post_processing=True)
print("default:", m, "| enable_post_processing=True:", m2)
n3 = len(o3d.io.read_triangle_model(p).meshes)
print("read_triangle_model sub-meshes:", n3)
print("BUG REPRODUCED: all-quad OBJ loads as empty mesh (with and without post-processing)" if len(m.triangles) == 0
      else "OK: quad OBJ triangulated")
