"""https://github.com/isl-org/Open3D/issues/5913
Easy-to-Find Hash Value Collision with Negative Coordinates
Expected: distinct small integer 3D keys hash to distinct values (low collision rate).
Actual: FNV-1a in core/hashmap/Dispatch.h (MiniVecHash::operator()) XORs the full 64-bit
sign-extended int, so negative coords flip all upper bits and many keys collide.
This mirrors the C++ hash exactly in Python (the hash is not exposed in the Python API).
Verdict: CONFIRMED (performance-only; equality check keeps results correct)
"""
import numpy as np
M = (1 << 64) - 1
def h(key):  # exact copy of MiniVecHash<int,3>::operator()
    x = 14695981039346656037
    for k in key:
        x ^= (k & M)            # static_cast<uint64_t>(int) sign-extends
        x = (x * 1099511628211) & M
    return x
r = range(-30, 31)
keys = [(a, b, c) for a in r for b in r for c in r]
hs = {}
for k in keys: hs.setdefault(h(k), []).append(k)
coll = sum(len(v) - 1 for v in hs.values())
ex = next(v for v in hs.values() if len(v) > 1) if coll else None
pos = [(a, b, c) for a in range(61) for b in range(61) for c in range(61)]
coll_pos = len(pos) - len({h(k) for k in pos})
print(f"keys={len(keys)} full-64-bit collisions={coll} (non-negative grid of same size: {coll_pos}) e.g. {ex}")
print("BUG REPRODUCED: exact 64-bit hash collisions among small signed keys" if coll > coll_pos
      else "OK: no excess collisions")
