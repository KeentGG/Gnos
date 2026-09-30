---
name: jsxgraph
description: Build and inspect mathematical graphs and coordinate constructions with JSXGraph when a learner needs to connect an equation to a shape, solve graphically, or test a quantitative change. Use other diagram tools for concept maps, network layouts, and geographic maps.
---

# JSXGraph

Use this skill after lesson design has selected a mathematical graph through
[representation choices](../lesson-design/references/representation-choices.md).
It builds the graph; the subject teacher still owns the model and explanation.
JSXGraph runs in the browser. It needs no MCP server, account, or learner setup.

## Establish what the graph teaches

Read the selected subject guidance and the block brief. Identify the difficult
step that a graph will expose. A learner might connect a derivative to a tangent,
find an intersection, compare feasible choices, or explain a parameter change.
Write that action into the brief before choosing controls.

Keep the lesson's example, variables, units, and assumptions. Show how each
important equation term corresponds to an object or value in the graph.
If the learner has not met the axes or the quantities, introduce them in the
surrounding explanation. Work through one result before asking the learner
to investigate a new case.

Use a fixed view when comparing its parts is sufficient. Add a draggable point,
slider, or step button only when changing it answers the lesson's question.
For graph reading, ask the learner to explain a slope, area, scale, or domain.
For graphical problem solving, connect the estimated solution to a calculation
and state its precision. A picture can suggest a result; it does not prove it.

## Build the artifact

Read [authoring](references/authoring.md) for the starter examples, export command,
and checks specific to mathematical plots. Follow
[simulation presentation](../lesson-design/references/simulation-design.md)
for the palette, layout, responsive views, and embedded inspection. Those rules
remain shared with other HTML experiments.

Start from the example closest to the teaching action and adapt its ordinary
JavaScript. Use the pinned local runtime through `scripts/build_graph.py`.
Keep the numerical calculation available in the source. JSXGraph draws the
model; it does not establish a physical law, causal claim, or numerical method.
Use the host's available browser and file tools to build and inspect the result.
Do not add a research service or require an MCP for this workflow.

## Hand it back to lesson design

Return the checked HTML, its title and purpose, model assumptions, and the
actual iframe dimensions. Use `interactive-graph` for a mathematical view
and `simulation` for an experiment whose state evolves. Both register as a
`simulation` artifact with MIME type `text/html`. Declare
`skills/jsxgraph/SKILL.md` in the lesson's `skill_routes` and in the block's
`production.skill_route`. Existing binding representation plans still apply.

The coordinator follows the existing
[artifact registry](../course-design/references/artifact-manifest.md) to publish
the result. Keep prompts for learner predictions and explanations in the
existing exercise blocks.
Moving a control is exploration, not independent success. Do not claim that
responses inside an HTML graph have been saved or graded by the course viewer.
If the export or embedded checks fail, return the concrete failure and keep
the artifact in draft until it is repaired.
