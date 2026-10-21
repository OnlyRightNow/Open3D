"""https://github.com/isl-org/Open3D/issues/7558
geometry::OrientedBoundingBox::Transform() always throws, even for a rigid transform.
Expected: a pure translation (rigid) transform updates the box center.
Actual (0.20): RuntimeError "A general transform of an OrientedBoundingBox is not implemented".
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d

box = o3d.geometry.OrientedBoundingBox(np.zeros(3), np.eye(3), np.ones(3))
T = np.eye(4)
T[0, 3] = 1.0
try:
    box.transform(T)
    print("OK: transform applied, center =", box.center)
except RuntimeError as e:
    print("BUG REPRODUCED: OrientedBoundingBox.transform raised:", e)
