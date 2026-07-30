---
title: "The Prompt That Summarizes Meeting Notes in 3 Minutes"
description: "When you write \"just give me the key points,\" the AI picks whatever it thinks is important. A prompt and review checklist for keeping only the information your team actually needs in meeting notes."
created: 2026-07-27
updated: 2026-07-27
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - meeting-notes
  - practical
---

## Why "Just Summarize the Key Points" Fails

It's the most commonly used prompt. And the most commonly failing one.

After a meeting, you toss the transcript to the AI and type "just summarize the key points." The AI returns a clean summary. The problem starts when you send it to your team. "When was this decision made?", "Who agreed to do that?", "The deadline is missing." The "key points" the AI picked differ from what the team actually needs.

The AI picks sentences that "look important." But in meeting notes, what matters isn't sentences — it's **decisions, owners, deadlines, and next steps**. Unless you explicitly extract these four things, the summary looks pretty but is useless.

## A Prompt That Actually Works

Paste this prompt before your meeting transcript. Replace the content inside the quotes with your actual meeting notes.

```
Summarize the meeting notes below using the following format:

1. Meeting info (date, attendees, topic)
2. Items discussed (one line each)
3. Decisions made (who, what, by when)
4. Items pending (to be discussed at the next meeting)
5. Next meeting schedule

Meeting notes:
"""
[Paste your meeting notes here]
"""
```

This prompt differs from "just summarize the key points" in three ways.

First, **it specifies what to extract**. Instead of having the AI pick what "looks important," it structurally pulls out decisions, owners, and deadlines.

Second, **it fixes the format**. There are numbered sections 1 through 5, and each has a defined purpose. When team members receive the summary, they know exactly where to find what.

Third, **it separates pending items**. Things not yet decided are kept out of "decisions made." This matters more than you'd expect. When "discussed" and "decided" are mixed together, someone will mistake a discussion item for a decision and start executing.

## Review Checklist

Don't send the AI's summary as-is. Spend 30 seconds checking.

- [ ] Does every decision have an owner's name?
- [ ] Is the deadline explicitly stated? ("As soon as possible" is not a deadline)
- [ ] Are pending items not mixed in with decisions?
- [ ] Is there anything in the summary that differs from what I heard in the meeting?

The last item is the most important. You can spot mistakes in the AI's summary because you attended the meeting. Someone who didn't attend would have believed the incorrect information as fact. Having someone who can review the AI summary confirm it at the end is essential.

## Application: Compiling Weekly Summaries

If you summarize meeting notes daily, you can combine a week's worth on Friday.

```
Below are 5 meeting note summaries from this week. Combine them into one.

Conditions:
- If the same item was discussed in multiple meetings, keep only the final decision
- Mark overdue items as "Done" or "Postponed"
- Keep only items for next week's discussion in "Pending"

Meeting summaries:
"""
[Paste Monday through Friday summaries in order]
"""
```

This way, on Monday morning you can send the team a single-page "Last Week's Decisions." Team members who ignore daily summaries will read the weekly one.

## Limitations of This Prompt

If the meeting notes are poor, the AI can't fix them. If there's no record of who spoke, the AI can't identify owners. If decisions aren't recorded, the AI will fabricate them. The most dangerous case is when the AI infers and fills in content. If the notes themselves are a mess, you need to fix how meetings are recorded before you bother fixing the prompt.

One approach is to have the AI transcribe audio recordings first, then apply this prompt. In that case, speaker identification may not be perfectly accurate, so the owner section must always be verified by a person.
