"""https://github.com/isl-org/Open3D/issues/6096
compute_fpfh_feature hanging if executed inside a multiprocessing.Process.
Expected: completes in a forked child, also after running in the parent first.
Actual on 0.20 (fork start method): child finishes with exit code 0. Verdict: FIXED."""
import multiprocessing as mp
import open3d as o3d
def f(p):
    o3d.pipelines.registration.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=100))
if __name__ == "__main__":
    pcd = o3d.geometry.TriangleMesh.create_sphere().sample_points_uniformly(5000); pcd.estimate_normals()
    f(pcd)  # parent first
    p = mp.get_context("fork").Process(target=f, args=(pcd,)); p.start(); p.join(60)
    if p.is_alive():
        p.kill(); print("BUG REPRODUCED: child hung")
    else:
        print("OK: child exit code %s" % p.exitcode)
