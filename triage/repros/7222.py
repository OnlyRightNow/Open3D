"""https://github.com/isl-org/Open3D/issues/7222 - RAM issue while loading several PCL in threads
Expected: RSS returns near baseline after deleting clouds loaded in threads. Actual (0.19): ~300 MB retained.
Verdict on 0.20: FIXED / not reproduced (residual growth is small, consistent with glibc arena caching)."""
import gc, os, threading, numpy as np, open3d as o3d
rss = lambda: int(open(f"/proc/{os.getpid()}/statm").read().split()[1]) * 4096 / 2**20
o3d.io.write_point_cloud("/tmp/_7222.ply", o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(200000, 3))))
base = rss(); pcls = []; lock = threading.Lock()
def load():
    x = o3d.io.read_point_cloud("/tmp/_7222.ply")
    with lock: pcls.append(x)
for _ in range(3):
    ths = [threading.Thread(target=load) for _ in range(50)]; [t.start() for t in ths]; [t.join() for t in ths]
    peak = rss(); pcls.clear(); gc.collect()
growth = rss() - base
print(f"{'OK' if growth < 100 else 'BUG REPRODUCED'}: baseline {base:.0f} MB, peak {peak:.0f} MB, after 150 loads+gc {rss():.0f} MB (+{growth:.0f})")
