"""https://github.com/isl-org/Open3D/issues/5282
o3d.pipelines.integration.ScalableTSDFVolume does not work with copy.deepcopy
Expected: deepcopy yields an independent volume. Actual: ScalableTSDFVolume's implicit copy ctor
(bound via bind_copy_functions) copies volume_units_ whose VolumeUnit::volume_ is a
std::shared_ptr<UniformTSDFVolume>, so the "deep" copy shares voxel data with the original.
NOTE: in 0.20 ScalableTSDFVolume::Integrate is additionally broken for normal scenes (it calls
PointCloud::CreateFromDepthImage on the already-metric float depth with depth_scale=1000, which since
#7540 now divides float depth by 1000 -> volume units are allocated ~1mm from the camera).
To work around it here we use voxel_length=0.1 (unit = 1.6m) so the unit at the origin contains the surface.
Verdict: CONFIRMED
"""
import copy, numpy as np, open3d as o3d
I = o3d.pipelines.integration
h, w = 48, 64
intr = o3d.camera.PinholeCameraIntrinsic(w, h, 50, 50, w / 2, h / 2)
def rgbd(mm):
    return o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(np.full((h, w, 3), 128, np.uint8)), o3d.geometry.Image(np.full((h, w), mm, np.uint16)),
        convert_rgb_to_intensity=False)
def tsdf_sum(v):
    return float(np.asarray(v.extract_voxel_point_cloud().colors).sum())  # colors encode tsdf
vol = I.ScalableTSDFVolume(voxel_length=0.1, sdf_trunc=0.3, color_type=I.TSDFVolumeColorType.NoColor)
vol.integrate(rgbd(1000), intr, np.eye(4))
before = (len(vol.extract_voxel_point_cloud().points), tsdf_sum(vol))
vol2 = copy.deepcopy(vol)
vol2.integrate(rgbd(1200), intr, np.eye(4))
after = (len(vol.extract_voxel_point_cloud().points), tsdf_sum(vol))
print("original before:", before, "original after integrating into copy:", after)
if before[0] == 0:
    print("Inconclusive: nothing integrated")
elif before != after:
    print("BUG REPRODUCED: integrating into deepcopy modified the original ScalableTSDFVolume")
else:
    print("OK: deepcopy is independent")
