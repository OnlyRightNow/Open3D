"""https://github.com/isl-org/Open3D/issues/5911
Open3D crashes when using boolean_intersection with non-overlapping meshes.
Expected: empty mesh for non-overlapping inputs, never a crash/hang.
Actual: reporter's knot convex-hull pipeline crashes (segfault) or hangs inside VTK boolean filter.
Verdict: see printed line (run in subprocess, crash detected by exit code)."""
import subprocess, sys, textwrap
code = textwrap.dedent('''
import copy, numpy as np, open3d as o3d
p = o3d.data.KnotMesh().path
m1 = o3d.t.geometry.TriangleMesh.from_legacy(o3d.io.read_triangle_mesh(p)); m1.translate([0,0,100])
m2 = o3d.t.geometry.TriangleMesh.from_legacy(o3d.io.read_triangle_mesh(p))
inter = m1.boolean_intersection(m2).to_legacy()
cid, n, _ = inter.cluster_connected_triangles()
meshes = []
for i in range(len(n)):
    m = copy.deepcopy(inter); m.remove_triangles_by_mask(np.array(cid) != i); m.remove_unreferenced_vertices()
    if len(m.vertices) > 3: meshes.append(m.compute_convex_hull()[0])
print("hulls", len(meshes), flush=True)
for i in range(len(meshes)):
    a = o3d.t.geometry.TriangleMesh.from_legacy(meshes[i])
    for j in range(i+1, len(meshes)):
        a.boolean_intersection(o3d.t.geometry.TriangleMesh.from_legacy(meshes[j]))
print("DONE", flush=True)
''')
try:
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    out = r.stdout.strip().splitlines()
    if r.returncode != 0:
        print(f"BUG REPRODUCED: subprocess exited with code {r.returncode}; last stdout: {out[-1:] }")
    else:
        print("OK: finished without crash:", out[-2:])
except subprocess.TimeoutExpired:
    print("BUG REPRODUCED: boolean_intersection hung (>120 s)")
