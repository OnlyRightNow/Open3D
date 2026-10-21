"""https://github.com/isl-org/Open3D/issues/5140 - t.pipelines.registration.icp incompatible function arguments
Expected: icp accepts a Float32 init_source_to_target. Actual (0.15): TypeError (only Float64 overload).
Verdict on 0.20: FIXED."""
import numpy as np, open3d as o3d
reg = o3d.t.pipelines.registration
src = o3d.t.geometry.PointCloud.from_legacy(o3d.geometry.TriangleMesh.create_torus().sample_points_uniformly(3000))
tgt = src.clone().translate([0.05, 0, 0])
try:
    r = reg.icp(src, tgt, 0.5, o3d.core.Tensor(np.eye(4), o3d.core.float32), reg.TransformationEstimationPointToPoint(),
                reg.ICPConvergenceCriteria(1e-6, 1e-6, 50), 0.2)
    print(f"OK: Float32 init accepted, fitness={r.fitness:.3f}")
except Exception as e:
    print("BUG REPRODUCED:", str(e)[:200])
