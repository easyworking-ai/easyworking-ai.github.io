---
title: "A Prompt for Turning Scattered Work Notes into a Handover Document"
description: "Ask AI to \"turn these materials into a handover document,\" and it will summarize each source type separately and invent procedures that were never there. A two-step prompt and review checklist that first extracts a question list, then fills in only answers supported by evidence."
created: 2026-11-17
updated: 2026-11-17
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - handover
  - workplace
---

<img class="ewa-article-art" src="/static/img/art-handover-doc.jpg" alt="An illustration of a robot organizing scattered notes and document fragments into a structured binder under an amber lamp" width="900" height="900" loading="lazy">

## Why “Just organize it” fails

A colleague has left the company. What remains is twelve pages of personal notes, five Excel files, the results of searching the mailbox for “orders,” and several months of conversations in the team chat.

You paste all of it into AI and write, “Organize this into a handover document.” Half a day later, AI returns a polished document. It has a table of contents, neatly separated sections, and smooth prose. The problem appears when someone actually starts the work. You open the document on Monday to place an order, only to find no answer to “Who needs to approve this?” There is no approval deadline either. Instead, the document contains lines such as “Monthly routine checks are recommended”—procedures that appeared nowhere in the source material.

AI organized the material **by source type** (notes summary, email summary, chat summary), not **by the order in which the work is done**. It also filled the gaps by making things up. Both are dangerous in a handover document. When the structure follows the sources, you cannot find what you need; when the blanks are filled in, you may carry out a procedure that never existed.

The fix is to reverse the order. Do not start with the materials; **start with questions**. First extract the questions a new owner is likely to search for during their first month, then find evidence in the materials and attach an answer to each question. Leave questions with no answer as “Not in the materials.” That list becomes what you need to ask the departing employee and what you need to verify yourself.

## Working prompt

Use it in two stages. When you run it all at once, the questions get tailored only to what appears in the materials, and the gaps stay hidden.

**Stage 1 — Extract a question list**

```
Below are the work materials left by the person who handled this work before leaving. Extract the questions a new person taking over might look up during their first month.

Conditions:
- Divide them into four areas: ① what needs to be done (procedures) ② who to communicate with and how (relationships) ③ when recurring work is done (schedule) ④ whom or where to ask when something goes wrong (response)
- Write them in wording someone would actually search, such as “How do I place an order?”
- Include questions whose answers do not appear to be in the materials. Those are the real gaps.

Source materials:
"""
[Paste the notes, emails, and chat records separately]
"""
```

**Stage 2 — Fill in evidence-based answers**

```
Find evidence in the attached materials and write an answer to each question below.

Conditions:
- Add the source supporting each answer in brackets, such as [Notes] or [Email, March 14]
- If an answer is not in the materials, do not make it up; leave it as “Not in the materials”
- If an answer is spread across multiple materials, combine it and write it in procedural order
- At the end, collect a separate list of the items marked “Not in the materials”

Question list and source materials:
"""
[Paste the question list from Stage 1 and the materials together]
"""
```

Why split it into two stages? When Stage 1 extracts the questions first, AI looks not only for what is in the materials but also for **what is missing**. Without the condition “Include questions whose answers do not appear in the materials,” the questions get shaped around the materials and the gaps never surface. In a handover, the most dangerous document is the one that hides its blanks.

The key to Stage 2 is the evidence tag and “Not in the materials.” When every answer carries its source, you can immediately see where it came from during review. Items left as “Not in the materials” become both a question list to send to the departing employee and a task list for you to verify. You are not erasing the gaps from the document; you are turning them into the next actions.

## Review checklist

Do not upload the returned document to the team wiki as is. Check the following before publishing.

- [ ] Does every answer have an evidence tag? (A sentence without a tag was filled in by AI.)
- [ ] Did you send the “Not in the materials” list to the departing employee? (If you do not ask now, you may never get the chance.)
- [ ] Are the owner, contact, frequency, and deadline written as actual names and numbers? (“Check with the relevant department” is not an answer.)
- [ ] Did I open the original source materials behind the evidence and review them one by one? (AI sometimes attaches the wrong citation.)
- [ ] Can a new owner execute the first week’s work using only this document?

## Application: Have the departing person prepare it in advance

The departing employee can use this prompt ahead of time too. Change just one condition.

```
List 30 questions the person taking over would look up during their first month if I stopped handling this work.
Review the notes and materials I left behind, and put [Needs confirmation] next to any question whose answer is not in the materials.
```

Preparing it in advance lets you ask the departing employee about the “Not in the materials” items right away. The cheapest time to fill the blanks in a handover document is not after the person leaves; it is before they leave.

## Limitations of this prompt

AI does not know what is missing from the materials. No matter how well the questions are extracted, if the materials contain no answer, the result is simply “Not in the materials.” Filling that gap takes a call with the departing employee or a check of the vendor’s mailbox. The prompt only makes the gap **visible**.

You also need to check whether the materials are outdated. An approval process changed last year may not be reflected in this year’s notes. If a source has a date, have the AI include that date next to the answer, and verify with the current owner whether evidence older than one year is still current.

Chat logs mix jokes with work-related messages. AI occasionally turns a joke into a procedure. Read every answer that names a person or department yourself at least once.
