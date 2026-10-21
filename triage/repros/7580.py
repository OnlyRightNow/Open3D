"""https://github.com/isl-org/Open3D/issues/7580
TSDF Integrate truncates the depth lookup (static_cast<index_t>(u)) although Project() uses
pixel-center convention, biasing samples by ~0.5 px.
Expected: TSDF surface of a tilted plane lies on the plane (mean signed error ~0).
Actual (0.20): systematic bias; feeding a depth image pre-shifted by +0.5 px removes most of it.
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d
import open3d.core as o3c

W, H, f = 160, 120, 100.0
cx, cy = W / 2, H / 2
k = 1.0  # plane z = 1 + k*x (strong tilt)
K = o3c.Tensor([[f, 0, cx], [0, f, cy], [0, 0, 1]], o3c.float64)
E = o3c.Tensor(np.eye(4), o3c.float64)


def depth_image(shift):
    u = np.arange(W)[None, :] + shift + 0 * np.arange(H)[:, None]
    z = 1.0 / (1.0 - k * (u - cx) / f)
    return o3d.t.geometry.Image(o3c.Tensor(z.astype(np.float32)))


def mean_err(shift):
    vbg = o3d.t.geometry.VoxelBlockGrid(("tsdf", "weight"), (o3c.float32, o3c.float32),
                                        ((1), (1)), 0.004, 16, 20000, o3c.Device("CPU:0"))
    d = depth_image(shift)
    blocks = vbg.compute_unique_block_coordinates(d, K, E, 1.0, 3.0)
    vbg.integrate(blocks, d, K, E, 1.0, 3.0)
    p = vbg.extract_point_cloud(weight_threshold=0.5).point.positions.numpy()
    p = p[np.abs(p[:, 0]) < 0.3]
    return np.mean(p[:, 2] - (1 + k * p[:, 0])), len(p)


e0, n0 = mean_err(0.0)
e1, n1 = mean_err(0.5)
print(f"exact depth image:          mean signed z error = {e0*1000:.3f} mm ({n0} pts)")
print(f"depth sampled at u+0.5 px:  mean signed z error = {e1*1000:.3f} mm ({n1} pts)")
if abs(e0) > 3 * abs(e1):
    print("BUG REPRODUCED: truncating depth lookup biases TSDF surface by ~half a pixel")
else:
    print("OK: no half-pixel bias detected")
