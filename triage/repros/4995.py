"""https://github.com/isl-org/Open3D/issues/4995
write_point_cloud saves with different precision depending on write_ascii.
Expected: same round-trip precision for ascii and binary.
Actual: legacy PCD header declares x/y/z as 4-byte float; binary stores float32 (error ~0.25 at UTM-like
coordinates), ascii prints %.10g (error ~5e-4). PLY is the reverse: ascii uses rply "%g" (6 digits, error ~5)
while binary stores doubles exactly.
Verdict: CONFIRMED (cpp/open3d/io/file_format/FilePCD.cpp: GenerateHeader/WritePCDData; 3rdparty/rply ply_write_ascii_double)."""
import os, tempfile
import numpy as np
import open3d as o3d
d = tempfile.mkdtemp()
pts = np.random.rand(1000, 3) * 10 + np.array([384826, 5825884, 0])
pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pts))
err = {}
for ext in ("pcd", "ply"):
    for asc in (True, False):
        p = os.path.join(d, "x%d.%s" % (asc, ext))
        o3d.io.write_point_cloud(p, pc, write_ascii=asc)
        err[(ext, asc)] = np.abs(np.asarray(o3d.io.read_point_cloud(p).points) - pts).max()
print(err)
if any(abs(np.log10(err[(e, True)] + 1e-12) - np.log10(err[(e, False)] + 1e-12)) > 2 for e in ("pcd", "ply")):
    print("BUG REPRODUCED: round-trip error differs by >100x between write_ascii=True/False")
else:
    print("OK: consistent precision")
