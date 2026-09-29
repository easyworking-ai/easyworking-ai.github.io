---
title: "How Not to Send AI Work Results Straight to Your Team"
description: "If all you write is \"Had AI put this together,\" the first question that comes back is \"Where did this number come from?\" A sharing prompt and review checklist for sending work with its verification basis and limitations attached."
created: 2026-09-29
updated: 2026-09-29
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - collaboration
  - workplace
---

<img class="ewa-article-art" src="/static/img/art-share-ai-output.jpg" alt="An illustration of a robot handing over a stack of reports with an amber verification seal and a blank tag" width="900" height="900" loading="lazy">

## Why “Had AI put this together” fails

Suppose you ask AI to make a comparison table of competitors’ pricing plans. After polishing it for about an hour, you post it in the team chat. The attachment contains a clean table, and the message says only, “I had AI put this together.”

Most responses are similar. It starts with, “Where did the number in row 3 come from?” followed by, “As of when is this?” The worst case is when it passes without a single question. No one trusted it, so no one read it. The next time you post an AI-generated result, no comments come at all. The problem is not the quality of the output; it is that **the recipient cannot tell how far they can trust it**.

The first question from someone who receives an AI work result is not, “Is this correct?” It is, “Which parts of this can I use as material for my judgment?” If you do not answer that question, the output is not read and simply passes by. A shareable document that gets read includes three things: what was made (the output), what was checked (the verification basis), and what cannot be trusted (the limitations).

## Working prompt

After asking AI to do the work, copy the entire result and paste it into the prompt below. The AI repackages its own result in a format suitable for sharing with the team.

```
The following is the work result you just created. Reorganize it into a format that can be shared with the team.

Format:
1. One-line summary — what the team can do with this result
2. Output — keep the table or list as is
3. Verification basis — for each item, distinguish and label “based on the materials I provided” / “my inference”
4. Unverified parts — list the items a person needs to verify
5. Limitations — situations in which this result should not be used

Rules:
- For the items that are inferences in section 3, identify the supporting material by name
- Do not leave section 4 blank. Write “none” only when you can honestly say there are none
- In section 5, describe specific situations instead of vague wording such as “for reference only”

Work result:
"""
[Paste the AI-generated result here]
"""
```

The difference between this prompt and “I’ll clean it up and send it to the team” comes down to three things.

First, **it separates facts from inferences**. The dangerous thing in an AI output is not simply that some content may be wrong; it is that content that could be wrong is mixed with correct content in the same format. Item 3 forces a source onto each row.

Second, **it requires “Unverified parts” without allowing the field to be left blank**. It makes the AI admit its own verification status. AI usually overestimates the confidence of its results, so if you do not request this item, it will move on with “Everything has been checked.”

Third, **it makes the AI describe limitations as situations**. “For reference only” tells you nothing. The recipient can make a judgment only when the situation in which the result cannot be used is explicit, such as, “This table is based on domestic pricing plans, so it cannot be used to compare overseas subsidiaries.”

## Review checklist

Do not send the AI-packaged shareable document as is. Take one minute to check it before sending.

- [ ] Does every item in the output have a verification basis label?
- [ ] Are there actual items under “Unverified parts”? (If it is completely empty, that means it was not checked.)
- [ ] Did I open and verify myself every item labeled “based on the materials” in section 3?
- [ ] Does the limitations sentence describe a specific situation? (“For reference only” is not a limitation.)
- [ ] Does the one-line summary include the recipient’s next action?

Section 3 is the part that belongs to the person. Even items AI labels “based on the materials” can be wrong. It may have misread the material, or the material I provided may itself be outdated. A person still has to do the checking, but because the items to check are already separated, there is no need to dig through everything; just look at those items. That is the practical benefit of this format.

## Application: Make it a team document template

Use this structure once and discard it, and next time you will be back to “AI put this together.” Add three status labels to the team document template to keep the format consistent.

- **Draft** — exactly as AI produced it. Do not share.
- **Awaiting verification** — the format is in place, but unverified items remain.
- **Verified** — a person has checked the evidence items. It can be used as meeting material.

Even creating one rule to put this label at the beginning of the document title changes how the team handles AI output. The moment a person has to explain the status verbally instead of the document making it clear, the document is once again forced to rely on trust.

## Limitations of this prompt

If it looks as though verification has been delegated to AI, this format has failed. This prompt does not perform verification; it **extracts a list of things to verify**. Recalculating numbers and reopening source materials remain the person’s responsibility.

Ultimately, a person is also responsible for the limitations sentence. AI does not know well where its own result will break down. Mistakes such as applying a table built from domestic data to overseas cases can be caught only by someone who understands the context in which the result will be used. Section 5 should be used as a place where a person takes the AI draft and adds one more sentence.

Finally, once a team’s trust is broken, the cost of restoring it is high. If one unverified table is overturned in a meeting, every subsequent result will be met with suspicion even if its format is perfect. It is much cheaper to attach the output, basis, and limitations from the start.
