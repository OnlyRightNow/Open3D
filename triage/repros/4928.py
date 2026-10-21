"""https://github.com/isl-org/Open3D/issues/4928
OrientedBoundingBox renders flat.
Expected: 3D box. Actual: z of all corners equals center z.
Verdict: CONFIRMED as reported, but cause is user input: R has R[2,2]=0 (singular, not a rotation).
With a proper rotation the box is 3D. Library only lacks validation of R (OrientedBoundingBox ctor, cpp/open3d/geometry/BoundingVolume.h).
"""
import numpy as np, open3d as o3d
t = 0.5
R_bad = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 0]])
R_ok = R_bad.copy(); R_ok[2, 2] = 1
zb = np.ptp(np.asarray(o3d.geometry.OrientedBoundingBox([0, 0, 0], R_bad, [2, 2, 2]).get_box_points())[:, 2])
zo = np.ptp(np.asarray(o3d.geometry.OrientedBoundingBox([0, 0, 0], R_ok, [2, 2, 2]).get_box_points())[:, 2])
print("z extent with user R:", zb, " with valid R:", zo)
if zb == 0:
    print("BUG REPRODUCED: singular R accepted silently -> flat box (user error, no validation)")
else:
    print("OK")
