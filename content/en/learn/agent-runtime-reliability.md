---
title: "The Real Reason Agents Keep Failing — 5 Runtime Reliability Criteria"
description: "Why agents stall in real work even with high benchmark scores. 5 practical criteria to verify: latency budgets, tool call costs, permission boundaries, state recovery, and execution environment."
created: 2026-07-27
updated: 2026-07-27
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - ai-agent
  - runtime-reliability
  - practical
---

<img class="ewa-article-art" src="/static/img/art-agent-reliability.jpg" alt="Illustration of a robot pausing on a tipped stepping stone while a worker watches ready to intervene" width="900" height="720" loading="lazy">

## "Can't I Just Switch to a Smarter Model?"

When an agent causes problems in production, the first thing most teams do is switch the model. From GPT-4o to Claude, from Claude to Gemini. They refine prompts, lower temperature to 0, add few-shot examples. Eight out of ten of these attempts fail. Because the root cause isn't the model's intelligence — it's the **execution architecture**.

Even with a model that scores high on benchmarks, the agent still stops mid-process, tool calls fail, and costs spiral out of control. A smarter model means "it gives better answers in a given environment" — not "it solves problems with the environment itself."

Here are 5 criteria for judging runtime reliability — making sure an agent doesn't just work once, but keeps working.

## 1. Latency Budget

How long does it take for an agent to complete a single task? A simple question, but most teams don't measure this.

When an agent needs 5 steps, each step consists of model inference (3–15 seconds) plus tool calls (1–30 seconds). Five steps means at minimum 20 seconds, at maximum 200 seconds. If this exceeds what users are willing to wait, they'll either give up mid-process or handle it manually.

In practice, what you need to check isn't the average but the **worst case**. If P99 latency (the slowest response that occurs roughly 1 in 100 times) is 5 minutes, that single instance stops the entire workflow. Set a latency budget and design the agent to show intermediate results to the user when it exceeds that budget.

## 2. Tool Call Cost

Every time an agent calls a tool, there's a cost. API call fees, database query costs, compute costs. If an agent calls a tool 10 times for a single task, that cost is multiplied by 10.

The problem is when agents "repeatedly call the same tool." It receives search results, doesn't understand them, and searches again. And again. You hit API call limits or costs blow past expectations.

In practice, you need to set upper limits on tool call counts. A rule like "maximum 3 calls to the same tool per task." When the limit is exceeded, the agent stops and notifies a person. An agent with uncontrolled costs is unusable.

## 3. Permission Boundary

What can the agent do, and what can't it do? When this boundary isn't clear, the agent takes dangerous actions "trying to be helpful."

Give write access where only read access is needed, and the agent modifies data. Give external API access where only internal data should be visible, and the agent sends data to external services. Actions taken "to be helpful" become security incidents.

In practice, permissions should follow the **principle of least privilege**. Give the agent only the permissions needed for the current task, and revoke them when the task is done. Especially for actions like file deletion, email sending, and payments — prevent the agent from doing these directly and insert a human approval step.

## 4. State Recovery

If an agent fails at step 3 of a 5-step task, what happens?

Good design: Preserve results from steps 1–2 and restart from step 3.
Bad design: Start from scratch. Steps 1–2 run again, doubling the cost.

When an agent fails mid-process, it needs to remember how far it got and be able to resume from there. This is called "state recovery." An agent without state recovery restarts from the beginning every time it fails — and that's unusable in production.

## 5. Execution Environment

When an agent needs to execute code, where does that code run? If it runs in a sandbox (an isolated environment), it's safe. If it runs on the user's actual machine, the agent can touch system files.

In practice, code executed by agents should be isolated in a sandbox, file system access should be restricted, and network access should be managed via a whitelist. "We don't know what the agent will execute, so let's allow everything" is a recipe for incidents.

## Practical Application: What to Check First

When adopting or evaluating an agent, verify these 5 things in order.

1. **Latency budget**: How long does a single task take to complete? (Measure)
2. **Cost**: How many tool calls does a single task make? (Measure)
3. **Permissions**: What is the scope of what the agent can do? (Document)
4. **Recovery**: When it fails, where does it restart from? (Test)
5. **Environment**: Where does the code execute? (Verify)

If the answer to any of these is "I don't know," solve that first. Switching to a smarter model comes after.

---

*This article is followed by a more technically in-depth [Deep Dive into Agent Runtime Reliability](/wiki/concepts/agent-runtime-reliability).*
