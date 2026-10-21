"""https://github.com/isl-org/Open3D/issues/6721
No bounds are set when moving an AxisAlignedBoundingBox to a different device.
Expected: .to(device) keeps min/max bounds (and dtype).
Actual: To() builds a default box (zeros, Float32) and calls SetMaxBound then SetMinBound,
which validate against the preset zeros -> warning, bound dropped, dtype changes.
Shown on CPU with copy=True (same code path as CPU->CUDA).
Root cause: cpp/open3d/t/geometry/BoundingVolume.cpp AxisAlignedBoundingBox::To.
Verdict: CONFIRMED."""
import numpy as np
import open3d as o3d

b = o3d.t.geometry.AxisAlignedBoundingBox(o3d.core.Tensor([-3., -3, -3]), o3d.core.Tensor([-1., -1, -1]))
c = b.to(o3d.core.Device("CPU:0"), True)
if not np.allclose(c.max_bound.numpy(), [-1, -1, -1]) or c.min_bound.dtype != b.min_bound.dtype:
    print(f"BUG REPRODUCED: copied box is {c} (expected {b})")
else:
    print("OK: bounds preserved")
