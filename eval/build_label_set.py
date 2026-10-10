"""Step 2 of the eval upgrade: build a set of claims for a human to label, so
the faithfulness judge can be validated against human labels.

Claims come from two kinds of answer to the 20 verified questions in
eval/questions.jsonl:

- real: the hybrid pipeline's answers from eval/results/faithfulness_questions.json
  (Step 1). Mostly expected to be supported.
- bad: one deliberately bad answer per question, so the set is not mostly
  "supported". Even-numbered questions get an answer written from ANOTHER
  question's retrieved chunks ("wrong_context"); odd-numbered questions get an
  answer written from the model's own knowledge with no context
  ("no_context"). Both prompts tell the model to answer confidently, since the
  pipeline's own prompt would just decline.

Every claim is paired with the contexts its question actually retrieved
(Step 1's hybrid top-5, read from Chroma by chunk id), which is what both the
human and the judges check it against.

Claims are split by eval-harness's extract_claims (claude-sonnet-5), once, so
every judge later labels the exact same claim list. A seeded random sample of
CLAIMS_PER_ANSWER claims per answer is kept: never selected by any judge
verdict, since that would bias the agreement numbers. No judge is run here.

Outputs (eval/labels/):
  to_label.jsonl          one row per claim: claim_id, question, claim, contexts, label ("")
  to_label.md             the same claims grouped by question, contexts shown once
  labels.csv              claim_id,label -- fill this in (or the jsonl "label" field)
  _hidden_sources.jsonl   claim_id -> answer source and text; don't open before labeling
"""
from __future__ import annotations

import csv
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
EVAL_HARNESS_DIR = Path(os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness"))
sys.path.insert(0, str(EVAL_HARNESS_DIR))

from eval.budget import BudgetedClient, CostTracker, JudgeCache  # noqa: E402
from eval.faithfulness import extract_claims  # noqa: E402

from query_rag import ANTHROPIC_MODEL, build_context, get_anthropic_client, get_collection  # noqa: E402

STEP1_RESULTS = ROOT / "eval" / "results" / "faithfulness_questions.json"
LABELS_DIR = ROOT / "eval" / "labels"
JUDGE_CACHE_DIR = ROOT / "eval" / "cache" / "judge"
EXTRACT_MODEL = "claude-sonnet-5"  # same extractor as Step 1, so real-answer claims come from the cache
CLAIMS_PER_ANSWER = 3
SEED = 42
COST_CAP_USD = 2.0
LABELS = ("supported", "not_supported", "contradicted")

WRONG_CONTEXT_PROMPT = """We are building test data for a fact-checker that verifies \
answers against source excerpts, and need examples of unfaithful answers. The excerpts \
below were retrieved for a DIFFERENT question. Write the answer a careless assistant \
would give by stretching these excerpts to fit the question: 4-6 confident, specific \
sentences that borrow names, methods, and numbers from the excerpts. Do not mention \
that the excerpts are off-topic. Output only the answer.

Excerpts:

{context}

Question: {question}"""

NO_CONTEXT_PROMPT = """Answer the following research question from your own knowledge in \
4-6 confident, specific sentences. Do not mention sources or say you are unsure.

Question: {question}"""


def fetch_chunks(chunk_ids: list[str]) -> list[dict]:
    got = get_collection().get(ids=chunk_ids, include=["documents", "metadatas"])
    by_id = {
        cid: {"chunk_id": cid, "text": doc, "metadata": meta}
        for cid, doc, meta in zip(got["ids"], got["documents"], got["metadatas"])
    }
    missing = [cid for cid in chunk_ids if cid not in by_id]
    if missing:
        raise RuntimeError(f"chunks missing from Chroma: {missing}")
    return [by_id[cid] for cid in chunk_ids]


def generate_bad_answer(client, question: str, wrong_chunks: list[dict] | None) -> str:
    if wrong_chunks is None:
        prompt = NO_CONTEXT_PROMPT.format(question=question)
    else:
        prompt = WRONG_CONTEXT_PROMPT.format(context=build_context(wrong_chunks), question=question)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": prompt}],
    )
    if response.stop_reason != "end_turn":
        raise RuntimeError(f"bad-answer generation stopped with {response.stop_reason}")
    return next(b.text for b in response.content if b.type == "text")


