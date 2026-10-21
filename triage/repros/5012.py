"""https://github.com/isl-org/Open3D/issues/5012
search_radius_vector_3d crashes when using a kdtree returned by a function
Expected: KDTreeFlann built inside a function (from a local point cloud / numpy array) stays valid.
In 0.20 KDTreeFlann copies data into data_ (KDTreeFlann::SetRawData).
"""
import numpy as np, open3d as o3d, gc

def make_tree_pcd():
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(20000, 3) * 100))
    pcd = pcd.voxel_down_sample(10)
    return o3d.geometry.KDTreeFlann(pcd), np.asarray(pcd.points).copy()

def make_tree_np():
    a = np.random.rand(6, 5000) * 100
    return o3d.geometry.KDTreeFlann(a), a.copy()

ok = True
for mk in (make_tree_pcd, make_tree_np):
    tree, ref = mk(); gc.collect()
    junk = [np.random.rand(1000, 1000) for _ in range(5)]  # overwrite freed memory
    for i in range(0, ref.shape[1] if ref.shape[0] == 6 else ref.shape[0], 37):
        q = ref[:, i] if ref.shape[0] == 6 else ref[i]
        k, idx, d = tree.search_hybrid_vector_3d(q[:3] if ref.shape[0] != 6 else q, 15.0, 5) if ref.shape[0] != 6 \
            else tree.search_knn_vector_xd(q, 1)
        if k < 1 or d[0] > 1e-9:
            ok = False
print("OK: KDTree returned from a function still finds the exact query points" if ok
      else "BUG REPRODUCED: KDTree from function returns wrong results")
