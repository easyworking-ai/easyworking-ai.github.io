---
title: "How to Get an AI Briefing 30 Minutes Before a Meeting"
description: "\"What is this meeting even about?\" — the question you shouldn't be asking for the first time inside the room. A pre-meeting briefing prompt that turns background documents into a question list, plus a review checklist."
created: 2026-09-08
updated: 2026-09-08
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - meetings
  - practical
---

<img class="ewa-article-art" src="/static/img/art-pre-meeting-briefing.jpg" alt="Illustration of a robot looking through a stack of reports and holding up a single organized briefing sheet, lit by a warm amber desk lamp" width="900" height="720" loading="lazy">

## The Moment You Ask "What Is This Meeting About?" — Inside the Room

The invitation says only "Q4 Promotion Performance & Improvement Discussion." The one person who knows what this meeting is for is the organizer; you walk into the room still digging through last quarter's materials. The first 20 minutes go to having documents you didn't read explained to you. When you finally ask a question, the answer comes back: "We settled that in the last meeting." With ten attendees burning 20 minutes each, three hours just evaporated. That is how meeting cost actually adds up.

The reason meetings catch us unprepared usually isn't lack of time. It's not knowing where to start reading, and not knowing what to bring even if you do read. Scanning three reports takes 40 minutes, and days with 40 spare minutes are rare. So preparation gets postponed — and the postponement is exposed inside the room.

AI can fill this gap. Not as a summarizer of documents, but as something that first sorts out **what you personally need to get out of this meeting**. But "summarize these documents" fails here too, because a summary isn't what you need before a meeting. What you need before a meeting isn't a summary — it's questions.

## The Prompt That Works

Copy the prompt below, replace the bracketed parts to match your situation, and paste your background materials at the end.

```
Using the materials below, prepare a pre-meeting briefing for me.

Meeting info:
- Topic: [e.g., Q4 promotion performance & improvements]
- Organizer: [e.g., marketing team lead]
- My role: [e.g., IT Planning — reviewing budget and system requests]
- What I need to walk away with: [e.g., the scale and priority of system change requests]

Briefing format:
1. Background (why this agenda is being discussed now, in 3 sentences or fewer)
2. Discussion so far (what was decided or parked in previous meetings or documents)
3. Key numbers and dates (only the figures and deadlines that appear in the materials)
4. Issues that concern me (only the parts relevant to my role)
5. 3–5 candidate questions to ask in the meeting (questions whose answers would actually help me decide)

Materials:
"""
[paste the meeting invitation, previous minutes, reference reports, etc.]
"""
```

Three things separate this prompt from a document summary.

First, **it states your position**. The same materials contain different key points for a marketing owner and an IT Planning owner. Leave the role out, and the AI produces a neutral summary that pretends to matter equally to everyone — which is useless to you specifically.

Second, **it defines what you're there to get**. With a purpose like "reviewing budget and system requests," the AI knows which parts of the materials to stare at. The goal of the 30 minutes before a meeting isn't knowing everything — it's having the minimum you need to make your own judgment.

Third, **it produces candidate questions**. This is the heart of the prompt. The difference between a prepared attendee and an unprepared one isn't speaking volume — it's question precision. Take the candidates, refine them, and you walk in as the person who names the crux, not the person who missed the last meeting's decision.

## Review Checklist

Don't walk into the room trusting the AI's briefing. Two minutes of checks:

- [ ] Are the key numbers and dates actually in the materials? (AI sometimes invents plausible figures)
- [ ] Is everything listed under "decided" genuinely decided? (Promoting a mere discussion to a decision tangles the meeting)
- [ ] Have you filtered out candidate questions that don't fit your position?
- [ ] Does anything contradict what you already know? (If so, your materials may be outdated)

The first item is the most dangerous. A briefing is a document you glance at mid-meeting, which makes it easy to quote a wrong number out loud. Base an argument on a bad figure and the rest of the meeting goes to repairing it.

## Going Further: Batching a Whole Week

If you have four recurring meetings a week, you can't run this every time. Run the whole week on Friday.

```
Below are invitations and background materials for my four meetings next week.
Produce a briefing in the same format as above for each meeting.

Additional rules:
- When the same agenda spans multiple meetings, mark which meeting the decision will actually land in
- List any materials or numbers I need to prepare, separated by meeting
- If any issue cuts across meetings, group it under "this week's through-line issue"

Materials:
"""
[paste invitations and materials for each meeting, clearly separated]
"""
```

Seen as a week rather than one room at a time, things become visible that aren't otherwise. If Tuesday's decision is a premise for Thursday's discussion, coasting through Tuesday means getting dragged along on Thursday. That's why you ask for the through-line issues.

## The Limits of This Prompt

No background materials, no briefing. If all you have is a one-line invitation and no obtainable minutes, running this prompt makes the AI invent a background. That "discussion so far" would be pure speculation — and walking in armed with speculation is worse than walking in unprepared. With fewer than two documents, asking the organizer directly is faster.

Office politics sit outside this prompt's reach. Which question will irritate the organizer, who backed down at the last meeting — none of that is written in the documents. The person who does well in meetings isn't the one who fires off every candidate question the AI produced, but the one who picks the two or three that fit the moment. The standard for choosing them still has to live with a human.
