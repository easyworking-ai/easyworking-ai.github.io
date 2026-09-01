---
title: "Why AI-Translated Business Emails Sound Like Translations"
description: "\"Translate this\" makes the AI translate sentence by sentence. A translation prompt that passes along intent and relationship to produce natural English emails, plus a review checklist."
created: 2026-09-01
updated: 2026-09-01
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - translation
  - practical
---

<img class="ewa-article-art" src="/static/img/art-translation-prompt.jpg" alt="Illustration of a robot at a desk holding up a freshly rewritten letter while the original document lies flat below, lit by a warm amber lamp" width="900" height="900" loading="lazy">

## Why "Translate This" Fails

You're staring at an English email you need to send to a partner company, so you hand your Korean draft to the AI. "Translate this." English comes back in seconds. Nothing is grammatically wrong. But read it again and something feels off: "Please kindly confirm the below matters at your earliest convenience." The sentences are correct, yet anyone who has exchanged emails with overseas clients knows — the formality is excessive, the request is indirect, and the Korean sentence structure is showing through.

The problem isn't the AI's translation ability. It's that you told it nothing. "Translate this" contains exactly one instruction: convert sentences into sentences. The AI obeys. But in an email, what needs to move across languages isn't sentences — it's **intent and relationship**. The same "please review this" calls for different wording when it's going to an overseas buyer you're contacting for the first time versus a global teammate you've worked with for three years.

Korean business email is especially unfriendly to literal translation. Expressions like "검토 부탁드립니다" (please give it your review), "차질없이 진행하겠습니다" (we will proceed without delay), and "회신 주시면 감사하겠습니다" (I would appreciate your reply) are natural in Korean, but word-for-word they turn into English that is stiff or oddly ceremonial. Korean is a language that makes requests indirectly; English is natural when it asks directly, as much as needed. Closing that gap is less translation than rewriting — which is why it has to be part of the instruction.

## The Prompt That Works

Copy the prompt below, replace the bracketed parts to match your situation, and paste your draft email at the end.

```
Rewrite the Korean email below as an English business email.

Context:
- Recipient: [e.g., a contact at a partner company, first time reaching out]
- My relationship with them: [e.g., we are the buyer, they are the supplier]
- Purpose of this email: [e.g., requesting a 3-day extension on next week's delivery schedule]

Rules:
- Use concise business written English. No excessive formality like "Please kindly" or "at your earliest convenience"
- Keep all numbers, dates, names, product names, and amounts exactly as in the original
- Replace set Korean phrases like "please review this" with requests that sound natural in English
- Don't follow the Korean sentence order — rearrange freely to match English email conventions

After the translation, also show me:
1. Two or three spots that would have read awkwardly if translated literally, and how you changed them
2. Any sentences you added that weren't in the original, following English email convention

Original email:
"""
[paste here]
"""
```

Three parts of this prompt do the work.

First, **the three lines of context**. When the AI knows who the recipient is, what the relationship is, and what this email is for, it gains a standard for choosing sentences. Whether it's a first contact or a long-standing working relationship changes the level of formality.

Second, **the list of things that must not change**. The most dangerous translation errors aren't about style — they're about numbers. Shift a date by one day or a single digit in an amount, and you have an email that reads beautifully but says the wrong thing. Specifying what to preserve draws that boundary in advance.

Third, **the post-translation report**. Making the AI disclose what it changed from a literal translation means you don't have to review the whole email — you check the spots it points out. The review area shrinks from the entire text to a few sentences.

## Review Checklist

Don't send the output as-is. One minute before you hit send:

- [ ] Do all numbers, dates, names, and amounts match the original exactly?
- [ ] Can you state in one sentence what the recipient needs to do? (If the action is blurry, it's a greeting, not a request)
- [ ] Does the formality match the relationship? (Not too casual for a first contact, not stiff for an internal colleague)
- [ ] Did the AI add any sentences that weren't in the original? (It sometimes inserts courtesy phrases on its own)
- [ ] Are meta details like attachment mentions and cc notifications still there?

## Going Further: Replying to an English Email

What happens even more often than translating is replying. You write your reply to an English email in Korean, then convert it back into English — a double job. You can bundle it into one pass.

```
Below are an English email I received and my Korean draft reply.
Turn the draft into a finished English reply.

Rules:
- Match the formality level of the email I received
- Check that my draft answers every question they asked. Where an answer is missing, mark that spot with [NEEDS INPUT]
- Follow the sender's style for greetings and sign-offs

Email received:
"""
[paste here]
"""

My draft reply:
"""
[paste here]
"""
```

The key is the [NEEDS INPUT] marker. When writing a draft, it's easy to miss one of the questions you were asked. If the AI finds the unmatched question and marks it, you just fill that spot before sending. Reply quality is decided more by what you didn't miss than by how elegant the sentences are.

## Limits of This Prompt

What translation can't carry is context. Deal history, an ongoing dispute, the other party's mood — none of that fits in a prompt. If the recipient is already frustrated, the same sentence needs to be written differently, and the AI doesn't know that. You asked it to match the formality level, but whether that formality fits this situation is a human judgment.

Emails with legal force — contract terms, delivery penalties, liability scope — must not end with an AI translation. A natural-sounding sentence and an accurate condition are two different things, and an error in the latter escalates to the contract stage. These emails go through legal or contract review after translation.

Finally, read the finished email out loud once. How the recipient will feel reading these lines is still something no AI can compute for you.
