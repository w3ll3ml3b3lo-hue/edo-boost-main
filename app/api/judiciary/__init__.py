"""Judiciary package exports.

The repository historically had both `app/api/judiciary.py` and this package.
The package wins Python import resolution, so re-export the legacy public API
here while the codebase completes the package consolidation.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_legacy_path = Path(__file__).resolve().parent.parent / "judiciary.py"
_spec = importlib.util.spec_from_file_location("_eduboost_legacy_judiciary", _legacy_path)
if _spec is None or _spec.loader is None:
    raise ImportError("Unable to load legacy judiciary module")

_legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_legacy)

Judiciary = _legacy.Judiciary
get_judiciary = _legacy.get_judiciary

__all__ = ["Judiciary", "get_judiciary"]
