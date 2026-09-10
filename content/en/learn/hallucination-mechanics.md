---
title: "How AI Models \"Lie\": The Mechanics of Hallucination"
description: "AI doesn't get things wrong because it's broken — it gets things wrong because this is how it works. Why hallucination happens, why numbers and citations are hit hardest, and how to filter it in practice."
created: 2026-09-10
updated: 2026-09-10
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - hallucination
  - practice
  - verification
---

<img class="ewa-article-art" src="/static/img/art-hallucination-mechanics.jpg" alt="An illustration of a robot handing over a plausible report next to an empty filing cabinet" width="900" height="900" loading="lazy">

## "Where did that number come from?"

You asked AI to summarize market research and draft a report. During review, someone on the team tried to verify a cited statistic — and the source document didn't exist. Asked again, the model produced a different number this time. Both looked credible. Neither had a source. If your team works with AI, you've seen this scene.

The phenomenon where AI states unsupported facts without hesitation is what the industry calls hallucination. The easy assumption is "it's a bug, they'll fix it." It isn't. Hallucination doesn't come from the model malfunctioning — it comes from how the model fundamentally works. Once you understand that, your response changes too.

## A machine that "continues sentences well"

Strip a language model down to one sentence: it's a machine that predicts the next words from the words before them.

"Our company's revenue last year was" — to fill in what follows, the model searches through the enormous number of documents it trained on. What words tended to follow similar contexts? It picks the most plausible continuation. There is no fact-checking step anywhere in this process. It doesn't query your internal systems, aggregate statistics, or look up the statute. Producing a smooth continuation is the entire job.

Here's an analogy. Someone half-overheard a conversation at the next desk, and you ask, "So what did they say after that?" Most people construct the most natural next sentence from the part they caught and answer with it. They're not trying to lie. They were asked a question, so they filled in the most plausible answer. A language model is a machine that does this filling-in extraordinarily well. That's why even its invented content reads like polished prose.

The problem is that the model has no distinction between "plausible" and "true." Its goal is a plausible sentence, so if a claim is false but reads naturally, the model has done its job.

## Numbers and citations collapse first

Hallucination doesn't appear everywhere equally. It concentrates in specific spots.

**Numbers.** "Revenue of 34.7 billion" and "37.4 billion" are equally grammatical. Swap the digits and the sentence doesn't waver. If both score the same on plausibility, the model has no reason to care which one is real.

**Sources and citations.** "According to Kim (2023)" — a likely-looking name with a likely-looking year produces a perfectly formed citation. Nonexistent paper titles, case numbers similar to but different from real rulings, statute articles off by one character — all manufactured the same way.

**Recent facts.** The model doesn't know the world after its training cutoff. But it answers anyway, filling gaps with familiar patterns. Ask about a leadership reshuffle from six months ago and it constructs a plausible answer from the org chart it memorized before that.

## How to filter it in practice

Take a document reviewing revisions to internal HR policy.

**Before**: "Summarize the recent changes to working-hours regulations." The model writes from the statute text it memorized. Pre-revision articles and article numbers that don't exist get mixed in. Quote that in a report and it comes back from legal review.

**After**: Get the original text and include it. "Summarize based on the attached revised statute. Don't cite article numbers, effective dates, or statistics that aren't in the original. If something you need isn't in the original, just note that it's missing." Now the model's room to invent shrinks, and the summary is easy to cross-check. At the end, a person verifies article numbers against the original — five minutes.

Competitor research works the same way. "Summarize recent moves by Company A" invites fabrication. "Extract only the Company A content from these five attached articles" keeps the answer inside the source material.

## Symptoms and responses at a glance

| Symptom | Why it happens | Response |
|---|---|---|
| Nonexistent sources, articles, papers | Likely-looking pieces get combined | Provide originals and cite only within them |
| Plausible numbers | Digit swaps don't break the sentence | Enter only figures from source documents and re-verify |
| Stale or wrong recent facts | No information past the training cutoff | Provide source documents or use search-connected tools |
| Never says "I don't know" | Continuation has no natural stopping point | Instruct it to admit unknowns — and verify with a person |

## The instruction isn't a cure-all

"Say so if you don't know" genuinely reduces hallucination. The frequency of confident fabrication drops noticeably. But it has two limits.

First, it reduces hallucination; it doesn't eliminate it. The model can't detect its own invention in the moment. To the model, an invented sentence is just a finished sentence.

Second, better models produce more convincing fabrications. A weak model's hallucinations read awkwardly and stand out. A strong model's hallucinations sit inside polished prose and don't get caught by reading. Paradoxically, hallucination gets harder to catch as models improve.

So the standard shouldn't be the model — it should be the output. External documents, citations that carry legal weight, numbers that feed decisions: whenever a deliverable contains any of these three, whoever made it verifies against the originals, regardless of which model produced it. Until that check is done, it's "an AI draft," not "verified material."
