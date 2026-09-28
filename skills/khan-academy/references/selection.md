# Decide whether Khan fits this teaching step

Use the current lesson's concept, depth, learner evidence, and next action.
"Khan teaches calculus" is not evidence that a particular item teaches the
proof, interpretation, or technique this section needs.

## Make a coverage judgment

| Judgment | Evidence needed | Decision |
| --- | --- | --- |
| Direct section match | The actual explanation demonstrates the target relation or operation, at the needed level | Use that segment for the section; GNOS supplies setup, connections, application, and assessment |
| Prerequisite match only | The item teaches a narrower skill the current step depends on, but does not teach the target topic | Use only if that gap is blocking; label the bridge and return to the target |
| Partial or adjacent match | Some terms overlap but a key assumption, mechanism, proof, or application is absent | Name the limit; use only the useful part if the transition is short and clear |
| No useful match | Inspected content is too basic, too advanced, mismatched, duplicative, or costs more explanation than it saves | Choose another source or representation |
| Unverified | Search failed, only a title is available, the page is blocked, or identity cannot be confirmed | Do not infer that coverage is absent; try a bounded fallback or proceed without it |

For a candidate, answer these questions before adding it:

- **Concept:** Which specific relation or step does it explain? What does it
  leave out? A slope video does not explain differentiation merely because
  both concern change.
- **Level:** What prior knowledge does it assume? Does it meet this lesson's
  depth, or only supply intuition before the required derivation?
- **Content:** Can you point to the inspected passage or interval that does
  the job? Check narration and the visual, not just chapter names.
- **Continuity:** Can the learner map its variables, axes, units, colors, and
  examples to GNOS's case? Explain a small mismatch; reject a distracting one.
- **Use:** What will the learner do with its result immediately afterward?
  If the answer is only "watch the next video," reconsider the section.
- **Access and cost:** Is the useful part readable/listenable at this viewport
  and language, and does viewing plus the follow-up fit the lesson time?

Record this judgment briefly in the source's `verification_notes` and the
block's production brief. These are reasoned decisions, not a numeric score.

## Where to look, without assuming coverage

These are search directions, not a guaranteed catalog. Verify today's item.

| Lesson need | Search direction | Coverage boundary to inspect |
| --- | --- | --- |
| Algebra or calculus foundation | Specific operation, graph interpretation, derivative or integral example | Procedural example versus conceptual explanation versus proof |
| Probability or statistics | Conditional probability, expected value, sampling, inference | Assumptions, independence, population/sample distinction, mathematical depth |
| Introductory science | Specific mechanism, conservation law, molecular process, circuit relation | Idealized model versus real apparatus, quantitative conditions, current context |
| Economics | Marginal change, opportunity cost, supply/demand, elasticity | Model assumptions versus empirical or current policy claims |
| Computing | The exact algorithm, representation, or mathematical prerequisite | Conceptual account versus the learner's language, library, version, and runtime |
| History or humanities | A specific event, period, work, or interpretive concept | Survey explanation versus primary evidence and competing interpretations |
| Advanced or current research | A named foundational prerequisite | Do not treat a prerequisite match as coverage of the advanced topic |

For example, a chain-rule explanation may support one step of backpropagation.
It does not establish reverse-mode graph traversal, tensor shapes, framework
behavior, or implementation correctness. Keep those in the appropriate code,
diagram, derivation, or current primary documentation.

## Stop searching when the decision is clear

Start with the concept plus the needed operation. If a result lacks an exact
item path, retry with the GraphQL translatedTitle plus parentTopic, then check
the official page through websearch for its canonical URL.
Try a narrower term or prerequisite only when it has a teaching reason.
After a small purposeful search and one useful fallback, choose or move on.
Empty results mean unverified, never absent. They do not justify weakening the goal.

Do not start from a generic YouTube only hit and retrofit the GNOS course to it.
The course sequence and learner evidence determine which sources are useful.
Score each pair with the finder. Strong means 70 and above.
Below 70 stays unverified and never embeds.
