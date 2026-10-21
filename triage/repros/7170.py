"""https://github.com/isl-org/Open3D/issues/7170 - t.geometry.TriangleMesh.boolean_intersection hangs forever
Expected: returns (or raises) for two box meshes. Actual: never returns (VTK vtkBooleanOperationPolyDataFilter
loops on near-coplanar faces). Verdict on 0.20: CONFIRMED (subprocess killed after 30 s)."""
import subprocess, sys
code = '''
import open3d as o3d
Ra=[[0.7763932909764589,0.6302487268743537,0],[-0.6302487268743537,0.7763932909764589,0],[0,0,1]]
Rb=[[0.932249806137092,-0.3618152829239726,0],[0.3618152829239726,0.932249806137092,0],[0,0,1]]
a=o3d.geometry.OrientedBoundingBox([1.6146446239451142,0.28286344833944177,0.007205603424467633],Ra,[0.11741286554647978,0.05476615015653086,0.014411206848935265])
b=o3d.geometry.OrientedBoundingBox([1.6095394270157695,0.3750636665091013,0.006781576251261745],Rb,[0.12141223692202752,0.07709698213053162,0.01356315250252349])
f=lambda o:o3d.t.geometry.TriangleMesh.from_legacy(o3d.geometry.TriangleMesh.create_from_oriented_bounding_box(o))
print(f(a).boolean_intersection(f(b)))
'''
try:
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    print(f"OK: returned ({r.returncode}) {r.stdout.strip()}")
except subprocess.TimeoutExpired:
    print("BUG REPRODUCED: boolean_intersection did not return within 30 s")
