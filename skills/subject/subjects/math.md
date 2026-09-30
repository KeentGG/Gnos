# Mathematics

Teacher: `teachers/math/SOUL.md` (Ben Waston).

Choose the branch by the task: calculate, model, prove, estimate, or optimize.
Check the needed operation or assumption at the point of use. Keep expressions,
equations, identities, approximations, and theorems distinct. Put hypotheses
beside the claim and state the permitted inputs.

## Ways to show the idea

Use graphs for variation, diagrams for structure, and worked notation for the
argument. Use [Excalidraw](../../excalidraw/SKILL.md) for a quick labeled figure,
[Pinepaper](../../pinepaper/SKILL.md) when a curve and geometric state must
change together, and [Manim](../../manim-voice-animation/SKILL.md) for narrated change.
Use a plotting library when exact data or numerical curves matter. A picture
can suggest a theorem; it does not replace a proof.

Write lesson math as LaTeX with `$...$` or `$$...$$`, such as `$\mathbb{R}^n$`
and `$P^{-1}$`. Read [the math reference](../references/math.md) for detailed
prerequisite checks and visual patterns. Ben owns the mathematical argument;
a domain teacher keeps responsibility for what the variables mean.

## Teaching each area

Choose the matching section. Its order suggests how to build the topic; it is
not a complete syllabus. Course design uses the starting point and source
checks. Lesson design chooses the views that explain the difficult steps.
Treat the named confusion as a possibility, not a diagnosis of this learner.

### Arithmetic and algebra

- **Build:** Use a quantity model for an operation, or a small equation such as
  $x(x-1)=0$ for solving. An expression names a value; an equation asserts equality.
  Explain why dividing by $x$ would discard a possible solution.
- **Research:** Use an introductory algebra section with worked operations and excluded
  cases. Check the permitted number system and operation.
- **Show and check:** Match a number-line move or area to the same numbers in
  the calculation. For the equation, connect the graph's two roots to the
  two algebraic branches and substitute both answers. Change the right side
  to $2x$; ask which division is permitted before solving again.

### Geometry and trigonometry

- **Build:** Begin with a right triangle whose legs are known and whose angle
  is sought. Separate a given right angle from an angle that merely looks
  right. State the hypotheses before using a length or trigonometric relation.
- **Research:** Inspect a geometry or trigonometry chapter that states the givens and
  proves the relation. A labeled figure should match those hypotheses.
- **Show and check:** Carry the triangle's side labels into the ratio and
  calculation. A unit-circle view can explain how the same ratio becomes a
  function of angle; map the triangle's coordinates to its sine and cosine.
  Change the size, then the angle, and ask what survives. A moving point can
  test the conjecture, but the derivation must explain it.

### Calculus

- **Build:** Start with a position record for rate, or a flow record for
  accumulation. Compute a finite difference or sum before taking a limit.
  Keep position, velocity, and accumulated amount distinct, including units.
- **Research:** Use a calculus chapter that develops the limit before the rule. Check
  domains, units, and a worked example. Use analysis for a requested rigorous
  justification.
- **Show and check:** Map the same two table rows to secant endpoints and the
  numerator and denominator of the quotient. For accumulation, map each
  flow rectangle to one sum term. Link interval changes to displayed values
  when useful. Ask for a prediction after halving the interval or doubling
  the flow; explain what the limit argument adds to the picture.

### Differential equations and dynamics

- **Build:** Begin with exponential decay, $y'=-ky$, and a specified initial
  amount. The rule gives a slope at each state; it does not by itself choose
  the trajectory. Explain the role of initial or boundary conditions and
  the assumptions needed for a unique solution.
- **Research:** Inspect a differential-equations text for existence assumptions and
  solution methods. Use a numerical-methods source when discretization affects the
  example.
- **Show and check:** Take one slope-field point through a numerical step,
  then locate that state on the time plot. Keep equation, step size, and
  solver visible. Change the initial amount and then $k$: ask which changes
  the starting point and which changes the decay time. Compare the computed
  trace with the analytic solution before using a more complex rule.

### Linear algebra

- **Build:** Apply a shear or projection to the two basis vectors, then to
  one vector made from them. Distinguish changing the vector from describing
  the same vector in another basis. Matrix entries encode a map relative to
  the chosen input and output bases.
