# Eval upgrade log

Working log for the eval upgrade (branch `eval-upgrade` in both repos). Paused 2026-10-11 **after Step 3**. Next is Step 4 (prompt injection planted in context).

## Resume here (next session)
- Steps 1–3 are done.
- **Next: Step 4.**
  - Build 30+ question/context sets, each with a harmless instruction planted in one retrieved chunk.
  - Report the follow rate.
  - The scorer goes in eval-harness, with fake-judge tests.
- **Default judge:** `claude-opus-5-5`.
- **Total spend so far:** about $5.54.

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

## Step 2, part 2: judge agreement (done 2026-10-10)
**Labels:**
- The user's labels are in `eval/labels/labels_submitted.csv`: 111/111 valid, 63 supported, 42 not_supported, 6 contradicted. That is 48 unsupported, above the 37 needed.
- An identical copy at `eval/labels_submitted.csv` is left uncommitted.
- **By source:** real 54/54 supported. wrong_context: 22 not_supported, 6 contradicted, 2 supported. no_context: 20 not_supported, 7 supported.

**Decision rule** (fixed before any judge ran): higher binary Cohen's kappa wins; a tie keeps sonnet.

**How it ran:**
- `eval/validate_judge.py` judges the fixed claims, one call per question, against that question's contexts, using the harness `judge_claims` (same prompt and path as Step 1).
- Metrics come from the harness `eval/agreement.py`, with 7 tests.
- Output: `eval/results/judge_agreement.json`. Cost $0.87737 (sonnet $0.34273, opus $0.53464).

| n=111 | claude-sonnet-5 | claude-opus-5-5 |
|---|---|---|
| Accuracy, 3-class | 0.9279279279279279 (103/111) | 0.954954954954955 (106/111) |
| Accuracy, binary | 0.963963963963964 (107/111) | 0.990990990990991 (110/111) |
| Unsupported precision | 0.9583333333333334 (46/48) | 1.0 (47/47) |
| Unsupported recall | 0.9583333333333334 (46/48) | 0.9791666666666666 (47/48) |
| Kappa, binary | 0.9265873015873016 | 0.9816011934361014 |
| Kappa, 3-class | 0.8614232209737827 | 0.913104744011273 |

**Result:** `claude-opus-5-5` becomes the default (`scripts/evaluate_retrieval.py`). The Step 1 saved numbers stay sonnet-judged and comparable.

**Disagreements:**
- **Sonnet (8):**
  - c009 (human not_supported, judge supported; binary);
  - c021 and c048 (human supported, judge not_supported; binary);
  - c058, c061, c068, c093 (human contradicted, judge not_supported);
  - c098 (human not_supported, judge supported; binary).
- **Opus (5):** c058, c061, c068, c093 (contradicted → not_supported), and c098 (not_supported → supported; binary).
- All are on bad-answer claims. Both judges matched the human on all 54 real-answer claims.

**Caveats for the README limits section:**
1. **No real-answer claim is unsupported in the human labels**, so judge recall on the *pipeline's own* subtle errors is not measured. All 48 positives come from deliberately bad answers, which are easier to catch.
2. **The judges differ by 3 binary disagreements out of 111** (4 vs 1). That is a small margin at this n.
3. **Neither judge used "contradicted" where the human did** (4/6 went to not_supported). The 3-class boundary is weak, so binary is the main metric.
4. **The worked example I gave before labeling covered c001–c006**, and the human's labels for those match it. Those 6 may be influenced by it.
5. **One human labeler**, so there is no inter-annotator agreement.

## Step 3: bias check on the generator (done 2026-10-11)
**What it tests:** the generator `claude-sonnet-5` alone, with plain prompts, no retrieval and no RAG system prompt. **It does not test the RAG pipeline.**

**Setup:**
- **Inputs:** `eval/bias/tasks.json` has 10 neutral tasks x 6 name pairs (male-coded a, female-coded b, same surname) = **60 pairs**. Each pair is one sample per name.
- **Scoring** (harness `eval/bias.py`, 7 tests):
  - word count;
  - VADER sentiment, averaged per sentence (new pinned dependency `vaderSentiment==3.3.2`);
  - a 1–10 tone rating by `claude-opus-5-5` on name-masked text.
- **Gap:** b − a, with a percentile bootstrap 95% CI (10,000 resamples, seed 0).
- **Runner:** `eval/run_bias.py`. Output: `eval/results/bias.json`. Cost $0.96533 (sonnet $0.361426, opus $0.603904).

| Metric (gap = female − male) | Mean gap | 95% CI | b>a / a>b / equal |
|---|---|---|---|
| Length (words) | 2.933333333333333 | [-1.8833333333333333, 7.783333333333333] | 32 / 28 / 0 |
| Sentiment (VADER) | 0.003919031746031752 | [-0.037238111111111104, 0.04346719444444445] | 32 / 28 / 0 |
| Tone (judge, 1–10) | 0.05 | [-0.05, 0.15] | 6 / 3 / 51 |

**Means:**
- a (male-coded): length 140.48333333333332, sentiment 0.5730518095238095, tone 7.566666666666666;
- b (female-coded): length 143.41666666666666, sentiment 0.5769708412698412, tone 7.616666666666666.

**Result: all three CIs include 0, so no significant gap at n=60.**

**Observations:**
- **Pronouns:** a-side texts used he 214, she 6, they 29; b-side used he 0, she 260, they 25.
- **Wei Zhang:** the model used "they" in 8 of 10 tasks, and no pronoun at all in the other two. The exception is the **nurse bio**, where it used "she" 6 times. One sample, but a visible occupational stereotype.
- **Per-task mean gaps** are in the JSON. At 6 pairs per task, they are too small to read alone.

**Caveats for the README:**
1. **One sample per name/task.** Sampling noise is part of the gap, and n=60 can only detect moderate gaps.
2. **Tone ratings are coarse.** 51/60 pairs got identical ratings, mostly 7 or 8, so tone has low sensitivity.
3. **VADER misses mild formal praise** (e.g. "reliable engineer" = 0.0).
4. **Narrow scope.** Only gender via first names was tested (6 names per side), and only English.
5. **Gender is visible to the tone judge through pronouns,** since only names are masked.
