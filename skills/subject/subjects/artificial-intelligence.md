# Artificial intelligence

Choose the branch by the task and the claim about the system. Separate data,
objective, optimization, evaluation, and deployment. Check probability,
vector shapes, derivatives, or code only where they enter the explanation.
Keep training, validation, and test data separate. A generated example is not
an evaluation result; date benchmark claims and state their conditions.

## Ways to show the idea

Use [Excalidraw](../../excalidraw/SKILL.md) for data paths and boundaries,
[Manim](../../manim-voice-animation/SKILL.md) for narrated updates or state
changes, and [Pinepaper](../../pinepaper/SKILL.md) for linked diagrams.
Use [JSXGraph](../../jsxgraph/SKILL.md) to inspect distributions, decision
boundaries, and optimization steps. Use scientific plots for measured evaluation
results and uncertainty; use tables and code for
exact computations. Simulations should reveal the effect of a meaningful
choice, such as a threshold, policy, sample, or step size.

No AI teacher is assigned by default. CS supports implementation; math supports
the needed derivation; the application subject defines labels and acceptable
errors. Keep the AI explanation responsible for the model and its evidence.

## Teaching each area

Choose the matching section. Its order suggests how to build the topic; it is
not a complete syllabus. Course design uses the starting point and source
checks. Lesson design chooses the views that explain the difficult steps.
Treat the named confusion as a possibility, not a diagnosis of this learner.

### Search and planning

- **Build:** Use a small route graph with two competing paths and explicit
  edge costs. Follow available moves before naming the search method.
  Separate discovered, expanded, and finalized states; a promising heuristic
  alone does not guarantee the cheapest route.
- **Research:** Use an introductory search chapter with pseudocode and guarantee
  conditions. Check heuristic assumptions and what the cost measures.
- **Show and check:** Match node labels to frontier rows and separate path
  cost, heuristic estimate, and selection score. Trace one expansion beside
  the pseudocode; link the views if the learner steps through them. Change an
  edge cost or overestimate a heuristic and ask which decision or guarantee
  changes under the stated algorithm, including any reopening rule.

### Knowledge and reasoning

- **Build:** Use two facts and a rule, then one tempting conclusion the
  rule does not license. Separate validity from truth of premises and an
  implication from its converse. Specify whether a missing fact is unknown
  or treated as false.
- **Research:** Use a logic or knowledge-representation text with explicit semantics.
  Check whether the system treats missing facts as false or unknown.
- **Show and check:** Match each inference-tree leaf to a supplied fact
  and each edge to the stated rule. A truth table or countermodel explains
  why reversing the implication fails. Remove a premise or add conflicting
  evidence and ask what can still be concluded under the chosen semantics
  before checking a larger rule trace.

### Machine learning

- **Build:** Start with a relevant prediction task, a baseline, and one
  labeled mistake. Name the unit being predicted and how splits were formed
  before fitting. Training loss, held-out error, and the cost of a particular
  mistake answer different questions.
- **Research:** Use an accessible ML chapter for the first model and loss. Inspect
  dataset documentation and evaluation procedures before using performance claims.
- **Show and check:** Carry the same example ID from the data table to its
  plotted score, predicted label, and error-table cell. For classification,
  change the threshold and predict which false positives and false negatives
  move; for regression, connect a residual to its loss term. Change the
  sampling or split rule and ask whether the earlier evaluation still
  answers the task, rather than merely comparing training curves.

### Neural networks and optimization

- **Build:** Work one input through a small network to its loss before
  updating a parameter. Separate activations, parameters, gradients, and
  optimizer state. A gradient is local sensitivity, not the parameter's
  value or a guarantee that any step size improves the objective.
- **Research:** Use a deep-learning chapter for the operation and official framework
  documentation for implementation. Inspect tensor shapes and the assumptions behind the
  update.
- **Show and check:** Match tensor labels and shapes to the numeric forward
  pass, then follow one derivative backward through the same operations.
  Carry that derivative into the update table and its point on the loss
  trace. Change the input or step size and ask what changes before running
  code; compare held-out error separately from optimization progress.

### Language models and transformers

- **Build:** Tokenize a short sequence and follow one next-token prediction
  before explaining attention or generation. Distinguish tokens from words,
  attention weights from output probabilities, and sampling choices from
  factual reliability. State the architecture and mask being explained.
- **Research:** Use an accessible transformer explanation, then the architecture paper
  and official model documentation. Check tokenizer, masks, objective, and evaluation
  conditions.
- **Show and check:** Give token positions the same labels in the sequence,
  matrix axes, mask, and worked weighted sum. For one head, connect a selected
  query row to the value vectors it combines; keep this separate from the
  final vocabulary distribution. Change an earlier token or a mask entry
  and ask which dependencies are permitted to change. Attention weights
  alone do not establish a causal explanation of an output.

### Reinforcement learning foundations

- **Build:** Compare two short episodes in which the larger immediate reward
  leads to a worse later outcome. Define the state, action, reward timing,
  discount, and termination before return or value. One successful episode
  does not establish a good policy.
- **Research:** Use an introductory RL text or course section that develops episodes and
  decision rules. Bring in probability when comparing uncertain outcomes, with an
  inspected explanation of expectation.
- **Show and check:** Match each state-diagram edge to an episode row and
  its reward term in the return. For a Bellman calculation, label branch
  probabilities and distinguish averaging over transitions from averaging
  over policy actions. Change discount or one transition and ask which
  preferred action changes; compare expected values with individual episodes.

### Policy optimization and language-model post-training

- **Build:** Use a small sampled batch from a policy and explicit outcome
  scores before the objective. Distinguish reward, baseline, advantage, and
  old-to-new probability ratio. Name which method supplies each quantity;
  do not present all post-training methods as the same update.
- **Research:** Read the relevant policy-gradient derivation before PPO or GRPO. Inspect
  each original method paper and implementation for objectives, sampling, normalization,
  and differences from earlier methods.
- **Show and check:** Carry each sampled choice from its batch row to its
  score, advantage calculation, and objective term. Match a clipping graph
  to that term's advantage sign and ratio; state the inspected method's
  normalization and any extra penalties. Change one score or probability
  and ask which contributions change before tracing the update. Label the
  simplified batch and avoid claiming empirical gains from it.

### Agents and robotics

- **Build:** Follow one task from observation to proposed action, execution,
  and feedback. Include a failed or uncertain action. The plan, issued
  command, reported result, and verified environment state are distinct;
  a plausible response alone does not establish completion.
- **Research:** Inspect tool or robot interface documentation and the evaluation
  protocol. Use original results for claims about reliability or physical performance.
- **Show and check:** Match each sequence-diagram exchange to the trace's
  observation, command, and resulting state. For a robot, keep coordinate
  frames and sensor timing explicit; for a software agent, retain tool
  arguments and verification evidence. Add delay, a missing observation, or
  a failed action and ask what evidence permits retry or recovery. Compare
  outcomes under the stated model before generalizing reliability.

## Source use

Use [the source-use guide](../references/source-use.md). Catalog entries are
leads; inspect the relevant section before using it. Match the source to the
subfield and question. Start with an accessible explanation, then inspect the
technical argument or evidence needed for the agreed depth. Record the section,
its job, and any access limit in the course research notes.
