"""https://github.com/isl-org/Open3D/issues/4976
FastGlobalRegistrationOption decrease_mu default is set to False in Python.
Expected: True (graduated non-convexity, and C++ default is true). Actual: False in Python bindings.
Verdict: CONFIRMED (cpp/pybind/pipelines/registration/registration.cpp: "decrease_mu"_a = false vs FastGlobalRegistration.h default true).
"""
import open3d as o3d
v = o3d.pipelines.registration.FastGlobalRegistrationOption().decrease_mu
print("default decrease_mu =", v)
print("BUG REPRODUCED: Python default decrease_mu is False (C++ default is True)" if not v else "OK: default True")
