---
title: "7 Things to Check When AI Drafts Your Report"
description: "When you say \"write a report,\" AI creates something that looks professional but is hollow. Give it structure, give it data, and set verification checkpoints — then AI produces a useful draft. 7 checkpoints and a prompt."
created: 2026-07-30
updated: 2026-07-30
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - report
  - practical
---

<img class="ewa-article-art" src="/static/img/art-report-checklist.jpg" alt="Illustration of a worker scrutinizing an AI-drafted report under a lamp while the robot waits" width="874" height="900" loading="lazy">

## What "Write a Report" Produces

You need to write a monthly sales report. You open the Excel file — the data is there, but you don't know where to start. You ask AI. "Write this month's sales report." AI returns a report in 3 seconds. Every paragraph is numbered, there are subheadings, even a "Conclusion" section. You read it. It looks professional.

You send it to your manager. Ten minutes later, you get a call. "The month-over-month growth rate looks off. Are these numbers correct?" You check the data again. The growth rates AI wrote don't match the actual data. AI estimated and filled in the numbers. Also, it says "B2B channel shows clear growth momentum" — but you never showed it any B2B data. AI fabricated a plausible-sounding sentence.

That's the result of "write a report." The format is perfect and the content is empty.

## The Root Cause

AI needs to know **what to write** to write it well. "Write a report" doesn't tell it what to write. In this situation, AI generates the most report-like format it can. It doesn't use actual data — it estimates "this is what a sales report would typically contain" and fills it in.

The points where reports fail are predictable: no structure, no data, no comparison baseline, and no defined reader. Leave any of these four blank, and AI fills it in. And it's usually wrong.

## A Prompt That Works

Use this prompt as your starting point for report writing. Replace the bracketed values with your actual information.

```
Draft a [report type] based on the following data.

Conditions:
1. Report purpose: [What decision will this report drive?]
2. Reader: [Manager / Executive / Client, etc.]
3. Structure:
   - Overview (2 sentences explaining why this report is needed)
   - Key figures (presented in a table)
   - Month-over-month / quarter-over-quarter changes and causes
   - Notable items (deviations from expectations)
   - Proposed next steps
4. Analysis metric: [Revenue volume / Revenue amount / Net profit — which to use as the baseline]
5. Comparison period: [June 2026 vs. May 2026]

Data:
"""
[Paste data copied from Excel here]
"""

Important:
- Never fabricate numbers not present in the data
- Write "Not available in data" for anything you don't know
- Mark sections requiring estimation as [Estimation needed]
```

## 7 Checkpoints

Before sending the AI's draft, you must verify all of the following.

**1. Are the numbers accurate?**
This is where errors are most common. AI makes mistakes adding and subtracting numbers. Cross-reference every figure in the draft against the original data. Growth rates, percentages, totals — check each one. Rounding differences are especially common.

**2. Does it contain content not in the data?**
Check if there are analyses like "B2B channel growth momentum" that don't come from the data. AI has a habit of appending plausible interpretations. Remove anything that can't be directly verified from the data.

**3. Is the comparison baseline stated?**
"It increased" — compared to what? Month-over-month, year-over-year, or versus target? The most common misunderstanding in reports happens when the comparison baseline isn't stated. Readers assume their own baseline.

**4. Do causal claims have evidence?**
"Sales increased due to new product launch effect" — can you prove this causal relationship with data? AI describes correlations in data as if they were causal relationships. If you want to claim causality, you need evidence. Without it, write only "A new product was launched during the same period" and nothing more.

**5. Can the reader finish it in one sitting?**
A report is someone's decision-making tool. Nobody reads a 10-page report. If the draft is too long, keep only the overview, key figures, and next steps, and move the rest to an appendix. The reader should be able to reach the conclusion within 3 minutes.

**6. Are the "next steps" actionable?**
"Continuous monitoring is needed" is not a next step. It needs to specify who will do what, by when. If the next steps AI wrote are abstract, convert them to concrete actions.

**7. Can I explain every sentence?**
For every sentence in the draft, you must be able to answer "Why was this written this way?" Sentences you can't explain can't be trusted. They're either AI's estimates or interpretations not supported by the data. Find them and delete or revise them.

## Application: Merging Department Reports into One

Sometimes each team member uses AI to draft their department report, and then you need to combine them. If everyone used different prompts, merging is hard because the structures don't match.

The solution is simple. Have the entire team use the same prompt structure. Make the prompt above the team's shared template, with each person only changing the data. Then when you merge, the structures align and you can combine them in one pass.

```
Below are 3 department reports, all written in the same structure.
Combine them into a single consolidated report.

Conditions:
- Consolidate each department's key figures into one table
- Summarize commonly occurring notable items at the top
- List each department's next steps separately with the department name
- Mark sections requiring consolidated analysis as [Consolidated analysis needed]

Department reports:
"""
[Department A report]
[Department B report]
[Department C report]
"""
```

## Limitations of This Prompt

If the data quality is poor, the draft will be poor too. When copying data from Excel, if columns are misaligned, numbers are recognized as text, or there are blank cells, AI can't understand it. Minimal cleanup before pasting — checking headers, removing blanks, standardizing units — is necessary.

Also, if you paste a large volume of data at once, AI may not process all of it. In that case, you need to split the data into sections, analyze each separately, and then combine the results. That method is covered in "How to Feed Long Documents to AI."
