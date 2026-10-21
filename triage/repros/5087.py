"""https://github.com/isl-org/Open3D/issues/5087
Cropping a cropped PCD returns empty (AxisAlignedBoundingBox with min_bound > max_bound).
Expected: crop returns the points inside the box. Actual on 0.15: empty result for inverted bounds.
Verdict: FIXED on 0.20 (constructor warns and swaps bounds; crop returns points).
"""
import numpy as np, open3d as o3d
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.random.rand(1000, 3)))
bb = o3d.geometry.AxisAlignedBoundingBox([0.8] * 3, [0.2] * 3)  # inverted
n = len(pcd.crop(bb).points)
print("bounds:", bb.min_bound, bb.max_bound, "cropped:", n)
print("OK: inverted box is normalized and crop is non-empty" if n > 0 else "BUG REPRODUCED: crop empty")
