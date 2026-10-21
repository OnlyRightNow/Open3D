"""https://github.com/isl-org/Open3D/issues/5879
numpy.asarray for open3d.core.Tensor converts the Tensor to np.ndarray of "scalar" Tensors
Expected: np.asarray(t) == t.numpy() with numeric dtype. Actual (0.16): object array of scalar Tensors.
"""
import numpy as np, open3d as o3d
t = o3d.core.Tensor(np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32))
a = np.asarray(t)
print(a.dtype, type(a.flat[0]))
if a.dtype == np.float32:
    print("OK: np.asarray(Tensor) returns float32 array")
else:
    print("BUG REPRODUCED: np.asarray(Tensor) gives dtype", a.dtype)
