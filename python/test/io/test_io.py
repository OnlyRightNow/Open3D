# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2026 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import open3d as o3d
import numpy as np
import pytest


def test_in_memory_xyz():
    # Reading/Writing bytes from bytes object
    pcb0 = b"1.0000000000 2.0000000000 3.0000000000\n4.0000000000 5.0000000000 6.0000000000\n7.0000000000 8.0000000000 9.0000000000\n"
    pc0 = o3d.io.read_point_cloud_from_bytes(pcb0, "mem::xyz")
    assert len(pc0.points) == 3
    pcb1 = o3d.io.write_point_cloud_to_bytes(pc0, "mem::xyz")
    assert len(pcb1) == len(pcb0)
    pc1 = o3d.io.read_point_cloud_from_bytes(pcb1, "mem::xyz")
    assert len(pc1.points) == 3
    # Reading/Writing bytes from PointCloud
    pc2 = o3d.geometry.PointCloud()
    pc2_points = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
    pc2.points = o3d.utility.Vector3dVector(pc2_points)
    pcb2 = o3d.io.write_point_cloud_to_bytes(pc2, "mem::xyz")
    assert len(pcb2) == len(pcb0)
    pc3 = o3d.io.read_point_cloud_from_bytes(pcb2, "mem::xyz")
    assert len(pc3.points) == 3
    np.testing.assert_allclose(np.asarray(pc3.points), pc2_points)


@pytest.mark.parametrize("data_type", ["ascii", "binary"])
def test_t_read_pcd_with_padding_fields(tmp_path, data_type):
    # PCL padding fields named "_" must be skipped (issue #6437).
    header = ("# .PCD v0.7\nVERSION 0.7\nFIELDS x y z _ intensity _\n"
              "SIZE 4 4 4 1 4 2\nTYPE F F F U F U\nCOUNT 1 1 1 4 1 3\n"
              "WIDTH 2\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS 2\n"
              f"DATA {data_type}\n").encode()
    xyz = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)
    intensity = np.array([7, 8], dtype=np.float32)
    if data_type == "ascii":
        body = b"1 2 3 0 0 0 0 7 0 0 0\n4 5 6 0 0 0 0 8 0 0 0\n"
    else:
        rec = np.zeros(2,
                       dtype=[("xyz", "<f4", 3), ("pad1", "u1", 4),
                              ("intensity", "<f4"), ("pad2", "<u2", 3)])
        rec["xyz"] = xyz
        rec["intensity"] = intensity
        body = rec.tobytes()
    path = tmp_path / f"padding_{data_type}.pcd"
    path.write_bytes(header + body)

    pcd = o3d.t.io.read_point_cloud(str(path))
    assert "_" not in pcd.point
    np.testing.assert_allclose(pcd.point.positions.numpy(), xyz)
    np.testing.assert_allclose(pcd.point.intensity.numpy().ravel(), intensity)
