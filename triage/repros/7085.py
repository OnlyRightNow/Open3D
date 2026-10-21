"""https://github.com/isl-org/Open3D/issues/7085 - Flood of 'getValue assumes leaf node' warnings after Poisson
Expected: no console flood, or at least suppressed by set_verbosity_level(Error). Actual: hundreds of PoissonRecon
WARN lines at low depth, ignoring Open3D verbosity. Verdict on 0.20: CONFIRMED. Root cause: 3rdparty PoissonRecon
WARN macro (FEMTree.Evaluation.inl) prints directly, not routed through utility::Log
(geometry/SurfaceReconstructionPoisson.cpp)."""
import subprocess, sys
code = '''
import open3d as o3d
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)
p=o3d.geometry.TriangleMesh.create_torus().sample_points_poisson_disk(5000); p.estimate_normals(); p.orient_normals_consistent_tangent_plane(10)
o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(p,depth=3)
'''
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
n = (r.stdout + r.stderr).count("getValue assumes leaf node")
print(f"BUG REPRODUCED: {n} 'getValue assumes leaf node' warnings despite VerbosityLevel.Error" if n else "OK: no warnings")
