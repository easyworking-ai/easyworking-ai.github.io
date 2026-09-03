---
title: "What Multimodal AI Actually Changes at Work — the Retyping Disappears"
description: "Multimodal doesn't mean AI got smarter; it means the busywork of converting everything into text is gone. Dropping in a full meeting recording or a table screenshot — and the limits you should know about."
created: 2026-09-03
updated: 2026-09-03
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - multimodal
  - practical
---

<img class="ewa-article-art" src="/static/img/art-multimodal-in-practice.jpg" alt="An illustration of a robot inspecting a photo of a table up close, with a stack of retyped documents pushed aside" width="900" height="600" loading="lazy">

## "Can I just upload this screenshot of the table?"

That question came up in a team chat. Someone posted a capture of a sales report and asked, "Can I ask AI about this, or do I need to retype it as text?" A year ago the answer was "retype it." Today it's "just upload it."

How we work reorganizes around that answer. The word for this shift is multimodal.

## Multimodal is not a complicated idea

A modality is a form of information. Text, photos, sound, video — each one is a modality. Chatbots used to read only text. So whatever you had, you converted it into text first. To ask about a table, you copied cells over one by one. With a meeting recording, you listened and typed notes as you went. A scanned contract couldn't be copied at all, so you read it off the screen and transcribed it line by line.

A multimodal model takes the original as-is. Paste a screenshot and it looks at the image. Upload a recording and it listens. Hand it a scanned PDF and it reads the pages.

Here's an analogy. The old AI was an outside consultant who only communicated in writing. However good your material, you had to reformat it into a document before sending. Now that consultant sits in the meeting room, watches the screen with you, and listens to the recording. The consultant didn't suddenly get smarter — the way you meet changed.

One scoping note. Multimodal also covers output: generating images or voices. But the part that changes daily work right now is input. That's what this article focuses on.

## The same task, before and now

### A 60-minute meeting recording

Before, you listened through the recording and noted decisions and owners. Listen, pause, write, repeat — it took longer than the recording itself.

Now you upload the file and write, "Pull out what was decided, what was deferred, and who owns what." A draft comes back in a few minutes, and you spend five minutes polishing it.

The difference isn't only speed. The old workflow had you doing two things: listening and judging, and typing. Once typing drops out, your attention goes to judgment.

### One screenshot of a table

Before, if a report a colleague sent raised a question, you had to find and open the original file, or retype the table into text.

Now you paste the screenshot and ask, "How did Q3 sales change versus Q2? Anything that looks off?" The model reads the table, answers, and can point out a column whose totals don't add up.

### Handwritten notes and scanned documents

Field notes scribbled in margins, a contract photocopied and scanned. Getting text out of these used to mean running separate OCR. Now you take a photo, upload it, and instructions like "make just the payment terms into a table" work.

## How far can you trust it

| Input | Before | Now | Check before handing it over |
|---|---|---|---|
| Tables, screen captures | Retype as text | Paste the original | Small text and digits get misread. Verify key figures against the source |
| Meeting and interview recordings | Listen and take notes manually | Upload, then extract summary and items | Proper nouns — names, product names — get misrecognized |
| Scanned PDFs, handwriting | Run OCR, then retype | Upload the photo or file as-is | Poor scans lead to misread clause numbers |

One rule covers all of it. A multimodal model's eyes and ears are probabilistic. Just as a person skims a blurry photo, the model can invent a reading for an unclear input. Numbers are the biggest risk: if it misreads one small digit in a table, every calculation downstream is wrong.

## What to check before you hand things over

**Does the file contain personal or confidential information?** A meeting recording carries voices and real names. Before uploading customer documents or contract scans to an external service, check your company's data policy first. Whether submitted data is used for training differs by service — look up the policy for the one you use.

**Easier input means more review.** Before, retyping forced you to skim the material. Now that you hand over the original, a new step is needed: checking whether the model actually read it right. Budget time to verify that names in the extracted minutes are correct and that numbers read from a table match the source.

**When not to use it.** A blurry scan, a graph whose axis is cut off, a recording where several people talk at once. And if the extracted content feeds something with legal force — contract payment terms, for instance — always cross-check against the original text. Multimodal AI is a fast drafter, not a notary that confirms for you.

To sum up: what multimodal changes is not AI's intelligence but the labor of conversion. The typing disappears, and that time goes to judgment and verification. Start with one meeting recording or one table screenshot, put it in directly, and lay the result over the original — you'll get a feel for how far you can delegate in your own work.
