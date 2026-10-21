"""https://github.com/isl-org/Open3D/issues/5550
Potentially missing "new" in TransformationEstimationForColoredICP(kernel) binding
Expected: constructor with kernel works and keeps kernel. (pybind11 factories may return by value.)
"""
import open3d as o3d
reg = o3d.t.pipelines.registration
k = reg.robust_kernel.RobustKernel(reg.robust_kernel.RobustKernelMethod.TukeyLoss, 0.5)
te = reg.TransformationEstimationForColoredICP(k)
print(te, te.kernel.type, te.kernel.scaling_parameter)
if te.kernel.type == reg.robust_kernel.RobustKernelMethod.TukeyLoss and abs(te.kernel.scaling_parameter - 0.5) < 1e-9:
    print("OK: by-value factory constructor works correctly (no missing new)")
else:
    print("BUG REPRODUCED: kernel not set")
