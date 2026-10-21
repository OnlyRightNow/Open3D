"""https://github.com/isl-org/Open3D/issues/5091
Binary PLY files with Rhino 6.0 (CRLF header line endings) fail to load.
Expected: file loads. Actual on 0.5.12: 'Read PLY failed: unable to parse header'.
Verdict: FIXED on 0.20 for a synthetic binary PLY with CRLF header (the original Rhino file was not available).
"""
import os, tempfile, numpy as np, open3d as o3d
hdr = (b"ply\r\nformat binary_little_endian 1.0\r\ncomment Rhinoceros Version 6.0\r\n"
       b"element vertex 3\r\nproperty float x\r\nproperty float y\r\nproperty float z\r\nend_header\r\n")
with tempfile.TemporaryDirectory() as d:
    f = os.path.join(d, "box.ply")
    open(f, "wb").write(hdr + np.arange(9, dtype="<f4").tobytes())
    pts = np.asarray(o3d.io.read_point_cloud(f).points)
print(pts.tolist())
print("OK: CRLF binary PLY parsed" if np.allclose(pts.ravel(), np.arange(9)) else "BUG REPRODUCED")
