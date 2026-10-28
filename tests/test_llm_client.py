"""scripts/llm_client.py is a copy of eval-harness eval/llm_client.py (the
deployed app must not depend on the harness); its behaviour is unit-tested
there. This only checks the copies have not drifted."""
import hashlib
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_matches_eval_harness_copy():
    harness = Path(os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness"))
    other = harness / "eval" / "llm_client.py"
    if not other.exists():
        pytest.skip(f"{other} not checked out")
    digest = lambda p: hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert digest(ROOT / "scripts" / "llm_client.py") == digest(other)
