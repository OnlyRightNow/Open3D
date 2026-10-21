"""https://github.com/isl-org/Open3D/issues/5577
Inconsistent output between CPU & CUDA for Tensor::To and/or Tensor::Sum
Expected: comparison/logical ops on CPU store bool true as byte 1, so mask.To(Int64).Sum() counts
true elements and mask.To(UInt8)*255 is white. Actual (0.20 CPU wheel, ISPC enabled): ISPC kernels in
cpp/open3d/core/kernel/BinaryEWCPU.ispc / UnaryEWCPU.ispc (e.g. CPULogicalNotElement_bool, CPUEqElement_bool)
store ISPC varying bool true as 0xFF; casting that bool tensor to int/uint8 yields 255.
Matches the report exactly: CPU sum 391680 = 255 * 1536 (CUDA), and 255*255 wraps to 1 in uint8 -> black image.
Verdict: CONFIRMED
"""
import numpy as np, open3d as o3d
c = o3d.core
a = c.Tensor(np.array([1, 2, 3], np.int32)); b = c.Tensor(np.array([1, 5, 3], np.int32))
eq = a == b
print("raw bytes of (a==b):", eq.numpy().view(np.uint8), "| .to(int64):", eq.to(c.int64).numpy(),
      "| logical_not().to(uint8):", eq.logical_not().to(c.uint8).numpy())
rng = np.random.default_rng(0)
x = rng.integers(0, 100, (48, 64, 3)).astype(np.int32); y = x.copy(); y[:8, :16] += 5
diff = c.Tensor(x).isclose(c.Tensor(y)).logical_not()
s = diff.to(c.int64).sum([0, 1, 2]).item()
print("isclose->logical_not->To(Int64).Sum:", s, "expected", 8 * 16 * 3)
print("BUG REPRODUCED: CPU bool tensors from comparisons hold 255, casts give 255 not 1" if s != 384
      else "OK: CPU bool casts correct")