def main() -> None:
    step1 = json.loads(STEP1_RESULTS.read_text(encoding="utf-8"))
    rows = step1["per_question"]
    if len(rows) != 20 or step1["failures"]:
        raise RuntimeError("expected Step 1 results for all 20 verified questions")

    tracker = CostTracker(cap_usd=COST_CAP_USD)
    client = BudgetedClient(get_anthropic_client(), tracker)
    cache = JudgeCache(JUDGE_CACHE_DIR)
    rng = random.Random(SEED)

    answers = []  # one entry per answer: question id, source, text, contexts, sampled claims
    for i, row in enumerate(rows):
        contexts = [build_context([c]) for c in fetch_chunks(row["hybrid_retrieved_chunk_ids"])]

        if i % 2 == 0:
            donor = rows[(i + 10) % len(rows)]
            bad_source = f"wrong_context (chunks of {donor['id']})"
            bad_text = generate_bad_answer(client, row["question"], fetch_chunks(donor["hybrid_retrieved_chunk_ids"]))
        else:
            bad_source = "no_context"
            bad_text = generate_bad_answer(client, row["question"], None)

        for source, text in (("real", row["hybrid_answer"]), (bad_source, bad_text)):
            record = {"question": row["question"], "contexts": contexts, "answer": text}
            claims = extract_claims(record, client, EXTRACT_MODEL, cache)
            sampled = rng.sample(claims, min(CLAIMS_PER_ANSWER, len(claims)))
            answers.append({
                "question_id": row["id"], "question": row["question"], "source": source,
                "answer": text, "contexts": contexts, "n_claims_extracted": len(claims), "claims": sampled,
            })
        print(f"{row['id']}: real {answers[-2]['n_claims_extracted']} claims, "
              f"{bad_source} {answers[-1]['n_claims_extracted']} claims")

    # Number claims in a shuffled order so ids carry no hint of the source.
    flat = [(a, claim) for a in answers for claim in a["claims"]]
    rng.shuffle(flat)
    flat.sort(key=lambda pair: pair[0]["question_id"])  # stable: grouped by question, shuffled within

    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    to_label, hidden = [], []
    for n, (a, claim) in enumerate(flat, start=1):
        claim_id = f"c{n:03d}"
        to_label.append({
            "claim_id": claim_id, "question_id": a["question_id"], "question": a["question"],
            "claim": claim, "contexts": a["contexts"], "label": "",
        })
        hidden.append({
            "claim_id": claim_id, "question_id": a["question_id"], "source": a["source"],
            "claim": claim, "answer": a["answer"],
        })

    with open(LABELS_DIR / "to_label.jsonl", "w", encoding="utf-8") as f:
        for r in to_label:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(LABELS_DIR / "_hidden_sources.jsonl", "w", encoding="utf-8") as f:
        for r in hidden:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(LABELS_DIR / "labels.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["claim_id", "label"])
        for r in to_label:
            writer.writerow([r["claim_id"], ""])
    write_markdown(to_label, LABELS_DIR / "to_label.md")

    n_real = sum(1 for h in hidden if h["source"] == "real")
    print(f"\n{len(to_label)} claims: {n_real} from real answers, {len(to_label) - n_real} from bad answers")
    print(f"Cost: {tracker.summary()}")


def write_markdown(to_label: list[dict], path: Path) -> None:
    lines = [
        "# Claims to label",
        "",
        "For each claim, judge ONLY against the excerpts shown for its question (no outside knowledge),",
        "and write one label per claim_id in `labels.csv`:",
        "",
        "- `supported` - the excerpts state the claim or directly entail it",
        "- `contradicted` - the excerpts state something incompatible with it",
        "- `not_supported` - neither (including true-in-the-world facts the excerpts don't state)",
        "",
    ]
    current = None
    for r in to_label:
        if r["question_id"] != current:
            current = r["question_id"]
            lines += ["---", "", f"## {current}: {r['question']}", "", "<details><summary>Excerpts</summary>", ""]
            for k, ctx in enumerate(r["contexts"], start=1):
                lines += [f"**[C{k}]**", "", "```", ctx, "```", ""]
            lines += ["</details>", "", "Claims:", ""]
        lines.append(f"- **{r['claim_id']}** {r['claim']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
