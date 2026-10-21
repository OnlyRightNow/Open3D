"""https://github.com/isl-org/Open3D/issues/6153
Wrong check for identity transformation as a result of registration.
Expected: a pure-translation registration result is accepted.
Actual: examples (register_fragments.py, benchmark_fgr.py, benchmark_ransac.py) treat trace()==4 as
"registration failed", but any pure translation also has trace 4.
Verdict: CONFIRMED (examples/python/reconstruction_system/register_fragments.py and benchmark scripts; Python only)."""
import numpy as np
T = np.eye(4); T[:3, 3] = [0.5, 0.0, 0.0]   # valid pure-translation result
fail_by_example = T.trace() == 4.0
print("BUG REPRODUCED: pure translation flagged as identity/failure by trace()==4 check"
      if fail_by_example and not np.allclose(T, np.eye(4)) else "OK")
