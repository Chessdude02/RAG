"""Step 3 of the eval upgrade: name/gender bias check on the GENERATOR.

This tests the generator model (query_rag.GENERATION_MODEL) on its own: plain
prompts, no retrieval, no RAG system prompt. It says nothing about the RAG
pipeline's retrieval or its grounded answers.

Each of the tasks in eval/bias/tasks.json is run once per name pair (male- and
female-coded name, same surname), giving len(tasks) x len(name_pairs) pairs.
Generation uses the model's default settings, so each text is one sample;
sampling noise is part of the measured gap and widens the CI. Generations and
judge calls are cached on disk, so a rerun reuses the same texts.

Scoring (eval-harness eval/bias.py): word count, VADER sentiment, and a 1-10
tone rating by the default judge (claude-opus-5-5) on name-masked text. Gaps
are b - a (female-coded minus male-coded), with a bootstrap 95% CI over pairs.

Usage:
    python eval/run_bias.py
    python eval/run_bias.py --cost-cap 4
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_HARNESS_DIR = Path(os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(EVAL_HARNESS_DIR))

from eval.bias import mean_or_none, score_text, summarize_gap  # noqa: E402
from eval.budget import BudgetedClient, CostCapExceeded, CostTracker, JudgeCache  # noqa: E402
from eval.faithfulness import _response_text  # noqa: E402

from evaluate_retrieval import DEFAULT_JUDGE_MODEL  # noqa: E402
from query_rag import GENERATION_MODEL, MAX_TOKENS, get_llm_client  # noqa: E402

TASKS_FILE = ROOT / "eval" / "bias" / "tasks.json"
CACHE_DIR = ROOT / "eval" / "cache" / "judge"
OUT = ROOT / "eval" / "results" / "bias.json"
DEFAULT_COST_CAP_USD = 4.0
METRICS = ("length_words", "sentiment", "tone")
SCOPE_NOTE = (
    "Tests the generator model alone (plain prompts, no retrieval, no RAG system prompt); "
    "it does not test the RAG pipeline."
)


def generate(prompt: str, client, cache: JudgeCache) -> str:
    request = {
        "model": GENERATION_MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
    }
    text = cache.get(request)
    if text is None:
        text = _response_text(client.messages.create(**request))
        cache.put(request, text)
    elif hasattr(client, "tracker"):
        client.tracker.cache_hits += 1
    return text


def _git_commit(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--cost-cap", type=float, default=DEFAULT_COST_CAP_USD, help="USD; stops the run.")
    args = parser.parse_args()

    spec = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    tracker = CostTracker(cap_usd=args.cost_cap)
    client = BudgetedClient(get_llm_client(), tracker)
    cache = JudgeCache(CACHE_DIR)
    names = [n for p in spec["name_pairs"] for n in (p["a"], p["b"])]

    pairs, stopped = [], None
    try:
        for task in spec["tasks"]:
            for pair in spec["name_pairs"]:
                row = {"task_id": task["id"], "a_name": pair["a"], "b_name": pair["b"]}
                for side in ("a", "b"):
                    text = generate(task["prompt"].format(name=pair[side]), client, cache)
                    # Mask every pair name, not just this one, so no name leaks to the judge.
                    row[side] = {"text": text, **score_text(text, names, client, args.judge_model, cache)}
                row["gaps"] = {m: row["b"][m] - row["a"][m] for m in METRICS}
                pairs.append(row)
            print(f"{task['id']}: {len(spec['name_pairs'])} pairs")
    except CostCapExceeded as exc:
        stopped = str(exc)
        print(f"STOPPED: {exc}")

    summary = {m: summarize_gap([p["gaps"][m] for p in pairs]) for m in METRICS} if pairs else {}
    means = {
        side: {m: mean_or_none([p[side][m] for p in pairs]) for m in METRICS} for side in ("a", "b")
    }
    by_task = defaultdict(dict)
    for m in METRICS:
        for task in spec["tasks"]:
            gaps = [p["gaps"][m] for p in pairs if p["task_id"] == task["id"]]
            by_task[task["id"]][m] = mean_or_none(gaps)
    pronouns = {
        side: {k: sum(p[side]["pronouns"][k] for p in pairs) for k in ("he", "she", "they")}
        for side in ("a", "b")
    }

    out = {
        "scope": SCOPE_NOTE,
        "gap_definition": "b - a, where b is the female-coded name and a the male-coded name",
        "generator_model": GENERATION_MODEL,
        "judge_model": args.judge_model,
        "n_tasks": len(spec["tasks"]),
        "n_name_pairs": len(spec["name_pairs"]),
        "n_pairs": len(pairs),
        "stopped_early": stopped,
        "gap_summary": summary,
        "means_by_side": means,
        "mean_gap_by_task": by_task,
        "pronoun_totals_by_side": pronouns,
        "pairs": pairs,
        "cost": tracker.summary(),
        "rag_pipeline_commit": _git_commit(ROOT),
        "eval_harness_commit": _git_commit(EVAL_HARNESS_DIR),
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{SCOPE_NOTE}")
    print(f"Generator {GENERATION_MODEL}, tone judge {args.judge_model}, {len(pairs)} pairs; gap = b - a (female - male)")
    for m, s in summary.items():
        print(f"  {m:<13} mean gap {s['mean_gap']!r}  95% CI [{s['ci95_low']!r}, {s['ci95_high']!r}]  "
              f"b>a {s['n_b_higher']}, a>b {s['n_a_higher']}, equal {s['n_equal']}")
    print(f"  means a: {means['a']}\n  means b: {means['b']}")
    print(f"  pronoun totals: {pronouns}")
    print(f"Cost: {tracker.summary()}")
    print(f"Wrote {OUT}")
    if stopped:
        sys.exit(1)


if __name__ == "__main__":
    main()
