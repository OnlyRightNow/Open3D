"""https://github.com/isl-org/Open3D/issues/7592
ScalableTSDFVolume produces empty geometry from metric float32 depth.
Expected: integrating a 2 m float32 depth plane (depth_scale=1) yields a non-empty mesh/point cloud.
Actual (0.20): empty output (float depth scaled twice: activation path uses depth_scale 1000).
Verdict: CONFIRMED
"""
import numpy as np
import open3d as o3d

w, h = 64, 48
depth = o3d.geometry.Image(np.full((h, w), 2.0, dtype=np.float32))
color = o3d.geometry.Image(np.full((h, w, 3), 128, dtype=np.uint8))
rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
    color, depth, depth_scale=1.0, depth_trunc=4.0, convert_rgb_to_intensity=False)
intr = o3d.camera.PinholeCameraIntrinsic(w, h, 50.0, 50.0, w / 2, h / 2)
direct = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intr)
vol = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=0.02, sdf_trunc=0.08,
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
vol.integrate(rgbd, intr, np.eye(4))
n_pts = len(vol.extract_point_cloud().points)
n_vox = len(vol.extract_voxel_point_cloud().points)
print("direct backprojection points:", len(direct.points))
print("tsdf points:", n_pts, "voxel points:", n_vox)
if len(direct.points) > 0 and n_pts == 0:
    print("BUG REPRODUCED: ScalableTSDFVolume output is empty for metric float32 depth")
else:
    print("OK: ScalableTSDFVolume produced geometry")
