"""https://github.com/isl-org/Open3D/issues/6913 - read_point_cloud_from_bytes: unknown format for PLY
Expected: PLY bytes load like the file. Actual: 'unknown format', 0 points; only 'mem::xyz' is supported.
Verdict on 0.20: CONFIRMED. Root cause: io/PointCloudIO.cpp in-memory reader map only has "mem::xyz"."""
import os, tempfile, open3d as o3d
pc = o3d.geometry.TriangleMesh.create_sphere().sample_points_uniformly(1000)
f = os.path.join(tempfile.mkdtemp(), "x.ply"); o3d.io.write_point_cloud(f, pc)
b = open(f, "rb").read()
n = {fmt: len(o3d.io.read_point_cloud_from_bytes(b, format=fmt).points) for fmt in ("auto", "ply")}
print(f"BUG REPRODUCED: points read from PLY bytes {n} (file has 1000)" if 0 in n.values() else f"OK: {n}")
