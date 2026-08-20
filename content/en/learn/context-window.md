---
title: "The Context Window — Why AI Forgets What You Just Said"
description: "As a conversation grows, AI starts ignoring your early instructions; long documents get skimmed in the middle. How the context window works and what to do about it in practice."
created: 2026-08-20
updated: 2026-08-20
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - context-window
  - practical
  - llm
---

<img class="ewa-article-art" src="/static/img/art-context-window.jpg" alt="Illustration of a robot focusing on a fresh sheet of paper at a lamplit desk while stacks of older documents crowd the desk and slip off the edge" width="900" height="600" loading="lazy">

## "I Told You That an Hour Ago — Why Did You Forget?"

You've been refining a report draft with AI for over an hour. At the start, you said: "Use formal register, and no footnotes." Twenty revisions later, the answer comes back — with footnotes. You type "I said no footnotes," and the AI apologizes. If this sounds familiar, you have a concrete reason to understand the context window.

## Everything That Lands on the Desk

The context window is the limit on how much text an AI can hold at once. Sizes vary by model, but the principle is one: **everything in the conversation must fit inside it.** Your questions, the AI's answers, the documents you paste, the small talk along the way — all of it.

Think of it as a desk. The AI can only see what's on the desk. A big desk holds many open documents; a small one forces you to keep putting things away.

The size is measured in tokens, not characters. A token is the unit AI uses to slice text — in English, roughly three-quarters of a word. An A4 page runs to about 500–800 tokens. Today's models have windows of hundreds of thousands of tokens, so a hundred A4 pages fit. Which is why the practical question isn't "does it fit" but "does it get read."

There are two traps here.

First, as the conversation gets long, the early content gets pushed out. Depending on the service, the oldest content may get trimmed away, and even when it stays, later messages crowd it out and its influence weakens. That's why instructions "you gave earlier" get ignored. The AI hasn't developed amnesia — that instruction card has been shoved to the corner of the desk.

Second, fitting inside the limit doesn't mean it gets read properly. Paste a long document whole, and the model tends to focus on the beginning and the end while skipping through the middle — this is what research on long-context models shows. Paste a forty-page business plan and ask about the budget rationale buried on page fifteen, and you'll get a vague answer. The input went in; it just wasn't read carefully.

## What This Looks Like at Work

### Case 1: Pasting a Long Document All at Once

**Before** — You paste an entire forty-page business plan and ask, "Find the weakly supported claims." The answer points out a few obvious sentences near the table of contents. The awkward figures in the budget table on page fifteen go unflagged. You think "AI checked it," and those numbers go straight into your report.

**After** — Split the same document by chapter and feed it in sections. Ask "Find three weakly supported claims in this chapter and explain why," and the quality of the answers changes. Once you've gone through everything, collect the findings from each chapter and run one more review pass. Two stages beat one giant pass.

### Case 2: Letting One Conversation Run Forever

**Before** — You keep revising in the same chat window from morning to afternoon. The tone and structure rules agreed at the start get ignored more and more, and you find yourself repeating the same instruction three or four times. The answers feel bland, and you can't tell why.

**After** — When the unit of work changes, start a new conversation. Restate the rules when you do: "Formal register, no footnotes, paragraphs of three sentences or fewer" at the top of the chat. If the conversation is already long, simply repeating the key instruction right before your request improves the result — models are most faithful to what arrives last.

### Case 3: Handing Off Between Conversations

Sometimes the volume forces you to split the work across conversations. How you split it decides the outcome.

**Before** — You break a forty-chapter manual review into twelve conversations, pasting the raw text into each with nothing but "please review." Each conversation applies its own standard, so the strictness of the feedback varies. When you merge the results, the same sentence got flagged in one conversation and passed in another.

**After** — Put the same criteria at the top of every conversation. Fix the review standard in words — "flag: sentences mixing fact and speculation, figures without sources, inconsistent terminology" — and in the final conversation, collect all findings, deduplicate, and run one consolidation pass. It's the same structure as a person handing off meeting notes between sessions, applied to AI.

The point: the moment you cross the window, shift your attention from "memory" to "handoff." If you design what gets passed to the next conversation, consistency survives even a small window.

## Symptoms, Causes, and Fixes

| Symptom | Cause | Fix |
|---|---|---|
| Suddenly ignores early instructions | Conversation grew and pushed them out | Start a new chat; restate the rules |
| Vague answers about a specific part of a long document | The middle wasn't read carefully | Paste just that section and ask |
| Response says the document is too long | Input limit exceeded | Split the document; lead with a summary |
| Answers get bland late in a conversation | Window filled with chatter, errors, retries | Start fresh with a tidy request |

## What to Check Before You Rely on This

The context window isn't just about size. Recent models advertise hundreds of thousands, even millions of tokens of input — but what fits and what gets read carefully are different things. A bigger desk doesn't mean every page spread across it gets equal scrutiny. Large inputs also mean larger bills and slower responses.

So in practice, flip the question. Not "how much can I put in" but "what is the minimum I should put in." For documents, just the relevant chapters; for conversations, just the instructions and the material at hand. That's what improves accuracy and cost at the same time.

Check your tool's spec once, too. Services differ not only in window size but in what happens when the window overflows. Some reject the input with an error; others silently trim the oldest content. The latter is worse — it means your early instructions disappeared without you knowing. If "but I told you that" keeps happening, suspect an overflow and start a fresh conversation.

Finally, some problems aren't solved by a bigger window. For bulky material you need every time — company policies, for instance — the right structure is retrieval that pulls in only the relevant parts, not pasting the whole thing into every conversation. It's not a memory problem; it's a finding-and-placing-on-the-desk problem. Miss that distinction, and you'll keep getting stuck at the same point no matter how large a window your model has.
