"""https://github.com/isl-org/Open3D/issues/7166
Tensor.nonzero(as_tuple) semantics are inverted vs PyTorch and Open3D's own docs.
Expected (PyTorch): as_tuple=False -> one 2D tensor; as_tuple=True -> tuple/list of 1D tensors.
Actual (0.20): as_tuple=False returns a list of 1D tensors, as_tuple=True a 2D tensor (docstring
describes this inverted behavior). Root cause: cpp/pybind/core/tensor.cpp Tensor.nonzero lambda.
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d

t = o3d.core.Tensor(np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]], dtype=np.int64))
a_false = t.nonzero(as_tuple=False)
a_true = t.nonzero(as_tuple=True)
print("as_tuple=False ->", type(a_false).__name__, getattr(a_false, "shape", None))
print("as_tuple=True  ->", type(a_true).__name__, getattr(a_true, "shape", len(a_true)))
print("docstring:", t.nonzero.__doc__.strip().splitlines()[:6])
if isinstance(a_false, o3d.core.Tensor) and isinstance(a_true, (list, tuple)):
    print("OK: as_tuple semantics match PyTorch")
else:
    print("BUG REPRODUCED: as_tuple semantics inverted vs PyTorch")
