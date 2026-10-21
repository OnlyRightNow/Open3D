"""https://github.com/isl-org/Open3D/issues/6697
doppler_icp exception.
Expected: `open3d example pipelines/doppler_icp_registration` runs on a default install.
Actual: ModuleNotFoundError: No module named 'pyquaternion' -- the bundled example imports
pyquaternion, which is only an optional ML extra (python/open3d/_optional_deps.py).
Root cause: examples/python/pipelines/doppler_icp_registration.py (top-level import;
could use o3d.geometry.get_rotation_matrix_from_quaternion). Verdict: CONFIRMED."""
import importlib.util, os, subprocess, sys
import open3d

ex = os.path.join(os.path.dirname(open3d.__file__), "examples", "pipelines", "doppler_icp_registration.py")
src = open(ex).read()
if "pyquaternion" in src and importlib.util.find_spec("pyquaternion") is None:
    r = subprocess.run([sys.executable, "-c", "import runpy,sys; runpy.run_path(sys.argv[1])", ex],
                       capture_output=True, text=True, timeout=120)
    err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
    print(f"BUG REPRODUCED: bundled example fails without optional dep: {err}")
else:
    print("OK: example does not need pyquaternion (or it is installed)")
