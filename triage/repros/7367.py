"""https://github.com/isl-org/Open3D/issues/7367
Tensor ICP does not stop when relative_fitness / relative_rmse criteria are met.
Expected: ICP stops early once fitness and RMSE stop changing.
Actual (0.20): stops early (converged in a few iterations of max 30).
Verdict: FIXED
"""
import numpy as np
import open3d as o3d

reg = o3d.t.pipelines.registration
rng = np.random.default_rng(0)
pts = np.asarray(o3d.geometry.TriangleMesh.create_sphere(0.5).sample_points_uniformly(20000).points)
src = o3d.t.geometry.PointCloud(o3d.core.Tensor(pts.astype(np.float32)))
T = np.eye(4); T[:3, 3] = (0.004, -0.002, 0.003)
tgt = src.clone().transform(o3d.core.Tensor(T))
tgt.point.positions = tgt.point.positions + o3d.core.Tensor(rng.normal(0, 0.001, pts.shape).astype(np.float32))
iters = []
res = reg.icp(src, tgt, 0.02, o3d.core.Tensor(np.eye(4)), reg.TransformationEstimationPointToPoint(),
              reg.ICPConvergenceCriteria(relative_fitness=1e-5, relative_rmse=1e-3, max_iteration=30),
              0.01, lambda d: iters.append((d["iteration_index"].item(), d["fitness"].item(), d["inlier_rmse"].item())))
for i, f, r in iters:
    print(f"iter {i}: fitness {f:.6f} rmse {r:.6f}")
print("num_iterations:", res.num_iterations)
if len(iters) >= 30:
    print("BUG REPRODUCED: tensor ICP ran all 30 iterations despite convergence")
else:
    print(f"OK: tensor ICP stopped after {len(iters)} iterations")
