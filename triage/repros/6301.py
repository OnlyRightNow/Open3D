"""https://github.com/isl-org/Open3D/issues/6301
Inconsistent NaN handling in octree between arm64 and x86.
Expected: NaN points ignored (or error) consistently.
Actual (x86 too): if the first point is NaN, GetMinBound/GetMaxBound are NaN and the octree origin/size are NaN.
NaN in the middle is silently skipped only because SSE min/max return the non-NaN operand; NEON propagates NaN.
Verdict: CONFIRMED (cpp/open3d/geometry/Geometry3D.cpp: ComputeMinBound/ComputeMaxBound, used by Octree::ConvertFromPointCloud)."""
import numpy as np
import open3d as o3d
arr = np.random.rand(1000, 3); arr[0] = np.nan
pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(arr))
t = o3d.geometry.Octree(max_depth=3); t.convert_from_point_cloud(pc, size_expand=0.01)
print(("BUG REPRODUCED: %s" % t) if np.isnan(t.size) else "OK: %s" % t)
