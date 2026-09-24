---
title: "Where Agent Adoption Breaks Down: Five Anti-Patterns from Real Failure Cases"
description: "Most failed agent rollouts are caused not by the technology, but by how the work is delegated. Here are five anti-patterns repeated by teams that returned to manual work within two months."
created: 2026-09-24
updated: 2026-09-24
cssclass: blog-post
publish: true
lang: en
section: AGENTS
tags:
  - ai-agent
  - 도입
  - 실패
---

<img class="ewa-article-art" src="/static/img/art-agent-failure-cases.jpg" alt="An illustration of a desktop robot staring in dismay at a collapsing tower of documents" width="900" height="600" loading="lazy">

## "It worked well—so why did you stop?"

A team introduced an agent early last year, then went back to doing the work manually within a few months. They started with organizing meeting notes, then assigned it customer inquiry responses and weekly reports. It seemed to run well for about two months. But reviewing the outputs began to take longer than doing the original work, and at some point the team took the work back.

Look at a few teams like this and an odd common thread appears. The reasons for failure seem different, but the point where things break down is usually the same. It was not a lack of technology. The problem was how the work was assigned.

Recurring patterns of failure are called anti-patterns. Here are five anti-patterns that frequently appear when teams introduce agents, organized as case studies.

## Five Failure Cases

### Case 1: They assigned work with no defined standard

"Just reply to incoming inquiries on your own"—that was how it started. The problem was that there was no definition of a correct answer for the task. Even for the same inquiry, the tone varied by person, and the team decided case by case how much to answer and when to bring in the person responsible. Humans had to make that judgment every time, too.

When there is no standard, an agent creates its own. That standard is not the company's; it is an average standard drawn from its training data. The result was not a "wrong answer" so much as an "answer that did not sound like our company," and the only option was for a person to fix each one.

Before assigning this work to an agent, the team needed to define the response tone in writing and put the escalation conditions into a table. Work that has not been organized this way is not ready to be handled by an agent.

### Case 2: They removed the approval step

They designed the agent to send customer emails immediately instead of preparing drafts. The human review step was removed because it was considered something that would "slow things down."

Nothing went wrong for three weeks. Just as that clean run was turning into confidence, 40 emails went out with the wrong company name because the agent used a template whose customer name had changed. The messages could not be recalled.

What broke down here was not quality but recoverability. Sending an email, making a payment, or writing a record to an external system cannot be undone once it has happened. Even if 99 runs go well, the cost of the 100th failure can exceed the gains from the first 99. Put a human approval step in front of irreversible actions. That is not sacrificing speed; it is buying insurance.

### Case 3: They kept no logs

This was weekly report automation: an agent that gathered data every Monday, built a table, and shared it. After about two months, the customer was the first to notice that the numbers looked wrong. When the team traced the problem back, the aggregation criteria had been off for at least three weeks.

Agents fail quietly. They do not always raise an error; they produce results that look plausible. The table does not break, and the writing remains smooth. Unless someone deliberately checks, the mistakes keep accumulating.

The operation that survived was simple. They kept an execution record of what the agent read and calculated, and set aside 15 minutes each week for a person to open and review the results. Automation without observation is like a broken clock. If it has stopped, you notice quickly. If it keeps running while showing the wrong time, you find out late.

### Case 4: They gave it every permission

The reason was convenience: designing the permissions was a hassle. Reading the mailbox was enough to classify inquiries, but they also gave the agent write access and database access "so it could do other things later."

If nothing goes wrong, that is the end of the story. But an agent that has quietly drifted off course, as in Case 3, will carry out incorrect actions within the permissions it has. Incorrect classification results get written to the database, and other automations act on those records. The scope of the damage becomes the scope of the permissions.

Grant only what is necessary, and separate read access from write access. Permissions granted in advance for later use do not make the future safer; they become the source of a future incident.

### Case 5: They rushed to expand after the first success

Meeting-note organization worked well. The following week they added report drafting, and the week after that they added data lookup and email sending. Within two months, the workflow had grown to five stages.

Even if each stage has a 95% chance of success, the chance that all five stages succeed is 77%. If the workflow runs 20 times a month, something will go wrong somewhere about five times. Finding the point of failure means checking all five stages, so the review burden actually increases.

Expand one stage at a time. Whenever a new stage is added, set aside time to confirm that the earlier stages are still working as before.

## Failed Adoption vs. Adoption That Survived

The same work can produce different results depending on how it is assigned. The difference was not the tool but the design.

The teams that failed delegated the entire process from the start. They ran it without approval. They operated without records. They granted generous permissions. They expanded as soon as they saw success.

The teams that survived started with a single task. They put human approval before irreversible actions. They kept execution records and reviewed them every week. They started with the minimum read permissions. They expanded one stage at a time.

| Anti-pattern | What it looks like at first | When it breaks down | Prevention |
|---|---|---|---|
| Delegating work without criteria | "It seems to handle it well on its own." | Results that do not sound like our company pile up | Turn human judgment criteria into rules first |
| Removing the approval step | Things get faster | An irreversible execution incident | Send, pay, or write records only after human approval |
| Operating without logs | It runs quietly and smoothly | Wrong results are discovered after they pile up | Execution logs + a 15-minute weekly review |
| Excessive permissions | Setup is convenient | The damage from a malfunction grows as far as the permissions allow | Separate read and write access; grant least privilege |
| Expanding too quickly | It is easy to report early wins | More stages make review take longer | One stage at a time; recheck the previous stages |

## What to Check Before Adoption

It comes down to five questions.

1. Can you write down the standard for a correct answer for this task? If not, it is not ready yet.
2. Can you recover when the agent is wrong? If not, add an approval step.
3. How will you know that it is wrong? Without logs and a review cadence, you will not know.
4. Are the permissions minimal? Do not give write access to a task that only needs read access.
5. Did you verify the previous stage before expanding to the next one? If not, run the current stage for longer.

One limitation is worth making clear. Even if a rollout passes all five questions, failures will still happen. An agent is a probabilistic system, so failure cannot be reduced to zero. The goal is not to make failure impossible; it is to notice failures quickly and make them reversible. With those two safeguards in place, the team does not end up going back to doing everything manually.