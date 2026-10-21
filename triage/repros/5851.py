"""https://github.com/isl-org/Open3D/issues/5851
read_triangle_model --- read_triangle_mesh not compatible.
Expected: same vertex count from read_triangle_model and read_triangle_mesh for the same file.
Actual: for a glTF without normals, read_triangle_model gives 24 vertices for a box and
read_triangle_mesh gives 8. ReadModelUsingAssimp always uses kPostProcessFlags_fast
(aiProcess_GenNormals splits vertices to flat-shade), read_triangle_mesh defaults to compulsory flags only.
Verdict: CONFIRMED (cpp/open3d/io/file_format/FileASSIMP.cpp: ReadModelUsingAssimp vs ReadTriangleMeshUsingASSIMP)."""
import os, tempfile
import open3d as o3d
p = os.path.join(tempfile.mkdtemp(), "c.gltf")
o3d.io.write_triangle_mesh(p, o3d.geometry.TriangleMesh.create_box())
a = len(o3d.io.read_triangle_model(p).meshes[0].mesh.vertices)
b = len(o3d.io.read_triangle_mesh(p).vertices)
print(("BUG REPRODUCED: model %d vs mesh %d vertices" % (a, b)) if a != b else "OK: counts match (%d)" % a)
