---
title: "How to Keep AI-Generated Tables Out of Your Report"
description: "AI-generated comparison tables look finished, which makes people skip verification. A prompt and review checklist for checking numbers in three steps: tracing sources, recalculating, and cross-checking."
created: 2026-08-25
updated: 2026-08-25
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - report
  - verification
  - work
---
<img class="ewa-article-art" src="/static/img/art-verify-ai-tables.jpg" alt="Illustration of a robot using a magnifying glass to compare numbers in a report table with the original documents" width="900" height="900" loading="lazy">

## When an AI-Generated Table Fails

You needed a table for a quarterly report. You pasted three past reports into AI and typed, "Create a table of quarterly revenue growth for the past three years." A finished table came back in seconds. The alignment was clean and the units matched. You dropped it straight into the report draft.

The day after the executive meeting, the strategy planning team called. "The revenue figure for Q3 2024 doesn't match our data." When you checked, AI had copied one number incorrectly while moving figures across two reports, and it had filled a cell that did not exist with an estimate. If it had been prose, you might have noticed something odd while reading. Tables are different. When numbers run neatly across the page, people tend to scan past them without reading the contents. The more finished a table looks, the easier it is to skip verification. That's the problem.

AI-generated tables usually go wrong in three places.

1. **Numbers with no source.** It fills cells that aren't in the data with plausible values instead of leaving them blank. It may have pulled a similar figure from its training data, or it may simply have guessed.
2. **Calculation errors.** It gets derived numbers such as growth rates, totals, and shares wrong. AI is unreliable with arithmetic involving many digits.
3. **Mixed-up time periods.** It puts a 2023 survey figure in the table as if it were a 2025 number. Even if the table includes a year, that year may still not match the year of the source.

## A Prompt That Works

When you ask AI to make a table, add three conditions. Do not let it fill cells it cannot source, make it show its calculations, and make it disclose conflicts between sources.

```
Create a comparison table from the material below.

Rules:
- Use only numbers that appear in the material. Never guess to fill cells that are not in the material; leave them as "Data not available"
- Add a source next to each number. Use the format "material name + the relevant sentence"
- If you calculate a growth rate or total, show the formula separately below the table
- If the numbers differ across sources, do not choose one and hide the other. Show both and explain which source is newer

Table to create:
[Write the table format directly here. Example: Year (rows) x Product category (columns), unit: KRW 100 million]

Material:
"""
[Paste the report, meeting minutes, or Excel data here]
"""
```

This prompt differs from "make a table" in three ways.

First, **it allows blank cells.** If a "Data not available" cell appears, a person fills it in. A blank is better than an AI-generated estimate. A blank signals that someone needs to fill it; a plausible number makes everyone look past it.

Second, **it requires sentence-level sources.** "Source: 2024 annual report" isn't enough. Ask which sentence the number came from so you can compare it with the original later. Treat a number with no source as a number AI made up.

Third, **it prevents the AI from hiding discrepancies across sources.** When two sources report different numbers, AI usually picks one. Deciding which source is newer is a human job, so structure the output to hand you the evidence you need.

## Review Checklist

Check the table before putting it in a report. If there are many numbers, you may not be able to check every one, so start with the figures that would cause the most trouble if they were wrong.

- [ ] Does every number have a source? Have you left any "Data not available" cells as they are?
- [ ] Did you recalculate totals and growth rates with a calculator or spreadsheet?
- [ ] Did you verify the three numbers that directly affect the report's conclusion against the original source documents?
- [ ] Is the reference period for each number (survey year, quarter) stated in the table?
- [ ] Can you tell which figure you used in the final table where sources disagreed?

The third item is the most useful in practice. You cannot verify every number in a table. Instead, use the question "Would the report's conclusion change if this number were wrong?" to choose three figures and open the original documents. Put your verification time into those three numbers.

## Application: Move Derived Numbers to a Spreadsheet

If a large share of the table depends on AI's calculations, do not outsource the calculations to AI. Have AI extract only the original numbers and sources, then calculate growth rates and totals with spreadsheet formulas.

```
Extract only the original numbers to put in the table from the material below. Do not calculate anything.

Format:
| Item | Number | Unit | Reference period | Source sentence |

Material:
"""
[Paste the material here]
"""
```

Transfer the numbers you get back into a spreadsheet, and let formulas calculate the growth rates. Because AI does not calculate them at all, you eliminate arithmetic errors, and if a number changes later, you only need to update the formula. Once you have finished entering the original numbers, it is also useful to ask AI one more question: "Pick out any numbers in this table that do not appear to be supported by the material." This gives you a second set of eyes on flaws the person who made the table may have missed.

## Limitations of This Prompt

An attached source does not mean a number has been verified. AI can invent sources that sound plausible. It may write "Quoted from the 2024 annual report" even though no such sentence exists. That is why the prompt asks for the exact source sentence, but the final check still requires a person to open the original document and compare it.

Without web search, AI still cannot provide the latest figures. For outside figures such as prices, market size, or adoption rates, if you need a value from a period not in the AI's memory, use a tool that can search the web or find the original source yourself. Even when you instruct AI to cite search results, do not skip checking that the URL opens and that the cited document actually contains the number.

Finally, verification requires judgment. When two sources disagree, deciding which one to use depends on your organization's standards. Whether to follow the newest source or the official statistics is not something AI should decide. Your team should set that rule and record it in a note under the table. Think of it this way: the person who puts a number in the table also takes responsibility for that number.
