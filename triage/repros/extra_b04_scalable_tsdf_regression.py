"""Not an upstream issue in batch b04 -- regression found while triaging #5282.
ScalableTSDFVolume.integrate produces an empty volume in 0.20 for ordinary data.
Root cause: ScalableTSDFVolume::Integrate (cpp/open3d/pipelines/integration/ScalableTSDFVolume.cpp)
calls PointCloud::CreateFromDepthImage(image.depth_ /*float, metres*/, ..., depth_scale=1000, depth_trunc=1000).
Commit fb693b6 (#7540, fix for #6347) made CreateFromDepthImage apply depth_scale to float images too,
so depths are divided by 1000 and volume units are allocated next to the camera, not at the surface.
UniformTSDFVolume on the same input works.
"""
import numpy as np, open3d as o3d
I = o3d.pipelines.integration
intr = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
    o3d.geometry.Image(np.full((480, 640, 3), 128, np.uint8)), o3d.geometry.Image(np.full((480, 640), 1011, np.uint16)),
    convert_rgb_to_intensity=False)
s = I.ScalableTSDFVolume(voxel_length=0.02, sdf_trunc=0.06, color_type=I.TSDFVolumeColorType.RGB8)
s.integrate(rgbd, intr, np.eye(4))
u = I.UniformTSDFVolume(length=4, resolution=128, sdf_trunc=0.06, color_type=I.TSDFVolumeColorType.RGB8, origin=[-2, -2, 0])
u.integrate(rgbd, intr, np.eye(4))
ns, nu = len(s.extract_point_cloud().points), len(u.extract_point_cloud().points)
print("scalable points:", ns, "uniform points:", nu)
print("BUG REPRODUCED: ScalableTSDFVolume integrates nothing" if ns == 0 and nu > 0 else "OK: ScalableTSDFVolume works")
