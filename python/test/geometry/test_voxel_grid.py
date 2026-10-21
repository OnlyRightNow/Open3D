# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2026 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import numpy as np
import open3d as o3d


def test_create_from_point_cloud_within_bounds_skips_outside_points():
    # Points outside the bounds are skipped; bounds are inclusive
    # (issues #2766, #4569).
    points = np.array([[0.1, 0.1, 0.1], [0.5, 0.5, 0.5], [5.0, 5.0, 5.0],
                       [-3.0, 0.0, 0.0], [0.1, 0.1, 0.6]])
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(
        pcd, voxel_size=0.25, min_bound=[-0.5] * 3, max_bound=[0.5] * 3)
    indices = sorted(v.grid_index.tolist() for v in voxel_grid.get_voxels())
    assert indices == [[2, 2, 2], [4, 4, 4]]


def test_create_from_point_cloud_keeps_all_points():
    rng = np.random.default_rng(0)
    points = rng.random((2000, 3)) * 3 - 1
    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, 0.05)
    assert all(voxel_grid.check_if_included(pcd.points))
