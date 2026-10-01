# Research the course route

Search for the material needed to build each step of the course. Do not copy
one syllabus or assign one book to every topic. A source can help with the
order of ideas, the first explanation of one concept, a precise derivation,
or an exercise. Say which job it does.

## Match the source to the step

For each topic, name the action the learner should be able to perform, the
subfield that judges it, and the knowledge needed before it. Implementing a
solver, justifying its convergence, and interpreting its output may need different
source sections even when all three concern the same method.

Open the candidate section and inspect its explanation, notation, assumptions,
and worked example. Check the reasoning between steps, not just the final
answer. If it starts with unfamiliar terms or methods, find an earlier
explanation or give that prerequisite its own topic. Check that the learner
can access the relevant material; a readable introduction does not establish
that the needed chapter is available.

Use a technical chapter or paper when its exact method, evidence, or limits
matter. A course that ends at a research method may use a paper near the end
without teaching the opening concepts from that paper. Explain the paper's
terms before asking the learner to read its derivation.

The course depth changes how far you check an idea, not how hard the first
source must be:

| Depth | Check while planning |
| --- | --- |
| `survey` | Find a sound first explanation, a concrete case, and the connection between the central ideas. |
| `working` | Also inspect worked reasoning and an exercise that changes a meaningful condition, so independent use requires more than copying steps. |
| `mastery` | Also inspect the justification, assumptions, limits, and a case that challenges the method or interpretation. |

Choose the few sources that do these jobs well. Add another only when it
answers a question the existing sources leave open. A short course should
cover fewer steps fully; a longer course can give difficult steps their own
topics. Do not use a source count as a proxy for depth.

## Check what the sources let you teach

Choose material that supports a connected explanation: a concrete case, the
reasoning that explains it, and a useful way to inspect the same idea. Check
how the source connects its prose, equations, diagrams, data, or code. Lesson
design can supply a missing view, but must check that it preserves the same
quantities, assumptions, or evidence. A polished figure with no explanation
of its labels is insufficient on its own.

Inspect a changed case before planning practice. Find what stays the same,
what changes, and why the original reasoning still works or needs revision.
An exercise can supply this case, or lesson design can develop one from the
checked material. Do not claim that the source contains an example you created.

For example:

- For a quantitative topic, choose a worked case that connects quantities to
  an equation and graph, then check what happens when one assumption changes.
  A derivation may supply the justification that the introductory case omits.
- For a history topic, use scholarship to explain the question and context,
  and a dated document for the claim it can support. Compare another account
  or change the proposed interpretation and ask which evidence still holds.
- For programming, use documentation for the actual interface and version,
  and inspect a small trace that explains state changes. Change the input or
  boundary case to check the behavior; add a tutorial only if it supplies
  reasoning the documentation leaves implicit.

These are source jobs, not required source types for every topic. One source
may do several jobs well; several sources may be needed for one hard step.

## Search and verify

Start with books, open course pages, official documentation, primary records,
and papers suited to the subject. `skills/subject/references/resources.json`
is a list of leads, not a preselected bibliography. An original work establishes
what its authors claimed or observed; an accessible textbook or course may
explain the prerequisite reasoning better. Use each for its actual contribution.
For changing software, check the installed version against its documentation.
For a research claim, open the original work and inspect the relevant method,
result, and limitations.

Record the actual section you read, what it establishes, and its audience.
A landing page may confirm a title but not a chapter's teaching content. A
search snippet is a lead, not proof. If a page is inaccessible, mark it that
way and use a source you can inspect.

For a video, inspect the exact segment and its prerequisites through the
owning media skill. A title match does not establish coverage. For a reused
figure or dataset, retain its source, labels, units, context, and permitted
use. Distinguish observed data from illustrative values and model output.
Keep an accessible explanation available when a useful source requires an
account, paid access, or a player the learner cannot use.

## Save the useful notes

Keep `RESEARCH.md` beside `course.json`. Record decisions and remaining gaps,
not the search history. A small table is enough:

| Topic or concept | Source and section | Job in the course | What you checked | Gap |
| --- | --- | --- | --- | --- |
| First encounter with probability | Introductory chapter, named section | Explain chance through a small case | Read the example and its prerequisites | Conditional cases come later |

Use `course-research.json` when structured notes help. Keep `used_in` tied to
topic IDs and state what the source contributes. For example:

```json
{
  "goal": "compare uncertain outcomes",
  "sources": [
    {
      "id": "openstax-expected-value",
      "title": "OpenStax Introductory Statistics 2e",
      "url": "https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation",
      "opened_sections": ["4.2 Mean or Expected Value and Standard Deviation"],
      "role": "Introduce a probability-weighted average through a small table",
      "trust": "opened",
      "used_in": ["expected-return"]
    }
  ],
  "open_questions": ["Learner's fluency with probability is unverified"]
}
```

The `id` must match `course.json/sources`. Only sources used by the route
belong in that course record. Its topic `resource_ids` select the sources for
that topic. Give each recorded source its real section and verification note.
In `course.json`, use the source fields in [course-contract.md](course-contract.md):
`title`, `type`, `checked_on`, `sections`, `verification_notes`, and exactly one
of `url` or `local_path`. The research notes above supplement that record;
they do not add fields to the course source schema.
Do not describe unopened material as checked.
