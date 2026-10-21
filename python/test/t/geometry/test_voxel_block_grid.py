# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2026 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import open3d as o3d
import open3d.core as o3c
import numpy as np
import pytest

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
from open3d_test import list_devices


@pytest.mark.parametrize("device", list_devices())
def test_extract_empty_without_color(device):
    """Empty extraction from a grid without colors returns empty geometry.

    Regression test for issue #5805.
    """
    vbg = o3d.t.geometry.VoxelBlockGrid(attr_names=("tsdf", "weight"),
                                        attr_dtypes=(o3c.float32, o3c.float32),
                                        attr_channels=((1), (1)),
                                        voxel_size=3.0 / 512,
                                        block_resolution=8,
                                        block_count=10000,
                                        device=device)
    intrinsic = o3c.Tensor([[525.0, 0, 319.5], [0, 525.0, 239.5], [0, 0, 1]],
                           o3c.float64)
    extrinsic = o3c.Tensor(np.eye(4))
    # Plane at 1.503 m (not on a voxel boundary).
    depth = o3d.t.geometry.Image(
        o3c.Tensor(np.full((480, 640), 1503, np.uint16))).to(device)
    coords = vbg.compute_unique_block_coordinates(depth, intrinsic, extrinsic,
                                                  1000.0, 3.0)
    vbg.integrate(coords, depth, intrinsic, extrinsic, 1000.0, 3.0)

    # A surface exists and has no colors.
    pcd = vbg.extract_point_cloud(weight_threshold=0.0)
    assert len(pcd.point.positions) > 0
    assert "colors" not in pcd.point

    # One frame gives weight 1 < default threshold 3, so the result is empty.
    pcd = vbg.extract_point_cloud()
    assert len(pcd.point.positions) == 0
    assert "colors" not in pcd.point
    mesh = vbg.extract_triangle_mesh()
    assert len(mesh.vertex.positions) == 0
    assert len(mesh.triangle.indices) == 0
    assert "colors" not in mesh.vertex
