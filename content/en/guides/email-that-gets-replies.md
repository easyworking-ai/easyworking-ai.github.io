---
title: "The Email Prompt That Gets Replies — Not \"Politely\""
description: "When you tell AI to \"write politely,\" you get a stiff, formal email. A prompt for crafting emails that make recipients want to reply, plus common mistakes."
created: 2026-07-27
updated: 2026-07-27
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - email
  - practical
---

<img class="ewa-article-art" src="/static/img/art-email-replies.jpg" alt="Illustration of a worker drafting an email in three marked sections while a robot nods in approval" width="900" height="900" loading="lazy">

## The Problem With "Write Politely"

When asking AI to draft an email, the most common instruction is "write politely." The result is predictable: an email starting with "Dear Sir/Madam, thank you for your inquiry" that loses the reader before they've even started.

The problem is that "politely" gives the AI no specific guidance. AI interprets "polite" as "formal written style." But in real work emails, "polite" doesn't mean formal — it means **a tone that doesn't burden the recipient**.

The difference between emails that get replies and emails that don't isn't politeness — it's **clarity**. If the recipient can't figure out "how should I respond to this?" within 3 seconds, the reply gets delayed. And delayed replies never come.

## A Prompt That Works

```
Write an email with the following details:

Recipient: [Title/Name]
Purpose: [One sentence explaining why you're sending this]
Request: [Specifically what you need from the recipient]
Deadline: [When you need a reply by]
Context: [Only if necessary, two sentences max]

Conditions:
- State the purpose in the first sentence
- List requests as numbered items
- Remove phrases like "I will review this carefully" — write specifically what needs to be done
- Keep greetings to one line, closings to one line

Content:
"""
[Roughly write what you need to convey here]
"""
```

The key to this prompt isn't "politely" — it's specifying **structure**.

When the first sentence states the purpose, the recipient knows "Ah, this is about ~" as soon as they open the email. When requests are numbered, what needs to be done is clear at a glance. When a deadline is explicit, "I'll reply later" becomes "I need to reply by Friday."

## Common Mistakes

**Adding "I will review this carefully"**

AI automatically inserts "I will review this carefully." This phrase means nothing and helps no one. You should write specifically what will be reviewed and by when. That's why the prompt explicitly instructs to remove this phrase.

**Context section is too long**

The "Context" field should only be used when necessary, and kept to two sentences or fewer. AI tends to elaborate on context. "As a follow-up to item 3 discussed in last week's meeting, this requires department head approval" — this is enough in one sentence. If you don't explicitly say "two sentences max" in the prompt, AI will write three or more sentences.

**Sending the same content to multiple people**

When sending the same request to multiple people, split the email so each recipient only sees what's relevant to them. Tell the AI "write the same request to three people but emphasize different parts for each" and it will create recipient-specific emails. If you put all three in one email, each person will wonder "Is this my task or theirs?"

## Review: Read It and Spend 3 Seconds Thinking

Before sending the AI-written email, check one thing:

> "If I were the person receiving this email, would I know what to do within 3 seconds?"

If the answer is yes, send it. If it's "I understand what it's about but not what I need to do," the requests are unclear. If it says "I would appreciate it if you could review it in this general direction," the recipient will also "generally" review and "generally" reply.

## Limitations: Emails Where Relationships Matter

For apology emails to clients, rejection notices to superiors, or emails in conflict situations — don't use this prompt. In these cases, what matters isn't "politeness" but relationships and context, and AI doesn't know that context. Here, have AI draft the email first, then have a person manually adjust the tone.
