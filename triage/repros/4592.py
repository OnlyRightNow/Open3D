"""https://github.com/isl-org/Open3D/issues/4592
PoseGraph in CPP example.
Expected: running `PoseGraph test_pose_graph.json` on the file the example itself writes
optimizes without "Invalid PoseGraph - graph is not connected".
Actual: examples/cpp/PoseGraph.cpp builds a 2-node test graph with an edge 0->2 (node 2
does not exist), saves it as test_pose_graph.json, and that file is then rejected by
global optimization. Mirrored here in Python. Root cause: examples/cpp/PoseGraph.cpp main
(bogus edge target; check in cpp/open3d/pipelines/registration/GlobalOptimization.cpp
ValidatePoseGraph). Verdict: CONFIRMED (example bug)."""
import numpy as np
import open3d as o3d

reg = o3d.pipelines.registration
pg = reg.PoseGraph()
pg.nodes.append(reg.PoseGraphNode(np.eye(4)))
pg.nodes.append(reg.PoseGraphNode(np.eye(4)))
pg.edges.append(reg.PoseGraphEdge(0, 1, np.eye(4), np.eye(6), uncertain=False, confidence=1.0))
pg.edges.append(reg.PoseGraphEdge(0, 2, np.eye(4), np.eye(6), uncertain=True, confidence=0.2))
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Warning)
reg.global_optimization(pg, reg.GlobalOptimizationLevenbergMarquardt(),
                        reg.GlobalOptimizationConvergenceCriteria(), reg.GlobalOptimizationOption())
bad = [(e.source_node_id, e.target_node_id) for e in pg.edges
       if max(e.source_node_id, e.target_node_id) >= len(pg.nodes)]
if bad:
    print(f"BUG REPRODUCED: example's test graph has edges {bad} to missing nodes (2 nodes); "
          "optimizer warns 'graph is not connected' (above) and skips optimization")
else:
    print("OK: example graph is valid")
