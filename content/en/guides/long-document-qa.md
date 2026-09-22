---
title: "How to Get AI to Read a 100-Page Document"
description: "\"Read this and summarize it\" fails when the document exceeds what AI can weigh evenly at once. A prompt for building a document map first, then rereading only the relevant sections."
created: 2026-09-23
updated: 2026-09-23
aliases:
  - prompts/long-document-qa
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - document-analysis
  - practical
---

<img class="ewa-article-art" src="/static/img/art-long-document-qa.jpg" alt="An illustration of a robot dividing one tall stack of documents into four parts and reading one of them intently under an amber lamp" width="900" height="900" loading="lazy">

## Why long documents fake being "read"

Long documents land on your desk: a grant program announcement, a request for proposal, contract review materials. You have no time to read the whole thing, so you paste it all into AI and type "read this and summarize it."

AI returns a summary. But something is off. The overview up front is detailed, while exactly what you need — payment eligibility, deadlines buried in the middle and back — gets glossed over in a sentence or two. Nothing in the answer says which part of the document it came from.

There are two reasons. First, the document exceeds what the model can attend to with equal weight in one pass. Even if it all fits, models lean on the beginning and end and skim the middle. Second, the question is open-ended. "Summarize it" tells AI to decide for itself what matters, and its criteria are not yours.

The fix has a fixed shape: split the document, build a map first, reread only the relevant sections, then demand citations.

## The prompt that works

### Step 1 — Build a document map

Split the document into 4–5 chunks along chapter boundaries. Run the prompt below for each chunk; just change "Document (1/4)" as you go.

```
Do not summarize the document below. Figure out its structure first.

Output format:
1. Document overview — what this document is about, in 2 sentences
2. List of chapters — title, start position, one line on what it covers
3. The 3 chapters most relevant to what I ultimately want to know, and why

What I ultimately want to know:
[e.g., payment eligibility and application deadlines, and whether my company qualifies]

Document (1/4):
"""
[first portion of the document, split at chapter boundaries]
"""
```

After four runs you have a map of the whole document. This is the first point where you actually know which chapter holds what.

### Step 2 — Reread only the relevant part and ask

From the map, pick only the chapters relevant to your question and paste them into a fresh conversation.

```
Below is an excerpt covering only [Chapter 3: eligibility conditions] of a document.
Answer the question using only this excerpt as your evidence.

Question: Which payment eligibility conditions relate to company size?

Rules:
- Attach the supporting sentence quoted verbatim to every answer
- If the excerpt does not cover something, answer "not in this part" — do not fill gaps with inference
- If conditions split into several, organize them per condition

Excerpt:
"""
[paste only the relevant chapters]
"""
```

Three things separate this from "read and summarize."

First, **you narrowed what gets read**. Only the chapters tied to the question are in play. The skimmed-middle problem disappears.

Second, **citations are mandatory**. Every answer carries the original sentence, so you can verify it against the document later.

Third, **AI is allowed to say it's not there**. Given a question, AI tends to produce an answer. Allowing "not in this part" makes fabrication visibly rarer.

## Review checklist

- [ ] Did you search the document for each quoted sentence? If search can't find it, the quote is invented
- [ ] For items answered "not in this part," did you re-check the map whether another chapter covers them?
- [ ] Do numbers, dates, and amounts match the quoted source?
- [ ] When picking relevant chapters, did you avoid trusting only your own phrasing? The document may use different terms

## Extension: comparing two drafts

When a revised draft arrives, build maps for both and compare clause by clause.

```
Below are excerpts on [contract terms] from two documents on the same subject.
Compare them clause by clause.

Output format:
1. Changed clauses — old sentence → new sentence (include the stated reason if the document gives one)
2. Clauses present in only one document — and which one
3. Identical clauses — list clause numbers only

Rules:
- List identical clauses by number, do not bundle them; I'll check against originals later
- Do not invent clauses that appear in neither

Excerpt A:
"""
[the corresponding part of the current draft]
"""

Excerpt B:
"""
[the corresponding part of the revised draft]
"""
```

## What this prompt cannot do

A human decides where to cut. Documents with clear chapters are easy; a scanned file with no table of contents forces you to judge the split points first. If it's a scanned image PDF, text extraction comes before everything, and poor extraction shakes every step after it.

Citations can be wrong too. AI is capable of producing sentences that read like quotes but don't exist. That's why the first checklist item is searching for the quote. And if the thing you're looking for is defined badly, both the map and the excerpts head the wrong way. You only got faster reading — deciding what to look for stays your job.
