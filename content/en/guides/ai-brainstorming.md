---
title: "Why \"give me ideas\" fails with AI brainstorming"
description: "\"Give me some ideas\" is a prompt for the most predictable answers. This practical brainstorming prompt uses constraints to push past the obvious, then adds a checklist to test what comes back."
created: 2026-09-15
updated: 2026-09-15
cssclass: blog-post
publish: true
lang: en
section: PROMPTS
tags:
  - prompt
  - brainstorming
  - practical
---

<img class="ewa-article-art" src="/static/img/art-ai-brainstorming.jpg" alt="Desktop robot illustration arranging idea cards inside a metal template frame and lifting one newly recombined card" width="900" height="900" loading="lazy">

## Why "give me ideas" fails

The day before a quarterly strategy meeting, you type this into AI: "Give me ten ideas for new features for our service." A neat list comes back in seconds: an AI chatbot for customer support, personalized recommendations, a subscription membership, a community feature. It looks plausible. But take it into the meeting and the responses are predictable. "We tried a chatbot last year and dropped it." "Our competitor already does recommendations." You have spent meeting time on a list you could have produced in ten minutes without AI.

The failure is not because AI is being unhelpful; it is because the question is too broad. The broader the question, the more AI chooses the average answer. Statistically, the combinations most often attached to "new feature ideas" are chatbots, recommendations, and subscriptions, so AI gives those back. Brainstorming needs not a broad question but a narrow, precise constraint. Good ideas do not come from "anything goes"; they come from "within these conditions."

## A prompt that works

Copy the prompt below and replace the bracketed parts with your actual situation.

```
Brainstorm within the conditions below.

Situation:
- Goal: [e.g., a marketing campaign to bring back users who churned]
- Audience: [e.g., office workers in their 30s who tried it once and churned within two weeks]
- Resources: [e.g., a ₩5 million budget, two people, four weeks]
- Do not use: [e.g., discount coupons, increased ad spend, new feature development]

Process:
1. First, list five common ideas that always come up for this kind of problem. Exclude all of them from the ideas in this round.
2. Generate 10 ideas that follow the constraints. For each one, include:
   - The idea in one line
   - Working hypothesis (why it seems likely to work for this audience)
   - Test method (the cheapest experiment that could prove it wrong within a week)
3. End with a self-review: if there are recurring patterns across the ideas, what are they, and which idea is the riskiest?
```

This prompt differs from "give me ideas" in three ways.

First, it **rules out the obvious answers up front**. AI gives obvious answers because they are the highest-probability answers. If you make it open that drawer first and then lock it, AI starts looking in the second drawer. The key is having AI create the exclusion list itself. If you bring in a list of forbidden ideas from outside, it may not fit the realities of your industry.

Second, it **turns constraints into ingredients**. Budget, headcount, schedule, and exclusions do not just narrow the idea space; they change the ingredients. The conditions "₩5 million, two people, four weeks, no coupons" demand something other than coupons or ads, and that pressure produces ideas. Brainstorming without constraints produces ideas that assume unlimited budget—ideas that end with "We could do it if we had the money" in the meeting.

Third, it **attaches a hypothesis and an experiment to each idea**. An idea's substance is not the sentence but the hypothesis. A list without "why it seems likely to work" and "how we could try to fail within a week" will be rejected again in the meeting. Those two lines make the ideas discussable.

## Review checklist

Do not use the list AI returns as meeting material without checking it. Take three minutes.

- [ ] Has each idea actually respected the budget, people, and time constraints?
- [ ] Does the working hypothesis talk about our audience? (If it is generic, it will not hold.)
- [ ] Are the five common ideas actually the common answers for this problem? (If not, the exclusion step failed.)
- [ ] Is the test method genuinely possible within a week? Does the experiment fit within the budget?
- [ ] How many genuinely different directions are there among the 10?

The last item is often deceptive. AI packages one pattern in ten variations. If the pattern "attract people through content" appears as YouTube, a newsletter, an infographic, and a blog partnership, it looks like four ideas but it is one direction. Counting directions is the human's job. If there are three or fewer, change the constraints and run it again.

## Application: Forced combinations

If ideas stall, break through with combinations. Give AI two assets you already have, and make it connect them only indirectly.

```
Our existing assets:
- [e.g., 8,000 subscribers to an email newsletter for office workers]
- [e.g., 40 work templates]

Generate seven ideas that emerge where these two assets meet.
However, exclude direct combinations such as "introduce the templates in the newsletter."
The more indirect the connection between the assets, the better.
For each idea, explain the connecting link in one line.
```

Anyone can think of a direct combination. Indirect combinations produce a third thing. An idea like "Survey subscribers about how they use the templates, then turn the results into an industry-specific report and use it as promotional material" is not a direct combination; it is a connection with one bend in it. In this prompt, a person must prepare the asset list. AI does not know what we have, and it will not ask.

## The limits of this prompt

AI does not know what our customers look like. No matter how precisely you state the constraints, the basis for deciding "our customers will not buy this" comes from field experience, and that belongs to people. So divide the work: AI expands the options; people choose.

Another issue is that many ideas that look fresh are recombinations. AI's output is a combination of what it learned, so even when something looks new to you, it may have been tried somewhere else. This prompt does not cover the step of searching to see whether competitors or others in the industry have already tried it. Do that search yourself or use a separate tool that can search.

Finally, half of brainstorming is convergence. AI makes divergence cheap, but choosing one option and taking responsibility for it remains your job. As divergence gets cheaper, your selection criteria must not become fuzzier. Before asking for ideas, decide what an idea must satisfy to be adopted this time. That is worth more than ten ideas.
