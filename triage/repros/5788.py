"""https://github.com/isl-org/Open3D/issues/5788
Wrong point cloud color when using RGBA images.
Expected: RGBA (10,100,200,255) gives color (10,100,200), same as RGB input.
Actual: blue = alpha (255); channels are read as pc[0], pc[(NC-1)/2], pc[NC-1], which for NC=4 is R, G, A.
Verdict: CONFIRMED (cpp/open3d/geometry/PointCloudFactory.cpp: CreatePointCloudFromRGBDImageT)."""
import numpy as np
import open3d as o3d
rgb = np.zeros((4, 4, 3), np.uint8); rgb[..., 0], rgb[..., 1], rgb[..., 2] = 10, 100, 200
rgba = np.ascontiguousarray(np.dstack([rgb, np.full((4, 4, 1), 255, np.uint8)]))
im = o3d.geometry.RGBDImage.create_from_color_and_depth(
    o3d.geometry.Image(rgba), o3d.geometry.Image(np.ones((4, 4), np.float32)),
    depth_scale=1, depth_trunc=1000, convert_rgb_to_intensity=False)
pc = o3d.geometry.PointCloud.create_from_rgbd_image(im, o3d.camera.PinholeCameraIntrinsic(4, 4, 2, 2, 2, 2))
c = np.round(np.asarray(pc.colors)[0] * 255)
print(("BUG REPRODUCED: color %s, expected [10 100 200]" % c) if not np.allclose(c, [10, 100, 200]) else "OK: correct color")
