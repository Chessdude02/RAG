"""Step 5 of the eval upgrade: prove the eval gate catches real regressions.

Two phases, run separately so the thresholds are fixed BEFORE any planted
failure is seen:

  python eval/run_planted_failures.py baseline [--resume]
      Two clean gate runs of the current pipeline, then writes
      eval/gate_baseline.json from them (eval-harness scripts/make_baseline.py:
      baseline = mean, allowed drop = max(0.05, 2 x spread between the runs)).

  python eval/run_planted_failures.py planted [--only 3_top_k_1]
      For each patch in eval/planted_failures/: apply it to scripts/query_rag.py,
      run the gate (eval-harness scripts/run_eval.py --gate --baseline ...),
      record caught (gate exit 1) or missed, and revert with git checkout.
      Each planted run starts from a snapshot of the results DB taken after the
      clean runs, so the rolling check always compares with a clean run and one
      missed failure can't become the bar for the next.

Runs use a separate results DB (eval/cache/gate_planted.db) via
EVAL_RESULTS_DB, so eval-harness's own history is untouched. The gate runs in
eval-harness's interpreter (HARNESS_PYTHON), which has both repos' deps.
Per-run reports: eval/results/gate_runs/<name>.json; summary:
eval/results/planted_failures.json.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_HARNESS_DIR = Path(os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness"))
HARNESS_PYTHON = Path(os.environ.get(
    "HARNESS_PYTHON",
    EVAL_HARNESS_DIR / (".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python"),
))
PATCH_DIR = ROOT / "eval" / "planted_failures"
TARGET = "scripts/query_rag.py"
BASELINE_FILE = ROOT / "eval" / "gate_baseline.json"
DB = ROOT / "eval" / "cache" / "gate_planted.db"
DB_SNAPSHOT = ROOT / "eval" / "cache" / "gate_planted_clean.db"
REPORT_DIR = ROOT / "eval" / "results" / "gate_runs"
SUMMARY = ROOT / "eval" / "results" / "planted_failures.json"
CLAIM_JUDGE = "ministral-8b-latest"  # Step 2 default judge (Mistral round)
COST_CAP_PER_RUN_USD = 6.0  # claim-judge calls only; Mistral free-tier calls cost $0


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check)


def target_is_clean() -> bool:
    return git("diff", "--quiet", "HEAD", "--", TARGET, check=False).returncode == 0


def run_gate(name: str, with_baseline: bool) -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"{name}.json"
    cmd = [
        str(HARNESS_PYTHON), "scripts/run_eval.py", "--system", "rag", "--gate", "--trigger", f"planted:{name}",
        "--claim-judge", CLAIM_JUDGE, "--cost-cap", str(COST_CAP_PER_RUN_USD), "--report", str(report),
    ]
    if with_baseline:
        cmd += ["--baseline", str(BASELINE_FILE)]
    env = {**os.environ, "EVAL_RESULTS_DB": str(DB), "RAG_PIPELINE_DIR": str(ROOT), "PYTHONIOENCODING": "utf-8"}
    log = REPORT_DIR / f"{name}.log"
    print(f"[{datetime.now():%H:%M:%S}] gate run: {name}", flush=True)
    with open(log, "w", encoding="utf-8") as f:
        proc = subprocess.run(cmd, cwd=EVAL_HARNESS_DIR, env=env, stdout=f, stderr=subprocess.STDOUT)
    if not report.exists():
        raise RuntimeError(f"gate run {name} wrote no report (exit {proc.returncode}); see {log}")
    data = json.loads(report.read_text(encoding="utf-8"))
    data["exit_code"] = proc.returncode
    print(f"[{datetime.now():%H:%M:%S}]   exit {proc.returncode}, passed={data['passed']}", flush=True)
    return data


def api_errors(run_id: str) -> list[str]:
    """Case errors that come from the API itself (credit, auth, overload), not
    from the pipeline. A run with any of these measures nothing about the planted
    failure, so it must not count as caught."""
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT error FROM case_results WHERE run_id = ? AND error LIKE '%Error code:%'",
                        (run_id,)).fetchall()
    conn.close()
    return [r[0] for r in rows]


def phase_baseline(resume: bool = False) -> None:
    if not target_is_clean():
        sys.exit(f"{TARGET} has local changes; the baseline must be the committed pipeline.")
    if DB.exists() and not resume:
        sys.exit(f"{DB} exists; delete it to rebuild the baseline from scratch, or pass --resume.")
    DB.parent.mkdir(parents=True, exist_ok=True)
    runs = []
    for i in (1, 2):
        report = REPORT_DIR / f"clean_{i}.json"
        if resume and report.exists():
            # Keep a finished clean run (e.g. after the process was killed mid-way).
            data = json.loads(report.read_text(encoding="utf-8"))
            if data["passed"] and data["metrics"].get("n_claim_scoring_errors") == 0:
                print(f"reusing clean_{i} ({data['run_id']})", flush=True)
                runs.append(data)
                continue
        runs.append(run_gate(f"clean_{i}", with_baseline=False))
    shutil.copyfile(DB, DB_SNAPSHOT)
    env = {**os.environ, "EVAL_RESULTS_DB": str(DB)}
    subprocess.run(
        [str(HARNESS_PYTHON), "scripts/make_baseline.py", "--runs", *[r["run_id"] for r in runs],
         "--out", str(BASELINE_FILE)],
        cwd=EVAL_HARNESS_DIR, env=env, check=True,
    )


def phase_planted(only: list[str] | None) -> None:
    if not BASELINE_FILE.exists() or not DB_SNAPSHOT.exists():
        sys.exit("run the baseline phase first")
    patches = sorted(PATCH_DIR.glob("*.patch"))
    if only:
        patches = [p for p in patches if p.stem in only]
    summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {"failures": {}}

    for patch in patches:
        if not target_is_clean():
            sys.exit(f"{TARGET} is not clean before {patch.name}; refusing to stack patches.")
        shutil.copyfile(DB_SNAPSHOT, DB)
        git("apply", str(patch))
        try:
            result = run_gate(patch.stem, with_baseline=True)
        finally:
            git("checkout", "--", TARGET)
        if not target_is_clean():
            sys.exit(f"revert of {patch.name} failed; fix {TARGET} by hand.")
        bad = api_errors(result["run_id"])
        if bad:
            summary["failures"].pop(patch.stem, None)
            SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
            sys.exit(f"{patch.stem}: {len(bad)} cases hit API errors, run is INVALID and not recorded. "
                     f"First: {bad[0][:200]}")
        summary["failures"][patch.stem] = {
            "caught": result["exit_code"] == 1 and not result["passed"],
            "exit_code": result["exit_code"],
            "rolling_regressions": [r["metric"] for r in result["rolling"]["regressions"]],
            "baseline_regressions": [r["metric"] for r in result["baseline"]["regressions"]],
            "metrics": result["metrics"],
            "run_id": result["run_id"],
            "claim_judge_cost": result["claim_judge_cost"],
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    caught = sum(1 for f in summary["failures"].values() if f["caught"])
    print(f"\nCaught {caught} of {len(summary['failures'])} planted failures.")
    for name, f in summary["failures"].items():
        print(f"  {name}: {'CAUGHT' if f['caught'] else 'MISSED'}  baseline: {f['baseline_regressions']}  "
              f"rolling: {f['rolling_regressions']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["baseline", "planted"])
    parser.add_argument("--only", nargs="*", help="planted phase: patch names (file stems) to run")
    parser.add_argument("--resume", action="store_true", help="baseline phase: reuse finished clean runs")
    args = parser.parse_args()
    phase_baseline(args.resume) if args.phase == "baseline" else phase_planted(args.only)


if __name__ == "__main__":
    main()
