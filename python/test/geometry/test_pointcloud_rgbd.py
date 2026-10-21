# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2026 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import numpy as np
import open3d as o3d
import pytest


def _create_from_rgbd(color, convert_rgb_to_intensity=False):
    """Project a 4x4 color image with uniform depth 1 to a point cloud."""
    depth = o3d.geometry.Image(np.ones((4, 4), np.float32))
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(color),
        depth,
        depth_scale=1.0,
        depth_trunc=1000.0,
        convert_rgb_to_intensity=convert_rgb_to_intensity)
    return o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd, o3d.camera.PinholeCameraIntrinsic(4, 4, 2, 2, 2, 2))


@pytest.mark.parametrize("channels", [3, 4])
def test_create_from_rgbd_image_color_channels(channels):
    """RGB and RGBA colors map to RGB; alpha is ignored (issue #5788)."""
    rgba = np.array([10, 100, 200, 255], np.uint8)
    color = np.ascontiguousarray(np.tile(rgba[:channels], (4, 4, 1)))
    pcd = _create_from_rgbd(color)
    np.testing.assert_allclose(np.asarray(pcd.colors),
                               np.tile([10, 100, 200], (16, 1)) / 255.0)


def test_create_from_rgbd_image_intensity():
    """Single channel intensity is replicated to gray."""
    pcd = _create_from_rgbd(np.full((4, 4, 3), 128, np.uint8),
                            convert_rgb_to_intensity=True)
    colors = np.asarray(pcd.colors)
    np.testing.assert_allclose(colors, np.full((16, 3), 128 / 255.0), atol=1e-6)
