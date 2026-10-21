"""https://github.com/isl-org/Open3D/issues/6795
Saving and loading a VoxelBlockGrid with negative block indices -> errors on load and segfault in ray_cast.
Expected: loaded grid equals saved grid and ray_cast works.
Actual (0.20, CPU, synthetic plane spanning negative block coords): keys round-trip and ray_cast
matches the original grid; no errors or crash.
Verdict: FIXED
"""
import subprocess
import sys
import tempfile

CHILD = r'''
import numpy as np, open3d as o3d, open3d.core as o3c, sys
dev = o3c.Device("CPU:0")
K = o3c.Tensor([[500., 0, 320], [0, 500., 240], [0, 0, 1]], o3c.float64)
E_ = np.eye(4); E_[:3, 3] = (0.5, 0.5, 3.0)  # world-to-camera: plane at negative world x/y/z
E = o3c.Tensor(E_, o3c.float64)
depth = o3d.t.geometry.Image(o3c.Tensor(np.full((480, 640), 1.0, np.float32)))
vbg = o3d.t.geometry.VoxelBlockGrid(("tsdf", "weight"), (o3c.float32, o3c.float32), ((1), (1)),
                                    3 / 512, 8, 100000, dev)
blk = vbg.compute_unique_block_coordinates(depth, K, E, 1.0, 3.0)
vbg.integrate(blk, depth, K, E, 1.0, 3.0)
hm = vbg.hashmap(); keys = hm.key_tensor()[hm.active_buf_indices().to(o3c.int64)].numpy()
print("blocks:", len(keys), "min key:", keys.min(0))
vbg.save(sys.argv[1])
vbg2 = o3d.t.geometry.VoxelBlockGrid.load(sys.argv[1])
hm2 = vbg2.hashmap(); keys2 = hm2.key_tensor()[hm2.active_buf_indices().to(o3c.int64)].numpy()
print("loaded blocks:", len(keys2), "min key:", keys2.min(0))
same = sorted(map(tuple, keys)) == sorted(map(tuple, keys2))
blk2 = o3c.Tensor(keys2)
r0 = vbg.ray_cast(o3c.Tensor(keys), K, E, 640, 480, ["depth"], 1.0, 0.1, 3.0, 0.5)
print("ray_cast on original valid px:", int((r0["depth"].numpy() > 0).sum()))
r = vbg2.ray_cast(blk2, K, E, 640, 480, ["depth"], 1.0, 0.1, 3.0, 0.5)
d = r["depth"].numpy()
print("ray_cast valid depth px:", int((d > 0).sum()), "keys identical:", same)
ok_rc = (d > 0).sum() > 0 and (d > 0).sum() == (r0["depth"].numpy() > 0).sum()
sys.exit(0 if same and ok_rc else 3)
'''
with tempfile.TemporaryDirectory() as td:
    p = subprocess.run([sys.executable, "-c", CHILD, td + "/vbg.npz"], capture_output=True, text=True)
print(p.stdout.strip())
print(p.stderr.strip()[-800:])
if p.returncode == 0:
    print("OK: save/load with negative block coordinates round-trips and ray_cast works")
else:
    print(f"BUG REPRODUCED: child exit code {p.returncode}")
