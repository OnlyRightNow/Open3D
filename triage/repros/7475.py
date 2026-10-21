"""https://github.com/isl-org/Open3D/issues/7475
registration_ransac_based_on_feature_matching cannot be deterministic (with checkers, seeded).
Expected: identical results for repeated runs after o3d.utility.random.seed(0).
Actual (0.20, CPU, noisy synthetic torus): identical across runs.
Verdict: FIXED
"""
import numpy as np
import open3d as o3d

reg = o3d.pipelines.registration
mesh = o3d.geometry.TriangleMesh.create_torus()
rng = np.random.default_rng(0)
src = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.asarray(mesh.sample_points_uniformly(20000).points)))
src = src.voxel_down_sample(0.05)
T = np.eye(4); T[:3, :3] = o3d.geometry.get_rotation_matrix_from_xyz((0.3, 0.2, 0.1)); T[:3, 3] = (0.5, 0.1, 0)
tgt = o3d.geometry.PointCloud(src).transform(T)
tgt.points = o3d.utility.Vector3dVector(np.asarray(tgt.points) + rng.normal(0, 0.01, (len(tgt.points), 3)))
for p in (src, tgt):
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
fp = [reg.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=100)) for p in (src, tgt)]
d = 0.075


def run():
    o3d.utility.random.seed(0)
    r = reg.registration_ransac_based_on_feature_matching(
        src, tgt, fp[0], fp[1], True, d, reg.TransformationEstimationPointToPoint(False), 3,
        [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(d)],
        reg.RANSACConvergenceCriteria(100000, 0.999))
    return r.fitness, r.inlier_rmse, len(r.correspondence_set), r.transformation.copy()


res = [run() for _ in range(5)]
for r in res:
    print("fitness %.6f rmse %.6f corr %d" % r[:3])
same = all(r[:3] == res[0][:3] and np.array_equal(r[3], res[0][3]) for r in res)
print("OK: seeded RANSAC deterministic across 5 runs" if same else
      "BUG REPRODUCED: seeded RANSAC results differ across runs")
