# Eval upgrade log

Working log for the eval upgrade (branch `eval-upgrade` in both repos). Paused 2026-10-10 in Step 2: label set built, **waiting for the user's labels**.

## Setup
- **RAG repo:** `C:\Users\vedan\OneDrive\python\RAG\rag-pipeline`
- **eval-harness:** `C:\Users\vedan\OneDrive\python\eval-harness`
- **venv:** `C:\venvs\rag-pipeline` (Python 3.12.10). Use this one, not the 3.14 `venv/` inside the repo.
- **Branches:** `eval-upgrade` in both repos. Not pushed yet. `main` is untouched.

## Decisions made (from your answers to the Step 0 plan)
1. **Faithfulness question sets.** Run both. `data/eval/test_questions.json` (20) gives the number that compares with the old score. The 20 `verified` rows of `eval/questions.jsonl` are reported separately. State the question and claim counts for each.
2. **Step 2 labels.** Use the 20 verified questions, plus one deliberately bad answer per question (wrong or missing contexts), so that at least 1/3 of claims should be unsupported. Target 100+ claims, and **tell the user the count before they label**.
3. **Judges.**
   - Keep `claude-sonnet-5` as the judge for the comparable number.
   - In Step 2, also run a second judge, `claude-opus-5-5`, on the same claims.
   - Report agreement with the human labels for each judge. **The judge with higher agreement becomes the default.** Human labels are the reference.
4. **Where code lives.** eval-harness works (12 tests passing, CI gate green on 2026-10-09) and takes generic records, so the **new scorers live in eval-harness**. The RAG repo keeps the questions, the labels and the CI gate that calls them. There must be no second faithfulness scorer.
5. **Gate proof.** Run all 5 planted failures locally. Then push ONE through CI on a throwaway branch so the README can link a real failed run, with the minimal workflow change needed for that.

Standing rules:
- Pin new dependencies.
- One step per commit, and stop after each step.
- Every new scorer gets fake-judge unit tests.
- The FastAPI app and the existing scripts must keep running.
- No rounded or invented numbers.
- If something is unclear or a number looks wrong, stop and ask.

## Step 0: findings (done)
- **Already existed:**
  - retrieval Recall/MRR (60 questions, only 20 verified);
  - Precision@5 (20);
  - answer-level faithfulness judge (20);
  - multi-hop recall (10);
  - latency and cost scripts;
  - 12 unit tests;
  - the CI gate via eval-harness (20 labeled + 24 red-team).
- **Missing:**
  - claim-level faithfulness;
  - judge validation against human labels;
  - bias tests;
  - planted-failure tests;
  - injection planted *inside retrieved context*. eval-harness only tests injection through the query text (8 cases).
- **README numbers flagged:**
  - **"Faithfulness 90% (18/20)"** has no saved result and predates the classifier, decomposition and token-budget changes.
  - **"Recall@5 0.88"** uses 60 questions, 40 of them unverified; the verified-20 figure is 0.80.
  - **"Precision@5 0.64"** had no saved result. Step 1 reproduced it: 0.64.

## Step 1: claim-level faithfulness (done)
Commits: eval-harness `68663ec`, RAG `ca2109b`.

**What was built:**
- `eval-harness/eval/faithfulness.py` contains two scorers:
  - answer-level, with the prompt copied verbatim from the old `check_faithfulness`;
  - claim-level: split the answer into claims, then judge each as supported / not_supported / contradicted, using structured outputs (`output_config.format`).
- `eval-harness/eval/budget.py` contains:
  - `BudgetedClient`, a hard USD cap over every call, generation included;
  - `JudgeCache` on disk;
  - a price table that refuses unknown models.
- `eval-harness/tests/test_faithfulness.py`: 14 fake-client tests.
- `rag-pipeline/scripts/evaluate_retrieval.py` now calls the harness. It accepts `.jsonl` input (verified rows only) and the flags `--judge-model`, `--cost-cap` (default $5) and `--out`. It writes `eval/results/faithfulness_<set>.json`.
- The cache lives in `eval/cache/judge/` (gitignored).

**Results** (generator and judge both `claude-sonnet-5`):

