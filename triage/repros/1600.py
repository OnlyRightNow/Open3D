"""https://github.com/isl-org/Open3D/issues/1600
cluster_dbscan crashes on large clouds.
Expected: DBSCAN runs (or fails gracefully) on big/dense clouds.
Actual: PointCloud::ClusterDBSCAN precomputes and stores the full eps-neighbor list of
every point (O(N*k) memory), so dense/large clouds exhaust memory. On 0.20 this now
surfaces as MemoryError: std::bad_alloc (no longer a silent crash), but memory use is
still unbounded in N*k.
Root cause: cpp/open3d/geometry/PointCloudCluster.cpp PointCloud::ClusterDBSCAN.
Verdict: CONFIRMED."""
import subprocess, sys, textwrap
code = textwrap.dedent('''
import resource, numpy as np, open3d as o3d
resource.setrlimit(resource.RLIMIT_AS, (1_500_000_000, 1_500_000_000))  # 1.5 GB cap
p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(150_000, 3)))
# ~5k neighbours/point -> ~3 GB of neighbour indices
labels = np.asarray(p.cluster_dbscan(eps=0.2, min_points=10))
print("labels", labels.max() + 1)
''')
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=280)
if r.returncode != 0:
    print(f"BUG REPRODUCED: cluster_dbscan failed (exit code {r.returncode}) "
          f"under a 1.5 GB memory cap with 150k points; stderr tail: {r.stderr.strip()[-120:]!r}")
else:
    print("OK: cluster_dbscan completed:", r.stdout.strip())
