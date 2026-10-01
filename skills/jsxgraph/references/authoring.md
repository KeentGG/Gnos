# Authoring a mathematical graph

Choose a starter by what the learner will inspect. The derivative example
connects a draggable point, tangent, and slope readout. The gradient-descent
example steps an update and compares learning rates. The supply-and-demand
example changes a condition while preserving the earlier curve for comparison.
Their formulas and values are teaching examples, not measured data.

Build a starter from the repository root:

```bash
python3 skills/jsxgraph/scripts/build_graph.py --example derivative --palette forest --output output/derivative.html
```

The other example names are `gradient-descent` and `supply-demand`. To change
the model, copy a scene from `examples/`, edit it, and pass its path:

```bash
python3 skills/jsxgraph/scripts/build_graph.py --scene output/my-graph.js --palette luxe --output output/my-graph.html
```

The builder combines the scene, graph shell, bundled JSXGraph 1.13.3 runtime,
license notices, and existing simulation styles and view switching into one
HTML file. No package installation or network access is required to build or
view it. Place a checked course artifact inside that course's `artifacts/`
directory before registration.

## Adapt the scene

`GNOSGraph.create()` sets the title, question, model notes, initial state,
numeric controls, axis descriptions, and bounding box. It returns `board`,
`state`, and palette `colors`. Build objects with the ordinary JSXGraph
`board.create()` API. `bind(render)` connects controls to the calculation;
`set(key, value)` changes a controlled value; `readout(text)` updates the
visible result. The supplied reset restores the initial state and calls
the same render function. Add a custom reset callback through `onReset`
when the scene also keeps a trajectory or other history.

Each scene ends by exposing its UI as `window.graph` for browser inspection.
This is a development aid, not a learner record. Replace every example title,
question, model note, axis description, and concluding task when adapting it.
Use the [current JSXGraph documentation](https://jsxgraph.org/docs/) through
the host's available tools when the scene needs another element or operation.

The shell reads colors from the existing approved palette. Use `colors.primary`
and `colors.secondary` for distinct quantities and `colors.ink` for labels.
Give compared curves different line styles as well as colors. Override
JSXGraph's default colors on each authored element so an unapproved highlight
does not appear during dragging or focus. The starter helper supplies these
attributes through `curveStyle()` and `pointStyle()`.
For compared curves, call `legend([[label, curve], ...])` after creating them.
It names each quantity and copies the curve's color and line pattern.

## Preserve the mathematical meaning

Choose the domain and viewport from the question. Check the values at useful
points, roots, intersections, and boundaries against calculations independent
of the drawing. Split curves across excluded inputs or asymptotes; never draw
a connecting segment across an undefined region. Show clipping or provide a
readout when an important result leaves the viewport.

Label both axes with the actual quantities and units. In economics, a relation
written as quantity in terms of price may need rearranging when price belongs
on the vertical axis. Keep probability density distinct from probability.
In motion plots, distinguish position, slope, and area and preserve the clock
and units across views. In optimization, show the actual update and state which
objective and assumptions the example uses.

Preserve the scale when comparing states. If an automatic scale change is
necessary, make it visible and explain why apparent slope or distance changed.
Use equal coordinate scales when angles, circles, or lengths carry meaning.
Start with 2D when it exposes the question; use 3D only when the learner needs
the extra dimension and can inspect it without occlusion.

Keep one state for the calculation, plotted objects, and numeric readouts.
Changing a parameter should recompute every dependent view. For an iterative
model, state whether the change restarts the experiment or applies to the next
step. Document the method and check an analytic or limiting case. Smooth
rendering does not validate the underlying computation.

## Inspect what the learner receives

Follow the responsive and sandbox checks in the shared presentation guide.
Also compare a known value and a meaningful changed case with the readout and
the actual plotted coordinates. Check the minimum and maximum of each control,
dragging where supplied, keyboard input, view switching, and reset. Confirm
that the axes and labels remain readable after resizing or revealing a hidden
board. Verify that the exported file makes no external requests.

Save screenshots of the initial and changed states in the actual course iframe,
including a narrow screen. Inspect the images for clipped labels, misleading
scales, overlaps, and differences from the lesson's notation. Exercise the
controls as well; screenshots alone cannot establish that the graph works.
The checked examples in `tests/test_jsxgraph_browser.py` demonstrate this
inspection using the existing course renderer and Playwright.
