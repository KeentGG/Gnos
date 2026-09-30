# Simulation presentation

Use this guide for self-contained HTML and exported widgets. The simulation
serves one question in the lesson. Keep long explanations in adjacent blocks.

## Fit the experiment

Design for a 1280 × 800 frame and inspect the actual viewer at 1200, 768, 390,
and 320 pixels wide. The simulation must fit its frame without horizontal or
vertical scrolling. Keep every active control, label, and result visible.
Do not hide overflow to conceal clipped content or shrink text until it fits.

At desktop width, place controls beside the visual result. At narrow widths,
use a clear Controls / Result / Model switch when both cannot fit comfortably.
Keep state when switching views. A learner must be able to change an input,
inspect its consequence, and return without losing the experiment.

Use [the reusable shell](../templates/simulation.html) as a starting point.
Its panes separate the experiment from model notes and keep the embed fixed
to the frame. Inline its CSS and script when exporting; the artifact must not
depend on a repository path or a running editor. Adapt the panes to the task.

## Keep the visual language quiet

Choose one of these approved palettes for an artifact. Keep its colors together;
do not mix palettes or introduce extra colors. Use the same palette in related
lesson visuals. Avoid yellow highlights; the yellow-toned swatches need not be
used. Use solid fills, thin borders, generous spacing, and 2–4 pixel radii.

| Preset | Approved colors |
| --- | --- |
| `luxe` | `#322D29`, `#72383D`, `#AC9C8D`, `#D1C7BD`, `#D9D9D9`, `#EFE9E1` |
| `wine` | `#EDE7C7`, `#8B0000`, `#5B0202`, `#200E01` |
| `forest` | `#445D48`, `#FDE5D4`, `#D6CC99`, `#001524`, `#5E3023` |
| `blue` | `#0274BD`, `#E9E6DD`, `#C4AD9D`, `#000000`, `#F57251` |

Set `data-palette` on the template's root element. Use `luxe` for neutral
cream and burgundy or `forest` for green, pale peach, and dark navy. The blue
and wine presets are alternatives for a whole artifact. Do not assign a
palette by subject or treat red and green alone as proof of a state.

Use serif or plain sans-serif for headings and explanations. Use local
monospace fonts for smaller labels, units, model notes, and numeric readouts.
Do not require a font download. Keep headings restrained and avoid stacked
cards, gradients, glows, or decorative shadows. These rules apply on Claude,
Codex, and other hosts.

Give color a stable meaning across the lesson. Label important differences in
words or line styles too. Keep ordinary text at least 14 pixels and controls
at least 44 pixels high. Use tabular numbers for changing values; give the
question, controls, visual result, and explanation a clear reading order.

## Make changes legible

State the question before the controls. Label each input with its quantity and
unit; place its current value beside it. A reset returns to the stated initial
conditions. Motion needs pause or step controls. Honor reduced-motion settings.

Compute all linked views from the same state. Explain which visual object
matches each equation term, code operation, or table entry. Keep a short
interpretation beside the result, and return to the lesson's running example
in the following block. A changed assumption must be named before its result.

## Check the embedded artifact

Open the exported file inside `sandbox="allow-scripts"`, as the viewer does.
Test minimum, middle, and maximum inputs; step, pause, reset, and every view
switch. Use keyboard controls as well as the pointer. Confirm that a switch
preserves state and that reset restores all views together.

Measure both document and pane overflow at each test size and after the
longest feedback or alarm appears. Inspect plot labels, contrast, spacing, and
the result with reduced motion. File presence or a screenshot of the editor
does not prove that the delivered simulation works.
