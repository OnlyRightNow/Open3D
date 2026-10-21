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
@pytest.mark.parametrize("dtype", [o3c.float32, o3c.float64])
def test_to_and_clone_keep_bounds(device, dtype):
    """to() and clone() keep bounds, color and dtype (issue #6721)."""
    aabb = o3d.t.geometry.AxisAlignedBoundingBox(
        o3c.Tensor([-3, -3, -3], dtype), o3c.Tensor([-1, -1, -1], dtype))
    moved = aabb.to(device, True)
    for box in (moved, moved.clone()):
        assert box.device == device
        assert box.min_bound.dtype == dtype
        assert box.max_bound.dtype == dtype
        assert box.color.dtype == dtype
        np.testing.assert_allclose(box.min_bound.cpu().numpy(), [-3, -3, -3])
        np.testing.assert_allclose(box.max_bound.cpu().numpy(), [-1, -1, -1])
