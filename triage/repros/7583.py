"""https://github.com/isl-org/Open3D/issues/7583
compute_fpfh_feature stub incorrectly requires the optional indices argument.
Expected: signature/stub shows `indices: Sequence[SupportsInt] | None = None`.
Actual (0.20): docstring signature (from which the .pyi is generated) drops `| None = None`,
because the docstring rewriter's type regex (cpp/pybind/docstring.cpp) has no '|'. Runtime call works.
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d

f = o3d.pipelines.registration.compute_fpfh_feature
sig = f.__doc__.splitlines()[0]
print(sig)
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(100, 3)))
pcd.estimate_normals()
feat = f(pcd, o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=30))
print("runtime call without indices works, feature num =", feat.num())
if "indices" in sig and "= None" not in sig.split("indices")[1]:
    print("BUG REPRODUCED: signature marks optional 'indices' as required")
else:
    print("OK: 'indices' shown as optional")
