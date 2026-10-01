---
title: "Why the Top-Ranked Model Was Only Average at Our Work"
description: "The team picked the model with the best benchmark score, but meeting-note summaries came out no better than before. Four reasons benchmark scores and real-world performance diverge, and what to actually look at when choosing a tool."
created: 2026-10-01
updated: 2026-10-01
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - 모델-선택
  - 벤치마크
  - 실무
---

<img class="ewa-article-art" src="/static/img/art-beyond-benchmarks.jpg" alt="An illustration of a desktop robot holding a first-place trophy while glancing back at a messy pile of documents on the desk" width="900" height="900" loading="lazy">

## "We picked the one with the highest score"

The team decided to switch the AI model they used. The person in charge opened a leaderboard and picked the model with the highest overall score. The rationale looked airtight: it ranked first.

Three weeks later, at the review meeting, the verdict came in. Meeting-note summaries were no different from before, and report drafts actually got wordier. The only thing that improved was English emails. Cost had doubled. The score was right, but the work stayed the same. Where did it go wrong?

## What a benchmark actually measures

Translated into office language, a benchmark is a **mock exam**. Multiple models take the same test, and the scores put them in order. The test usually consists of multiple-choice general-knowledge questions, math problems with definite answers, and coding tasks that must pass predefined tests. Scoring has to be mechanical, or you cannot compare dozens of models at once.

Real work problems are shaped differently. "Split this meeting transcript into decisions made and items deferred" has no standard answer. The context of our meetings, the information our team considers important, how to handle ambiguous remarks — all of that enters the judgment. The ability to ace questions with correct answers and the ability to do our answerless work well do not convert into the same score.

Beyond that, four structural reasons widen the gap between scores and practice.

**The test questions leak in advance.** Benchmark questions are mostly public on the internet. If they get mixed into a model's training data, the model answers from memory rather than reasoning — like cramming for an exam. This is called data contamination. Sometimes when a new benchmark comes out, existing models' scores drop across the board; they are seeing an uncontaminated test for the first time.

**The overall score is an average.** Being first in total score does not mean being first in every subject. Models have strengths and weaknesses by domain. Some write great English copy while sounding awkward in formal Korean documents. Our work corresponds to a specific subject, not the overall score. A model ranked a few steps lower overall can be first in our subject.

**The measurement environment is different.** Benchmarks run with fixed prompts, fixed settings, and no tools. In practice, a model runs with our prompts, our documents, and in combination with search or other tools. The same model produces different results when that environment changes. Benchmark scores do not capture any of that combination.

**The top tier is all similar.** On today's leaderboards, the top models sit within the margin of error. A one- or two-point gap is imperceptible in our work, yet that gap is exactly what leads teams to pick a model that costs twice as much.

## What changed when the team switched methods

The team above went back and tried again with a different approach.

**First attempt — pick by leaderboard rank.** They adopted the overall number-one model and put it on meeting-note summaries, report drafts, and email writing. The result was the review we saw. No difference in the core task of meeting summaries; the consensus was that nobody could tell anything had changed.

**Second attempt — compare directly on our own work.** They narrowed the candidates to three models and tested them with inputs from actual work: 10 meeting transcripts, 5 report drafts, 10 customer inquiry replies. Grading criteria were set before running anything. For summaries: number of missed action items and summary length. For replies: whether the designated tone was followed. The result was unexpected. The model ranked third overall was best at meeting summaries and cost half as much. For emails, they kept the existing model.

The difference between the two attempts came not from the models but from the **evaluation method**. "Which model is good?" has no answer. But define "what a good result looks like in our work" first, and comparison becomes possible. And that answer differs from team to team.

## In short: how far to trust benchmarks

| Category | Benchmark score is enough | Direct testing needed |
|---|---|---|
| Use case | One-off questions, general conversation | Recurring routine work (summaries, reports, responses) |
| Stage | Narrowing dozens of candidates to 2–3 | Choosing one of the final 2–3 |
| Language & format | When the benchmark (often English-centric) matches the use | When long-form Korean or internal jargon is central |
| Basis for judgment | Checking the big picture (generational gaps) | Felt quality and cost-effectiveness |

This is not an argument for throwing out benchmarks. For initial screening they are still the best tool available — you cannot hand-test every model. Use benchmarks to narrow the field, then make the final call on samples of your own work. Just keeping that order filters out most "great score, useless for us" situations up front.

## What to check before adoption

- **A 20–30 item internal evaluation set is enough to start.** Collect real work inputs as they are. Statistically thin, but sufficient for a decision. Document the grading criteria before running anything — without criteria you end up with a list of results and no decision.
- **Mask confidential information.** Even with real work inputs, replace customer names and unpublished figures. The moment you test via an external API, that data leaves the building.
- **Don't test once and stop.** A model's behavior changes when its version changes. Save the evaluation set and rerun it whenever you switch models. It is a half-day of work.
- **Check the source of scores vendors cite.** Until you know which benchmark it is and how it relates to your work, do not use numbers from marketing copy as evidence.
- **One-off uses don't need any of this.** A single translation or a single question will come out similar from any top-tier model. Don't spend time choosing; switch if it becomes inconvenient.

The final criterion for choosing a tool is always our own work. A benchmark is a tool for narrowing the field — it does not make the final decision for you.
