"""https://github.com/isl-org/Open3D/issues/5805
Segfault when integrating few depth images with new reconstruction system
Expected: integrating only 1-2 frames into a VoxelBlockGrid without a 'color' attribute (the example's
default, integrate_color=False) and extracting returns an empty point cloud / mesh (weight_threshold=3).
Actual (0.20, CPU): extract_point_cloud()/extract_triangle_mesh() raise
"Tensor has shape {0}, but is expected to have compatible with {None, 3}" (an uncaught C++ exception ->
abort in C++; in 0.16 the reporter saw "Aborted (core dumped)").
Root cause: t/geometry/VoxelBlockGrid.cpp ExtractPointCloud/ExtractTriangleMesh: the guard
`colors.GetLength() == normals.GetLength()` is true when both are 0 though `colors` is an empty {0} tensor.
Verdict: CONFIRMED
"""
import numpy as np, open3d as o3d
c = o3d.core
intr = c.Tensor([[525., 0, 319.5], [0, 525., 239.5], [0, 0, 1]], c.float64)
vbg = o3d.t.geometry.VoxelBlockGrid(attr_names=('tsdf', 'weight'), attr_dtypes=(c.float32, c.float32),
        attr_channels=((1), (1)), voxel_size=3.0 / 512, block_resolution=16, block_count=10000, device=c.Device("CPU:0"))
ext = c.Tensor(np.eye(4))
xx = np.mgrid[0:480, 0:640][1]
for i in range(2):  # fewer than 3 frames -> all voxel weights < default weight_threshold 3
    depth = o3d.t.geometry.Image(c.Tensor((1500 + 300 * np.sin(xx / 60.0 + i)).astype(np.uint16)))
    fb = vbg.compute_unique_block_coordinates(depth, intr, ext, 1000.0, 3.0)
    vbg.integrate(fb, depth, intr, ext, 1000.0, 3.0)
errs = []
for f in ("extract_point_cloud", "extract_triangle_mesh"):
    try:
        g = getattr(vbg, f)()
        print(f, "ok, empty result:", g)
    except Exception as e:
        errs.append(f); print(f, "raised:", str(e).splitlines()[0][:200])
print("BUG REPRODUCED: empty extraction from color-less VoxelBlockGrid raises: " + ", ".join(errs) if errs
      else "OK: empty extraction handled")
