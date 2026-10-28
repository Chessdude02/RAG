"""Step 2 of the eval upgrade, part 2: validate the faithfulness judge against
human labels.

Each judge labels the fixed claim list in eval/labels/to_label.jsonl (built by
build_label_set.py), using eval-harness's judge_claims: the same prompt, schema
and code path as the claim-level faithfulness score. Claims are sent one call
per question, against that question's retrieved contexts, in the file's order.
Claims are never re-extracted, so every judge sees exactly the claims the human
labeled.

Agreement with the human labels (eval-harness eval/agreement.py) is reported
per judge. Decision rule, fixed before any judge was run: the judge with the
higher binary Cohen's kappa (supported vs unsupported) becomes the default; a
tie keeps the --tie-default judge.

A judge that skips a claim is re-asked once for just the skipped claims
(eval-harness judge_claims). A claim with no verdict even then is scored as
the WORST case: the binary opposite of the human label (human supported ->
judge not_supported; human not_supported/contradicted -> judge supported).
Leaving such claims out would score a judge only on the claims it chose to
answer. Re-asked and still-missing claims are listed in the output per judge.

Three rounds, one per provider the project has run on:
- Claude (eval/results/judge_agreement_claude.json): claude-sonnet-5 vs
  claude-opus-5-5, tie keeps sonnet; opus won.
- Gemini free tier (eval/results/judge_agreement_gemini.json):
  gemini-3.5-flash vs gemini-3.5-flash-lite, tie keeps 3.5-flash; flash-lite won.
  Dropped because the free tier allows ~20 requests/day per model.
- Mistral free tier (eval/results/judge_agreement.json, the current default):
  ministral-8b-latest vs ministral-3b-latest, tie keeps ministral-8b. The
  generator is ministral-14b-latest, so neither judge grades its own model's
  answers. Mistral's free tier serves only the Ministral models.

Usage:
    python eval/validate_judge.py                       # Mistral round, eval/labels/labels_submitted.csv
    python eval/validate_judge.py --judges claude-sonnet-5 claude-opus-5-5         --tie-default claude-sonnet-5 --out eval/results/judge_agreement_claude.json
"""
from __future__ import annotations

import argparse
import csv
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

from eval.agreement import agreement  # noqa: E402
from eval.budget import BudgetedClient, CostTracker, JudgeCache  # noqa: E402
from eval.faithfulness import VERDICTS, judge_claims  # noqa: E402

from query_rag import get_llm_client  # noqa: E402

LABELS_DIR = ROOT / "eval" / "labels"
JUDGE_CACHE_DIR = ROOT / "eval" / "cache" / "judge"
OUT = ROOT / "eval" / "results" / "judge_agreement.json"
JUDGES = ("ministral-8b-latest", "ministral-3b-latest")
TIE_DEFAULT = "ministral-8b-latest"
DEFAULT_COST_CAP_USD = 3.0
# Verdict counted for a claim the judge never labeled: always a binary disagreement.
WORST_CASE = {"supported": "not_supported", "not_supported": "supported", "contradicted": "supported"}


