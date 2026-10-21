"""https://github.com/isl-org/Open3D/issues/5706
plt.tick_params() influences rounding of read pointcloud
Expected: ASCII PCD values parsed with full precision regardless of process locale.
Actual: matplotlib GUI backend sets LC_NUMERIC to the user locale (e.g. de_DE, decimal comma);
Open3D's ASCII PCD reader uses locale-dependent std::strtod/strtof, so 829.88127 -> 829.
This script emulates the backend by setting LC_NUMERIC=de_DE.UTF-8 (generated with localedef if needed).
Verdict: CONFIRMED
"""
import os, subprocess, sys, tempfile, textwrap

tmp = tempfile.mkdtemp()
pcd = os.path.join(tmp, "p.pcd")
with open(pcd, "w") as f:
    f.write("# .PCD v0.7\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n"
            "WIDTH 1\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS 1\nDATA ascii\n829.88127 1899.80715 101.29749\n")
env = dict(os.environ)
r = subprocess.run(["localedef", "-i", "de_DE", "-f", "UTF-8", os.path.join(tmp, "de_DE.UTF-8")],
                   capture_output=True)
env["LOCPATH"] = tmp
code = textwrap.dedent(f"""
    import locale, numpy as np, open3d as o3d
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')  # what a Qt/GTK matplotlib backend does
    print(np.asarray(o3d.io.read_point_cloud({pcd!r}).points)[0])
""")
p = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
out = p.stdout.strip()
print(out, p.stderr.strip()[-300:])
if "829.88" in out:
    print("OK: PCD parsed with full precision under de_DE LC_NUMERIC")
elif out:
    print("BUG REPRODUCED: ASCII PCD values truncated under comma-decimal LC_NUMERIC:", out)
else:
    print("Could not set locale; inconclusive")
