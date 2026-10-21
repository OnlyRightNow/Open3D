"""https://github.com/isl-org/Open3D/issues/4791
Bounding box properties inconsistency between AxisAlignedBoundingBox and OrientedBoundingBox.
Expected: same accessors on both. Actual: OBB has center/extent properties but no get_extent; AABB has get_extent but no extent/center properties.
Verdict: CONFIRMED (Python bindings cpp/pybind/geometry/boundingvolume.cpp).
"""
import open3d as o3d
names = ["center", "extent", "get_center", "get_extent"]
A = {n: hasattr(o3d.geometry.AxisAlignedBoundingBox, n) for n in names}
O = {n: hasattr(o3d.geometry.OrientedBoundingBox, n) for n in names}
print("AABB", A); print("OBB ", O)
print("BUG REPRODUCED: accessor sets differ" if A != O else "OK: consistent")