def load_claims() -> list[dict]:
    with open(LABELS_DIR / "to_label.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_labels(path: Path, claim_ids: set[str]) -> dict[str, str]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        labels = {r["claim_id"].strip(): r["label"].strip() for r in csv.DictReader(f)}
    bad = {k: v for k, v in labels.items() if v not in VERDICTS}
    if bad or set(labels) != claim_ids:
        raise ValueError(
            f"labels must cover exactly the {len(claim_ids)} claims with valid verdicts; "
            f"invalid={bad}, missing={sorted(claim_ids - set(labels))}, extra={sorted(set(labels) - claim_ids)}"
        )
    return labels


def run_judge(claims: list[dict], client, model: str, cache: JudgeCache) -> dict[str, dict]:
    by_question: dict[str, list[dict]] = defaultdict(list)
    for c in claims:
        by_question[c["question_id"]].append(c)
    verdicts = {}
    for qid, group in by_question.items():
        record = {"question": group[0]["question"], "contexts": group[0]["contexts"], "answer": ""}
        judged = judge_claims(record, [c["claim"] for c in group], client, model, cache, allow_missing=True)
        for c, j in zip(group, judged):
            verdicts[c["claim_id"]] = j
        print(f"  {model} {qid}: {len(group)} claims")
    return verdicts


def _git_commit(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return None


def _fmt(x) -> str:
    return "n/a" if x is None else repr(x)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # claims contain non-cp1252 characters
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", type=Path, default=LABELS_DIR / "labels_submitted.csv")
    parser.add_argument("--cost-cap", type=float, default=DEFAULT_COST_CAP_USD, help="USD; stops the run.")
    parser.add_argument("--judges", nargs=2, default=list(JUDGES))
    parser.add_argument("--tie-default", default=TIE_DEFAULT)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    judges, tie_default = args.judges, args.tie_default
    if tie_default not in judges:
        parser.error("--tie-default must be one of --judges")

    claims = load_claims()
    claim_by_id = {c["claim_id"]: c for c in claims}
    human = load_labels(args.labels, set(claim_by_id))

    tracker = CostTracker(cap_usd=args.cost_cap)
    client = BudgetedClient(get_llm_client(), tracker)
    cache = JudgeCache(JUDGE_CACHE_DIR)

    results = {}
    for model in judges:
        judged = run_judge(claims, client, model, cache)
        missing = sorted(cid for cid, j in judged.items() if j["verdict"] is None)
        reasked = sorted(cid for cid, j in judged.items() if j["reasked"])
        scored = {cid: (j["verdict"] if j["verdict"] is not None else WORST_CASE[human[cid]])
                  for cid, j in judged.items()}
        report = agreement(human, scored)
        report["reasked_claim_ids"] = reasked
        report["missing_after_reask_claim_ids"] = missing
        report["missing_scored_as"] = "binary opposite of the human label (worst case)"
        for d in report["disagreements"]:
            d["claim"] = claim_by_id[d["claim_id"]]["claim"]
            d["question_id"] = claim_by_id[d["claim_id"]]["question_id"]
            d["judge_evidence"] = judged[d["claim_id"]]["evidence"]
            d["judge_rationale"] = judged[d["claim_id"]]["rationale"]
        results[model] = {"agreement": report, "verdicts": judged}

    kappas = {m: results[m]["agreement"]["kappa_binary"] for m in judges}
    best = max(judges, key=lambda m: (kappas[m] if kappas[m] is not None else float("-inf"), m == tie_default))

    out = {
        "labels_file": args.labels.resolve().relative_to(ROOT).as_posix(),
        "n_claims": len(claims),
        "decision_rule": f"higher binary Cohen's kappa; tie keeps {tie_default}",
        "selected_default_judge": best,
        "judges": results,
        "cost": tracker.summary(),
        "rag_pipeline_commit": _git_commit(ROOT),
        "eval_harness_commit": _git_commit(EVAL_HARNESS_DIR),
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    for model in judges:
        a = results[model]["agreement"]
        print(f"\n=== {model} (n={a['n_claims']}) ===")
        print(f"judge label counts: {a['judge_label_counts']}  human: {a['human_label_counts']}")
        for key in ("accuracy_3class", "accuracy_binary", "unsupported_precision", "unsupported_recall",
                    "unsupported_f1", "kappa_binary", "kappa_3class"):
            print(f"  {key:<24}{_fmt(a[key])}")
        print(f"  TP/FP/FN (unsupported) {a['unsupported_tp']}/{a['unsupported_fp']}/{a['unsupported_fn']}")
        print(f"  re-asked: {len(a['reasked_claim_ids'])} {a['reasked_claim_ids']}  "
              f"missing after re-ask (scored as wrong): {len(a['missing_after_reask_claim_ids'])} "
              f"{a['missing_after_reask_claim_ids']}")
        print(f"  confusion (human -> judge): {a['confusion_3class']}")
        print(f"  disagreements ({len(a['disagreements'])}):")
        for d in a["disagreements"]:
            print(f"    {d['claim_id']} human={d['human']} judge={d['judge']}"
                  f"{' [binary]' if d['binary_disagrees'] else ''}: {d['claim']}")
    print(f"\nDefault judge by rule: {best}")
    print(f"Cost: {tracker.summary()}")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
