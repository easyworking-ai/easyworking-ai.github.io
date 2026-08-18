---
title: "A prompt that finishes competitor analysis in 30 minutes"
description: "\"Analyze my competitors\" makes AI fill tables with outdated information. A prompt that splits the work — you search, AI structures — plus a checklist for catching fabricated data."
created: 2026-08-18
updated: 2026-08-18
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompts
  - competitive-analysis
  - practice
---

<img class="ewa-article-art" src="/static/img/art-competitor-analysis.jpg" alt="An illustration of a worker evaluating competitor cards pinned on a board, pointing at one" width="900" height="900" loading="lazy">

## Why "analyze my competitors" fails

Before a planning meeting or a proposal, you need a competitor analysis. So you type "analyze companies A, B, and C" into an AI. It returns a plausible comparison table — pricing, features, market position, all neatly organized. The problem starts when you walk into the meeting with that table.

The prices AI knows are the prices from its training data. Products launched last year are missing, and discontinued features still show up as alive. Worse are the items that never existed. When AI gets a task called "competitor analysis," it tries to fill every empty cell in the table. Unknown items get filled with whatever is common in the industry. The table looks perfect, so you can't tell it's wrong until you check the numbers one by one.

Competitor analysis fails at the input, not the analysis. AI doesn't have current information — so you do the searching, and let AI structure what you found. The 30 minutes split like this: 15 minutes gathering sources, 5 minutes structuring with the prompt, 10 minutes reviewing. There's no fully automated analysis, but this gets you a comparison table you can actually use in a meeting.

## The prompt that works

Copy text from the competitors' pricing pages, press releases, and announcement pages. Three companies' worth fits in 15 minutes. Don't copy the slogans on their homepages — marketing copy doesn't become table material. Collect only verifiable things: prices, feature lists, dated announcements. Then send them with this prompt.

```
Below is text copied from the websites and press releases of three competitors.
Build a comparison table using only the information in this material.

Comparison axes (columns: Competitor A/B/C):
- Pricing: starting price and what it includes
- Core features: only what the material explicitly states
- Customer support: channels and hours
- Recent moves: only items with dates

Conditions:
- Mark items not found in the material as "not in material." Do not fill them with your own knowledge.
- Include the date with every recent-moves item.
- If the sources contradict each other, list those conflicts separately under the table.

Material:
"""
[Competitor A pricing page text]
[Competitor A's 3 most recent announcements]
[Competitor B pricing page text]
[Competitor B press release]
[Competitor C product page feature list]
"""
```

Three things make this different from "analyze my competitors."

First, **the source of truth is the pasted material, not AI's memory**. AI doesn't know about pricing changes or launches that happened after its training cutoff. Instead of asking what it doesn't know, you hand it verified material and restrict the work to that. The 15 minutes of searching is half the value of this prompt.

Second, **the comparison axes are specified**. Without axes, AI compares the companies using phrases lifted from their marketing copy. A table that puts "innovative platform" next to "all-in-one solution" doesn't help you make any decision. When you define the axes yourself, the table comes out shaped like the questions you'll actually have to answer in the meeting.

Third, **"not in material" is allowed**. AI doesn't leave blanks on its own. Permitting it to say "I don't know" makes fabrication visible. A lot of "not in material" entries is itself information — those are the items that need more research, and they move to a "to verify" list under the table.

## Review checklist

Never take AI's table straight into a meeting. Five minutes of checking, in checklist order: compare the table's numbers against the sources → check where "not in material" sits → check whether the axes match your meeting questions → check the dates. The order is arranged from highest catch probability first.

- [ ] Did you check every price and number in the table against the original material?
- [ ] Are the "not in material" entries still there? (Did AI quietly fill them in?)
- [ ] Are the comparison axes the items you'll actually be asked about in the meeting?
- [ ] Does every recent-moves item carry a date?
- [ ] Did you add a row for your own product on the same axes?

The first item is the one people skip most. When the table looks clean, it earns unearned trust. AI sometimes merges or rounds numbers while transferring them. If one number is wrong in the meeting, you end up re-checking the entire table on the spot.

## Extension: turn it into a one-page sales guide

It's a waste to stop at an internal report. Convert the comparison table into something the sales team can use in the field.

```
Turn the comparison table below into a one-page guide for the sales team.

Include:
- One line per competitor: "where we win"
- The 3 questions customers ask most, with suggested answers
- Where we lose, and the direction for answering those moments

Conditions:
- Use only facts from the table. Do not invent support we don't have.
- Write in the language a salesperson actually uses in the field.

Comparison table:
"""
[paste the comparison table from earlier]
"""
```

This extension isn't organizing facts — it's building a frame from your product's point of view. If "where we win" gets exaggerated, the field loses trust in it. Run it past the sales team before distributing. Keep feeding customer reactions from the field into the table's "recent moves" section, and the guide refreshes itself every quarter.

## The limits of this prompt

A human still gathers the material — and decides what to look at. Competitors' private numbers — revenue, customer counts, contract terms — don't come out of any prompt. When you need those, check public filings or industry reports separately. If AI offers an "estimate," throw it out rather than use it. Unless the basis of an estimate is public, you have no way to rebut it.

Competitor websites are marketing documents, and that's another limit. Claims like "industry-leading" or "chosen by 100,000 customers" are usually unverified assertions, but AI transfers them into the table as facts. Separating verifiable figures (public prices, dated announcements) from unverifiable claims is ultimately a human eye's job — don't delegate it. AI has no basis for judging whether a claim is true.

Finally, a comparison table is a snapshot of one point in time. Pricing changes every quarter. Write the date on the table, and rebuild it after three months. Walking into a customer meeting with a stale table is the most common accident in competitor analysis.
