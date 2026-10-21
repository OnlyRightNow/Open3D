"""https://github.com/isl-org/Open3D/issues/4792
Image constructor does not take care of non-contiguous input.
Expected: correct data or an error. Actual on 0.14: silently corrupted image.
Verdict: FIXED on 0.20 (raises 'Image can only be initialized from a contiguous buffer').
"""
import numpy as np, open3d as o3d
a = np.flipud(np.array([[0, 1, 2], [3, 4, 5]], dtype=np.uint8))
try:
    img = np.asarray(o3d.geometry.Image(a))
    print("OK: matches numpy" if np.array_equal(img, a) else "BUG REPRODUCED: silent corruption %s" % img.tolist())
except RuntimeError as e:
    print("OK: non-contiguous input rejected with error:", e)
