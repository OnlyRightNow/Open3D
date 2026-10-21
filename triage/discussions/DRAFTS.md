# Discussion answer drafts (Open3D Q&A)

Generated 2026-10-21. Read-only on GitHub; nothing was posted.

## Selection summary

- Listing method: the GraphQL step was replaced by WebFetch on github.com HTML pages
  (Q&A category with `is:unanswered`, plus `discussions?discussions_q=created:>=2026-07-23`).
- **Strict result: 0 Q&A discussions were opened on or after 2026-07-23.** The only
  discussions in that window are #7564 (General, release announcement), #7548
  (General, ARM build, author last active 2026-09-05) and #7532 (Ideas). The newest
  unanswered Q&A is #7483 (2026-04-29), and it already has a correct reply (capCafu,
  2026-09-05: zero normals plus lit shader).
- Activity check: `https://github.com/users/<user>/contributions` (public contribution
  calendar). This does not count discussion posts or private work, so it can miss
  some active users.
- **Fallback (outside the 90-day window, labeled as such):** older unanswered Q&A
  with no replies, author active in the last 30 days, testable on CPU Linux without a
  GUI. Two qualified. Other recent unanswered Q&A were dropped: GUI-only (#7462,
  #7389, #7356, #7261, #7247, #7171, #7142), Windows-only (#7457), not testable /
  advisory (#7304, #7357, #7408), or author inactive (#7395,
  #7131, #7078, #7057, #7035, #7018, #7221).

---

### https://github.com/isl-org/Open3D/discussions/7175 - [Question] Is there a way to be able to read the viewpoint field of a PCD file for instantiating a camera in it?
- Outside the 90-day window (opened 2025-02-20), 0 replies.
- Why the author will likely respond: davidelahoz has public contributions on 2026-09-24 (within 30 days), the question has had no reply at all, and the answer gives working code for exactly their goal (`project_to_rgbd_image` from the PCD viewpoint).
- Test status: `scripts/d7175_pcd_viewpoint.py` (log: `d7175_pcd_viewpoint.log`) on open3d-cpu 0.20.0 printed:
  `attributes Open3D keeps: ['positions']`, `viewpoint pose recovered: True True`, `valid depth pixels: 40000 median depth (m): 2.000` (plane placed 2 m in front of a rotated, translated sensor pose written to VIEWPOINT).
- Source check: `cpp/open3d/t/io/file_format/FilePCD.cpp` and `cpp/open3d/io/file_format/FilePCD.cpp` parse the VIEWPOINT line into a local header struct and never use it; the writer always writes `VIEWPOINT 0 0 0 1 0 0 0`. Limitation, not a bug.

Answer (ready to paste):

Not directly. Open3D (checked on 0.20) reads the VIEWPOINT line of a PCD header but throws it away, so it is not available on the point cloud. The header is plain text even for binary PCD files, so you can read it yourself and turn it into the extrinsic for `project_to_rgbd_image`.

VIEWPOINT is `tx ty tz qw qx qy qz`, the sensor pose in the cloud frame. The extrinsic Open3D wants is the inverse of that pose (cloud to camera):

```python
import numpy as np
import open3d as o3d

def read_pcd_viewpoint(path):
    with open(path, "rb") as f:
        for raw in f:
            line = raw.decode("ascii", "ignore").strip()
            if line.startswith("VIEWPOINT"):
                tx, ty, tz, qw, qx, qy, qz = map(float, line.split()[1:8])
                pose = np.eye(4)
                pose[:3, :3] = o3d.geometry.get_rotation_matrix_from_quaternion([qw, qx, qy, qz])
                pose[:3, 3] = [tx, ty, tz]
                return pose
            if line.startswith("DATA"):
                break
    return np.eye(4)

pcd = o3d.t.io.read_point_cloud("cloud.pcd")   # needs colors for the RGB part
pose = read_pcd_viewpoint("cloud.pcd")
extrinsic = o3d.core.Tensor(np.linalg.inv(pose), o3d.core.float32)
intrinsic = o3d.core.Tensor([[300, 0, 320], [0, 300, 240], [0, 0, 1]], o3d.core.float32)
rgbd = pcd.project_to_rgbd_image(640, 480, intrinsic, extrinsic,
                                 depth_scale=1000.0, depth_max=10.0)
```

I tested this with a plane placed 2 m in front of a rotated and shifted sensor. The depth image came out with a median of 2.000 m, so the pose and the inverse are right.

Two things to watch. Open3D's camera looks along +Z with +Y down, so if your scanner uses a different axis convention, multiply the pose by a fixed axis-swap rotation. Also, `project_to_rgbd_image` is a plain z-buffer projection into a pinhole image. For a 360 degree "bubble view" like CloudCompare you would need several of these (for example six cube faces) from the same viewpoint.

- Docs: https://www.open3d.org/docs/release/python_api/open3d.t.geometry.PointCloud.html#open3d.t.geometry.PointCloud.project_to_rgbd_image
- Where VIEWPOINT is parsed and dropped: https://github.com/isl-org/Open3D/blob/main/cpp/open3d/t/io/file_format/FilePCD.cpp

If this solves it, feel free to mark it as the answer.

---

### https://github.com/isl-org/Open3D/discussions/7127 - Cannot fill small holes in mesh
- Outside the 90-day window (opened 2025-01-05, asked on 0.18), 0 replies.
- Why the author will likely respond: olkham is very active (public contributions almost daily through 2026-10-20), nobody has replied, and the answer explains why their exact pipeline leaves holes and gives a concrete pre-processing step that measurably helps.
- Test status: `scripts/d7127_fill_holes.py` (log: `d7127_fill_holes.log`) on open3d-cpu 0.20.0 reproduces their pipeline (bunny, BPA with doubling radii, same cleanup, `fill_holes(1e6)`) and printed:
  `BPA connected pieces: 224`, `non-manifold vertices: 322`, `fill_holes on raw BPA mesh: 208 boundary loops -> 74`, `largest piece only: 11 loops -> 4; small loops (<=10 vertices) 10 -> 3`.
  Numbers vary a little run to run because the point sampling is random. Side probes (not kept) showed `fill_holes` fully closes clean holes on a sphere, and that a loose two-triangle piece gets "filled" with back faces, which adds a non-manifold edge.
- Source check: `TriangleMesh::FillHoles` in `cpp/open3d/t/geometry/TriangleMesh.cpp` is a thin wrapper around VTK's `vtkFillHolesFilter`. Limitation of the approach, not an Open3D bug.

Answer (ready to paste):

Most of the leftover holes come from the shape of the ball pivoting output, not from the hole size. `fill_holes` is a thin wrapper around VTK's `vtkFillHolesFilter`. It works well on clean, manifold holes. BPA output usually has hundreds of tiny loose pieces and many non-manifold vertices (two holes touching at one vertex). The filter treats the border of every loose piece as a hole, and it often gives up on loops that pass through a non-manifold vertex.

I reproduced your pipeline on the Stanford bunny with Open3D 0.20. The BPA mesh had about 220 separate pieces and about 320 non-manifold vertices. `fill_holes(1e6)` on it left 74 of 208 boundary loops open. Keeping only the main piece first made a clear difference: 11 loops went down to 4, and most of the small holes closed.

```python
import numpy as np
import open3d as o3d

def keep_largest_component(mesh):
    ids, counts, _ = mesh.cluster_connected_triangles()
    ids, counts = np.asarray(ids), np.asarray(counts)
    mesh.remove_triangles_by_mask(ids != counts.argmax())
    mesh.remove_unreferenced_vertices()
    return mesh

# mesh = your cleaned BPA mesh
mesh = keep_largest_component(mesh)
print("non-manifold vertices:", len(mesh.get_non_manifold_vertices()))
filled = o3d.t.geometry.TriangleMesh.from_legacy(mesh).fill_holes(hole_size=1e6).to_legacy()
```

If your object really has several parts, drop pieces below a triangle count instead of keeping only the largest one.

To be honest about the limit: holes whose border runs through a non-manifold vertex can still stay open, and Open3D has no built-in step to split those vertices.

- `fill_holes` docs: https://www.open3d.org/docs/release/python_api/open3d.t.geometry.TriangleMesh.html#open3d.t.geometry.TriangleMesh.fill_holes
- Implementation: https://github.com/isl-org/Open3D/blob/main/cpp/open3d/t/geometry/TriangleMesh.cpp (`TriangleMesh::FillHoles`)

If this solves it, feel free to mark it as the answer.
