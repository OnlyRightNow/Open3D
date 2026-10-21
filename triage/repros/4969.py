"""https://github.com/isl-org/Open3D/issues/4969
Loading of *.pcd point clouds ignores decimals after initializing PyQt's QApplication.
QApplication calls setlocale(LC_ALL, "") so LC_NUMERIC becomes e.g. de_DE (decimal comma).
Expected: ASCII PCD floats parsed with '.' regardless of process locale.
Actual: under a comma-decimal LC_NUMERIC, values are truncated to integers.
Verdict: CONFIRMED (simulated QApplication via ctypes setlocale; locale built with localedef).
"""
import ctypes, os, subprocess, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
code = r'''
import ctypes, sys, numpy as np, open3d as o3d
path = sys.argv[1]
with open(path, "w") as f:
    f.write("VERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n"
            "WIDTH 1\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS 1\nDATA ascii\n"
            "-0.20108423 11.055668 0.56653374\n")
libc = ctypes.CDLL("libc.so.6")
LC_NUMERIC = 1
r = libc.setlocale(LC_NUMERIC, b"de_DE.UTF-8")
print("setlocale ok:", bool(r))
pts = np.asarray(o3d.io.read_point_cloud(path).points)
print("read:", pts[0])
if bool(r) and not np.allclose(pts[0], [-0.20108423, 11.055668, 0.56653374], atol=1e-5):
    print("BUG REPRODUCED: PCD ASCII parsing depends on LC_NUMERIC; decimals dropped:", pts[0])
elif bool(r):
    print("OK: decimals preserved under de_DE LC_NUMERIC")
else:
    print("SKIPPED: could not set de_DE locale")
'''
env = dict(os.environ)
loc = os.path.join(HERE, "loc")
if not os.path.isdir(os.path.join(loc, "de_DE.UTF-8")):
    os.makedirs(loc, exist_ok=True)
    subprocess.run(["localedef", "-i", "de_DE", "-f", "UTF-8", os.path.join(loc, "de_DE.UTF-8")])
env["LOCPATH"] = loc
with tempfile.TemporaryDirectory() as d:
    r = subprocess.run([sys.executable, "-c", code, os.path.join(d, "p.pcd")], env=env, capture_output=True, text=True)
    print(r.stdout, r.stderr[-300:])
