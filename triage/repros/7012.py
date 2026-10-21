"""https://github.com/isl-org/Open3D/issues/7012 - GICP registration failed (NaN) with covariances only
Expected: GICP with only estimate_covariances() converges. Actual (0.18, user data): NaN transform.
Verdict on 0.20: FIXED on synthetic data (reporter's 1.ply not available)."""
import numpy as np, open3d as o3d
reg = o3d.pipelines.registration
src = o3d.geometry.TriangleMesh.create_torus().sample_points_uniformly(5000)
T = np.eye(4); T[:3, :3] = o3d.geometry.get_rotation_matrix_from_xyz([0.0035] * 3); T[:3, 3] = [0.05, 0.1, 0.02]
tgt = o3d.geometry.PointCloud(src).transform(T)
for pc in (src, tgt): pc.estimate_covariances(o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))
r = reg.registration_generalized_icp(src, tgt, 0.3, np.eye(4), reg.TransformationEstimationForGeneralizedICP(0.001),
                                     reg.ICPConvergenceCriteria(1e-6, 1e-6, 100))
ok = np.isfinite(r.transformation).all() and np.allclose(r.transformation, T, atol=1e-3)
print("OK: covariance-only GICP recovers transform" if ok else f"BUG REPRODUCED: {r.transformation}")
