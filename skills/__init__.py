from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "llm_agent" / "src"


def ensure_src_path() -> None:
    src_path = str(SRC_DIR)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT_DIR)).replace("\\", "/")
