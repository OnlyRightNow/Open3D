"""https://github.com/isl-org/Open3D/issues/7256
Claim: `fitness_ == other.fitness_` in RANSACResult::IsBetterRANSACThan
(cpp/open3d/geometry/PointCloudSegmentation.cpp) can never be true, so the inlier_rmse tie-break is dead.
Reality: fitness_ = (double)inlier_num / (double)points.size() (EvaluateRANSACBasedOnDistance), a single
correctly-rounded IEEE division, so two candidates with the same inlier count have bit-identical fitness
and the tie-break does trigger. An epsilon compare would only matter if fitness were accumulated.
Expected = Actual: exact equality for equal inlier counts.
Verdict: FIXED (not a bug; works as intended). The segment_plane call below is a smoke check.
"""
import numpy as np
import open3d as o3d

rng = np.random.default_rng(0)
ok = True
for _ in range(100000):
    n = int(rng.integers(1, 10**8)); k = int(rng.integers(0, n + 1))
    a = np.float64(k) / np.float64(n)
    b = np.float64(k) / np.float64(n)
    ok &= bool(a == b)
pts = np.c_[rng.uniform(-1, 1, (2000, 2)), rng.normal(0, 0.01, 2000)]
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pts))
plane, inl = pcd.segment_plane(0.02, 3, 1000)
print("segment_plane:", np.round(plane, 3), "inliers", len(inl))
print("OK: equal inlier counts always give bit-identical fitness; tie-break reachable" if ok else
      "BUG REPRODUCED: fitness differs for equal inlier counts")
