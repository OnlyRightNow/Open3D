"""https://github.com/isl-org/Open3D/issues/1887
Many holes in the Bunny data using ball pivoting.
Expected: BPA on bunny vertices with correct (mesh) normals gives a nearly hole-free surface.
Actual: thousands of boundary edges vs 223 in the source mesh, even with ground-truth oriented normals.
Verdict: CONFIRMED (BallPivoting in cpp/open3d/geometry/SurfaceReconstructionBallPivoting.cpp). Needs o3d.data.BunnyMesh download.
"""
import open3d as o3d
m = o3d.io.read_triangle_mesh(o3d.data.BunnyMesh().path); m.compute_vertex_normals()
pcd = o3d.geometry.PointCloud(m.vertices); pcd.normals = m.vertex_normals
r = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector([0.002, 0.004, 0.006, 0.008, 0.01]))
b0, b1 = len(m.get_non_manifold_edges(False)), len(r.get_non_manifold_edges(False))
print("source boundary edges", b0, "BPA boundary edges", b1, "tris", len(r.triangles), "/", len(m.triangles))
print("BUG REPRODUCED: BPA leaves many holes" if b1 > 5 * b0 else "OK: few holes")
