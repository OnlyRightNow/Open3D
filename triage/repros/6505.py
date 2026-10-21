"""https://github.com/isl-org/Open3D/issues/6505
KDTreeFlann built from an Eigen matrix does not work like one built from a PointCloud.
Expected: KDTreeFlann(MatrixXd of N points) == KDTreeFlann(PointCloud) for searches.
Actual: the matrix constructor treats each COLUMN as a point (dim x N layout). An N x 3 matrix
(as from igl::barycenter) silently builds an N-dimensional tree; in C++ SearchRadius returns
empty, in Python it raises. The layout is not documented. Root cause:
cpp/open3d/geometry/KDTreeFlann.h/.cpp KDTreeFlann(const Eigen::MatrixXd&)/SetMatrixData
(undocumented dim x N convention, no warning). Verdict: CONFIRMED (docs/validation)."""
import numpy as np
import open3d as o3d

P = np.random.rand(500, 3)
ref = o3d.geometry.KDTreeFlann(o3d.geometry.PointCloud(o3d.utility.Vector3dVector(P)))
n_ref = ref.search_radius_vector_3d(P[0], 0.2)[0]
n_t = o3d.geometry.KDTreeFlann(P.T.copy()).search_radius_vector_3d(P[0], 0.2)[0]
try:
    n_nx3 = o3d.geometry.KDTreeFlann(P).search_radius_vector_3d(P[0], 0.2)[0]
except RuntimeError as e:
    n_nx3 = f"error: {e}"
if n_nx3 != n_ref:
    print(f"BUG REPRODUCED: N x 3 matrix tree -> {n_nx3!r}; 3 x N -> {n_t}; PointCloud -> {n_ref}")
else:
    print("OK: matrix and point cloud trees agree")
