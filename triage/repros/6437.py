"""https://github.com/isl-org/Open3D/issues/6437
Segfault when loading a .pcd file with padding fields (named "_") into a tensor point cloud.
Expected: file loads, "_" padding fields are skipped (as PCL does).
Actual: each "_" field calls SetPointAttr("_") again, freeing the previous tensor while
map_field_to_attr_ptr keeps its stale data pointer -> use-after-free writes (segfault for
large clouds). Root cause: cpp/open3d/t/io/file_format/FilePCD.cpp ReadPCDData.
Verdict: CONFIRMED."""
import os, subprocess, sys, tempfile
import numpy as np

N = 2_000_000  # big enough that freed attribute buffers are mmap'd and unmapped
path = os.path.join(tempfile.mkdtemp(), "pad.pcd")
hdr = (f"# .PCD v0.7\nVERSION 0.7\nFIELDS x y z _ intensity _\nSIZE 4 4 4 1 4 2\n"
       f"TYPE F F F U F U\nCOUNT 1 1 1 4 1 3\nWIDTH {N}\nHEIGHT 1\n"
       f"VIEWPOINT 0 0 0 1 0 0 0\nPOINTS {N}\nDATA binary\n")
rec = np.zeros(N, dtype=[("xyz", "<f4", 3), ("p1", "u1", 4), ("i", "<f4"), ("p2", "<u2", 3)])
rec["xyz"] = np.arange(N, dtype=np.float32)[:, None]
rec["i"] = np.arange(N, dtype=np.float32)
with open(path, "wb") as f:
    f.write(hdr.encode()); f.write(rec.tobytes())
code = ("import open3d as o3d,sys; p=o3d.t.io.read_point_cloud(sys.argv[1]); "
        "print(sorted(p.point)); print(float(p.point.intensity[7].item()))")
r = subprocess.run([sys.executable, "-c", code, path], capture_output=True, text=True)
out = r.stdout.strip()
if r.returncode != 0:
    print(f"BUG REPRODUCED: reading PCD with '_' padding fields crashed (exit code {r.returncode})")
elif "'_'" in out:
    print(f"BUG REPRODUCED: '_' padding fields loaded as attribute (stale-pointer path): {out!r}")
else:
    print(f"OK: loaded without padding attribute: {out!r}")
