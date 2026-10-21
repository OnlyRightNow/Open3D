"""Discussion 7127: t.geometry.TriangleMesh.fill_holes leaves small holes on a
ball-pivoting mesh. https://github.com/isl-org/Open3D/discussions/7127
Shows that removing the small disconnected pieces BPA leaves behind lets
fill_holes close most small holes."""
import collections
import numpy as np
import open3d as o3d

print("open3d", o3d.__version__)

def boundary_loops(mesh):
    """Group boundary edges (edges used by one triangle) into connected loops."""
    t = np.asarray(mesh.triangles)
    e = np.sort(np.concatenate([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]]), 1)
    u, c = np.unique(e, axis=0, return_counts=True)
    adj = collections.defaultdict(list)
    for a, b in u[c == 1]:
        adj[a].append(b); adj[b].append(a)
    seen, loops = set(), []
    for s in adj:
        if s in seen:
            continue
        stack, comp = [s], []
        seen.add(s)
        while stack:
            x = stack.pop(); comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); stack.append(y)
        loops.append(comp)
    return loops

def fill(mesh):
    t = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
    return t.fill_holes(hole_size=1e6).to_legacy()

def keep_largest_component(mesh):
    mesh = o3d.geometry.TriangleMesh(mesh)
    ids, counts, _ = mesh.cluster_connected_triangles()
    ids, counts = np.asarray(ids), np.asarray(counts)
    mesh.remove_triangles_by_mask(ids != counts.argmax())
    mesh.remove_unreferenced_vertices()
    return mesh

# Same pipeline as in the question, on the Stanford bunny.
src = o3d.io.read_triangle_mesh(o3d.data.BunnyMesh().path)
pcd = src.sample_points_uniformly(20000)
radius = 0.5 * np.mean(pcd.compute_nearest_neighbor_distance())
pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=4 * radius, max_nn=30))
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector([radius * 2 ** k for k in range(6)]))
mesh.remove_degenerate_triangles(); mesh.remove_duplicated_triangles()
mesh.remove_non_manifold_edges(); mesh.remove_unreferenced_vertices()

print("BPA connected pieces:", len(np.asarray(mesh.cluster_connected_triangles()[1])))
print("non-manifold vertices:", len(mesh.get_non_manifold_vertices()))
before = len(boundary_loops(mesh))
after = len(boundary_loops(fill(mesh)))
print(f"fill_holes on raw BPA mesh: {before} boundary loops -> {after}")

clean = keep_largest_component(mesh)
b, a = boundary_loops(clean), boundary_loops(fill(clean))
small = lambda ls: sum(len(l) <= 10 for l in ls)
print(f"largest piece only: {len(b)} loops -> {len(a)}; "
      f"small loops (<=10 vertices) {small(b)} -> {small(a)}")
