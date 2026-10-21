"""Discussion 7175: use the VIEWPOINT field of a PCD file as a camera.
https://github.com/isl-org/Open3D/discussions/7175
Open3D's PCD reader parses VIEWPOINT but does not expose it, so we read it from
the ASCII header and build the extrinsic for project_to_rgbd_image."""
import os, tempfile
import numpy as np
import open3d as o3d

print("open3d", o3d.__version__)

def read_pcd_viewpoint(path):
    """Return the 4x4 sensor pose (sensor -> cloud frame) from a PCD header."""
    with open(path, "rb") as f:
        for raw in f:
            line = raw.decode("ascii", "ignore").strip()
            if line.startswith("VIEWPOINT"):
                tx, ty, tz, qw, qx, qy, qz = map(float, line.split()[1:8])
                pose = np.eye(4)
                pose[:3, :3] = o3d.geometry.get_rotation_matrix_from_quaternion([qw, qx, qy, qz])
                pose[:3, 3] = [tx, ty, tz]
                return pose
            if line.startswith("DATA"):
                break
    return np.eye(4)

# --- build a test PCD: a colored plane 2 m in front of a sensor at a known pose
xs, ys = np.meshgrid(np.linspace(-1, 1, 200), np.linspace(-1, 1, 200))
pts_sensor = np.stack([xs.ravel(), ys.ravel(), np.full(xs.size, 2.0)], 1)
R = o3d.geometry.get_rotation_matrix_from_xyz([0.3, -0.5, 0.2])
q = [0.0] * 4
# quaternion (w, x, y, z) from R
m = R; w = np.sqrt(1 + np.trace(m)) / 2
q = [w, (m[2, 1] - m[1, 2]) / (4 * w), (m[0, 2] - m[2, 0]) / (4 * w), (m[1, 0] - m[0, 1]) / (4 * w)]
t = np.array([1.5, -0.7, 3.0])
pts_world = pts_sensor @ R.T + t
tmp = tempfile.mkdtemp()
path = os.path.join(tmp, "vp.pcd")
with open(path, "w") as f:
    f.write("# .PCD v0.7\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\n")
    f.write(f"WIDTH {len(pts_world)}\nHEIGHT 1\n")
    f.write("VIEWPOINT %g %g %g %.9f %.9f %.9f %.9f\n" % (*t, *q))
    f.write(f"POINTS {len(pts_world)}\nDATA ascii\n")
    np.savetxt(f, pts_world, fmt="%.6f")

# --- the actual answer
pcd = o3d.t.io.read_point_cloud(path)
print("attributes Open3D keeps:", list(pcd.point))
pcd.point.colors = o3d.core.Tensor(np.full((len(pts_world), 3), 0.5), o3d.core.float32)

pose = read_pcd_viewpoint(path)                 # sensor pose in the cloud frame
extrinsic = o3d.core.Tensor(np.linalg.inv(pose), o3d.core.float32)  # cloud -> camera
intrinsic = o3d.core.Tensor([[300, 0, 320], [0, 300, 240], [0, 0, 1]], o3d.core.float32)
rgbd = pcd.project_to_rgbd_image(640, 480, intrinsic, extrinsic,
                                 depth_scale=1000.0, depth_max=10.0)
depth = np.asarray(rgbd.depth.to_legacy())
valid = depth[depth > 0]
print("viewpoint pose recovered:", np.allclose(pose[:3, :3], R, atol=1e-5), np.allclose(pose[:3, 3], t))
print("valid depth pixels:", valid.size, "median depth (m): %.3f" % np.median(valid / 1000.0))
