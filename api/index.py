import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend = os.path.join(_root, 'backend')
for p in [_root, _backend]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app import app