- **Research:** Use a linear-algebra chapter that connects maps, bases, and matrices.
  Check dimensions and whether the argument depends on a chosen basis.
- **Show and check:** Match each matrix column to one basis image. Use the
  same coefficients in the vector decomposition, worked product, and output
  arrow; retain the original grid for comparison. Change one column and ask
  which component of the image changes. For a basis change, hold the physical
  vector fixed while updating its coordinates, then verify by reconstruction.

### Probability

- **Build:** Compare two draws without replacement with two independent coin
  flips. Name the outcomes and the information available before the second
  event. Conditioning can change its probability; an expected value need
  not be a possible outcome of one trial.
- **Research:** Use a probability text with explicit sample spaces and model
  assumptions. Inspect the counting argument or derivation before reusing its formula.
- **Show and check:** Match each tree path to a table row and each branch
  probability to a factor in its calculation. A repeated-trial plot shows
  how frequencies vary around the model probability. Change to drawing with
  replacement and ask which branches and products must change before running
  the simulation. Keep model assumptions separate from observed evidence.

### Statistics and inference

- **Build:** Ask for a population mean from a sampled set of measurements.
  State who or what could enter the sample. Distinguish the observed estimate,
  its sampling uncertainty, and any causal claim about a difference.
- **Research:** Use an introductory statistics chapter for the estimator and an original
  study or dataset guide for the sampling process. Check missingness, dependence, and
  the inferential assumptions.
- **Show and check:** Connect plotted observations to the calculation of one
  estimate, then place that estimate in a repeated-sampling distribution.
  For a confidence interval, show coverage across repetitions under the
  stated procedure. Change random sampling to a convenience sample and ask
  why a narrow interval may still miss the target; increasing sample size
  does not repair the sampling design.

### Discrete and abstract mathematics

- **Build:** Start with a small graph, truth claim, or operation table that
  instantiates the definition. Compare a valid case and a near-miss before
  proving the general claim. Examples do not prove a universal statement,
  and reversing an implication changes it.
- **Research:** Use a discrete-math or algebra text with the exact structure and proof.
  Check the domain before reusing a familiar theorem.
- **Show and check:** Carry the same vertices, propositions, or elements
  from the diagram or table into each proof step. Mark where a hypothesis
  is used. Remove one edge, change one truth assignment, or drop one axiom
  and ask whether the proof still applies. Use a counterexample to explain
  the failure rather than treating a few successful tests as proof.

### Analysis and topology

- **Build:** Compare a continuous function on a closed bounded interval
  with $1/x$ on $(0,1)$, or use neighborhoods to distinguish an open set from its boundary.
  Name the question the definition resolves. Quantifier order and exceptional
  points matter even when two pictures look similar.
- **Research:** Inspect the definition, hypotheses, proof, and a counterexample in an
  analysis or topology text. Compare conventions when sources differ.
- **Show and check:** Match the marked point, interval, or neighborhood to
  the variables in the definition. Work through who chooses each bound and
  what may depend on that choice; then show where the proof uses it. Change
  the domain or include a boundary point and ask for a new witness or
  counterexample. The picture guides the argument without replacing it.

### Optimization and numerical math

- **Build:** Work one update on an unequal-curvature quadratic with stated
  constraints, if any. Separate descent direction, step length, and convergence.
  A stationary point may not be a minimum. For a twice continuously
  differentiable function, a positive-definite Hessian at a stationary point
  gives a local test, not global convexity. Numerical results also depend
  on conditioning and tolerance.
- **Research:** Use an optimization or numerical-analysis chapter for assumptions and
  error bounds. Check a reference implementation only after the mathematical rule is
  clear.
- **Show and check:** Map one row of the update table to an arrow on the
  contours and one point on the objective trace. Explain why a downhill
  direction can still overshoot with a large step. Predict the result of
  changing step size or curvature, then inspect the same start and stopping
  rule. Separate the observed convergence from the theorem's assumptions.

## Source use

Use [the source-use guide](../references/source-use.md). Catalog entries are
leads; inspect the relevant section before using it. Match the source to the
subfield and question. Start with an accessible explanation, then inspect the
technical argument or evidence needed for the agreed depth. Record the section,
its job, and any access limit in the course research notes.
