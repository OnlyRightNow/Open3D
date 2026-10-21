"""https://github.com/isl-org/Open3D/issues/4934
Weird memory behaviour with KDTreeFlann and numpy array.
Expected: KNN results stable after allocating other numpy arrays / with temporary inputs.
Actual on 0.20: 0/200 wrong results in the reported np.empty scenario and 0 mismatches vs
compute_point_cloud_distance for a temporary input array. Verdict: FIXED."""
import numpy as np
import open3d as o3d
bad = 0
for _ in range(200):
    a1 = np.empty([2, 4]); a1[:] = [[1, 3, 8, 12], [1, 3, 8, 12]]
    tree = o3d.geometry.KDTreeFlann(a1)
    i1 = tree.search_knn_vector_xd(np.array([4.0, 4.0]), 1)[1][0]
    a2 = np.empty([2, 4]); a2[:] = 1
    i2 = tree.search_knn_vector_xd(np.array([4.0, 4.0]), 1)[1][0]
    bad += (i1 != 1) or (i2 != 1)
p1, p2 = np.random.rand(10000, 3), np.random.rand(10000, 3)
tree = o3d.geometry.KDTreeFlann(p1.T * 1.0)  # temporary
d = np.sqrt([tree.search_knn_vector_xd(p, 1)[2][0] for p in p2])
ref = np.asarray(o3d.geometry.PointCloud(o3d.utility.Vector3dVector(p2)).compute_point_cloud_distance(
    o3d.geometry.PointCloud(o3d.utility.Vector3dVector(p1))))
mis = int(np.sum(np.abs(d - ref) > 1e-9))
print("OK: no wrong results" if bad == 0 and mis == 0 else "BUG REPRODUCED: bad=%d mismatches=%d" % (bad, mis))