| | test_questions.json | questions.jsonl (verified) |
|---|---|---|
| Questions | 20, 0 failed | 20, 0 failed |
| Answer-level faithful | 15/20 = 0.75 | 19/20 = 0.95 |
| Claims | 456 from 19 answers (1 made no claims) | 221 from 18 answers (2 made no claims) |
| Claim-level supported | 448/456 = 0.9825 | 216/221 = 0.9774 |
| Not supported / contradicted | 8 / 0 | 5 / 0 |
| Answers with every claim supported | 12/19 | 13/18 |
| Precision@5, hybrid (naive) | 0.64 (0.30) | 0.16 (0.10); max possible is 0.20 |
| Cost | $1.881612 | $1.26545 |

Total spend for Step 1: about $3.16, including a $0.0169 smoke test.

## Open questions to raise before or during Step 2
1. **90% → 75% on the same 20 questions.** Likely explained by pipeline changes, judge non-determinism, and n=20 (one question = 0.05). Optional: re-judge the same answers to measure judge stability (about $0.30).
2. **Answer-level and claim-level disagree on specific answers:**
   - **test_questions:** answer-level flagged 5 and claim-level agreed on 4. Claim-level **missed MultiRAG**, where the made-up "GCC = graph-level confidence calculation" expansion slipped through, and flagged 3 that answer-level passed.
   - **verified:** claim-level flagged 5 answers, answer-level flagged 1 (q006), and on q006 they flagged different claims.
   - Some flagged claims look like splitting artifacts (e.g. q019). Step 2's human labels should settle this.
3. **Claim granularity differs by judge.** In the smoke test, Opus split "introduced in 2030 by OpenAI" into 2 claims; Sonnet kept it as 1. For Step 2, extract claims **once** (fixed claim list) and have both judges label the same claims, so agreement is comparable.
4. **The result JSONs record parent commits** (`f374d0e`, `252a726`) because the runs happened before committing. The code that produced them is `ca2109b` / `68663ec`.

## Step 2, part 1: build the label set (done 2026-10-10)
`eval/build_label_set.py` built **111 claims**:
- 54 from the real answers to the 20 verified questions (q009 and q018 had none);
- 57 from deliberately bad answers: 30 wrong-context and 27 no-context. q012's no-context answer had none.

How it was built:
- 3 claims per answer, a seeded random sample (seed 42), never chosen by any judge verdict.
- Claims were split once by `claude-sonnet-5`.
- No judge has seen these claims yet.
- Spend: $0.53, including an $0.23 first attempt.

**First attempt:**
- **What happened:** 9 of 10 wrong-context answers made 0 claims, because sonnet-5 said the excerpts were off-topic even when told to answer anyway.
- **Fix:** the prompt now says outright that it is building unfaithful test answers for a fact-checker.

**Files** (`eval/labels/`):
- `to_label.jsonl` (label field empty)
- `to_label.md` (readable, grouped by question)
- `labels.csv` (claim_id,label)
- `_hidden_sources.jsonl` (answer source; the user shouldn't open it before labeling)

**Unsupported share:** at least 1/3 needs at least 37 unsupported claims. 57/111 = 51% come from bad answers, so this is likely, but it isn't confirmed until the labels are in.

## Step 2, part 2 (after labels): validate the judge
1. Build the labeling set:
   - real hybrid answers to the 20 verified questions (they can be reused from `eval/results/faithfulness_questions.json`);
   - plus one bad answer per question, generated with another question's contexts (about half) or with no context (about half).
2. Extract claims once, from a single fixed claim list.
3. Count the claims and the expected unsupported share, and **report the count to the user before labeling**.
4. Write `eval/labels/to_label.jsonl` with each claim and its contexts and **no verdicts**. Keep the judge verdicts in a separate file that isn't shown.
5. **Stop. The user labels.**
6. Then run `claude-sonnet-5` and `claude-opus-5-5` on the same claims and report, for each judge:
   - accuracy;
   - precision and recall on "not supported";
   - Cohen's kappa (implemented and unit-tested, no new dependency);
   - every disagreement.
7. The judge with higher agreement becomes the default.

Then Steps 3–6 as in the original brief: bias, injection planted in context, gate plus planted failures, README. Rough cost estimate: Steps 2–4 about $1–3 each, Step 5 about $20.
