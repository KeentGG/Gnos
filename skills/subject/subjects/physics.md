# Physics

Teacher: `teachers/physics/SOUL.md` (Mira Sen).

Choose the branch by the physical question. Name the system, frame, quantities,
and approximation before calculating. Develop a qualitative prediction, then
check units, sign, and a limiting case. Distinguish a model prediction from a
measurement and state when the approximation fails.

## Ways to show the idea

Use diagrams for setup, graphs for quantities, and equations for their relation.
Use [Excalidraw](../../excalidraw/SKILL.md) for boundaries or apparatus,
[Manim](../../manim-voice-animation/SKILL.md) for narrated motion, and
[JSXGraph](../../jsxgraph/SKILL.md) for linked quantity plots. Use
[Pinepaper](../../pinepaper/SKILL.md) when a composed apparatus or spatial scene
must change with the system. A simulation
lets the learner test a changed condition. Keep the same units and initial
state across views. Generated motion is a model illustration.

Read [the physics reference](../references/physics.md) for detailed examples
and visual conventions. Mira owns the physical meaning; math and CS support
only the calculation or implementation needed for this question.

## Teaching each area

Choose the matching section. Its order suggests how to build the topic; it is
not a complete syllabus. Course design uses the starting point and source
checks. Lesson design chooses the views that explain the difficult steps.
Treat the named confusion as a possibility, not a diagnosis of this learner.

### Mechanics

- **Build:** Use a thrown object at the top of its path, with drag neglected
  and the frame stated. Predict velocity and acceleration before calculating.
  Zero vertical velocity does not mean zero acceleration, and constant
  velocity does not require a net force.
- **Research:** Use an introductory mechanics chapter with a worked force or energy
  argument. Check the frame and approximations before adopting a formula.
- **Show and check:** Connect the gravity arrow in the free-body diagram to
  the acceleration term, the velocity plot's slope, and the curved path at
  the same instant. Keep force, velocity, and acceleration visually distinct.
  Change initial velocity or add drag and ask which prediction survives;
  explain the changed interaction before updating the graphs.

### Oscillations and waves

- **Build:** Begin with one marked point on a vibrating string, then follow
  a pulse along the string. Distinguish the point's local oscillation from
  propagation of the disturbance; the point does not travel with the pulse.
- **Research:** Inspect a waves chapter for the relation between the oscillator and
  propagation. Check the boundary conditions and whether the model is dispersive.
- **Show and check:** Connect the marked point's height in a spatial snapshot
  to the displacement-versus-time plot at that instant. Keep the axes explicit:
  one varies position, the other time. Use a shared clock if both move. With
  wave speed fixed, change frequency and ask for the wavelength and local
  period; change an end condition to explain reflection separately.

### Thermodynamics

- **Build:** Compare two processes taking a gas between the same equilibrium
  states. Name the boundary, heat transfer, and work before applying the first
  law. Temperature is a state property; heat and work describe transfers
  and depend on the process.
- **Research:** Use a thermodynamics chapter and any needed property table. Check sign
  conventions, process assumptions, and the range of the data.
- **Show and check:** Match arrows across the boundary to signed terms in
  the energy ledger. For a quasistatic pressure-volume path, connect its
  area to work using the chosen convention; connect endpoints to internal
  energy change. Draw a different path between the same states and ask what
  remains equal and what must be recalculated.

### Electricity and magnetism

- **Build:** Use a source charge and a movable test charge, or a single
  resistor circuit with named nodes. Separate field from force and potential
  from potential energy; in a circuit, distinguish current from voltage.
- **Research:** Use an electromagnetism or circuits chapter that defines the quantities.
  Inspect apparatus documentation when interpreting a real measurement.
- **Show and check:** At one location, map the field arrow to $q\mathbf E$
  and the potential value to $qV$. Reverse the test charge and ask which
  quantities reverse and which stay fixed, under the test-charge approximation.
  For circuits, carry node labels from the schematic into voltage differences
  and loop equations; change a resistance and predict current before solving.

### Optics

- **Build:** Start with a lens image or a slit pattern and state the
  relevant dimensions and wavelength. A ray model locates an image; a wave
  model explains interference or diffraction. Establish which approximation
  answers the observation before choosing a formula.
- **Research:** Choose a geometrical- or wave-optics source to match the scale. Inspect
  the approximation before applying a ray or diffraction formula.
- **Show and check:** Match object and image distances in a ray diagram to
  the lens equation. For a slit, connect path or phase differences at a screen
  point to the corresponding intensity-plot position. Predict what changing
  wavelength or aperture does before recalculating; explain when the original
  approximation becomes insufficient.

### Relativity

- **Build:** Give two inertial observers the same pair of events, then ask
  how each assigns position and time. Separate event identity, simultaneity,
  and the invariant interval. Scope an inertial-frame calculation to special
  relativity; use a dedicated treatment for gravitation or curved spacetime.
- **Research:** Use a relativity text that defines clocks, synchronization, frames, and
  the transformation. Check the physical assumptions before using a diagram.
- **Show and check:** Carry the same event labels from the spacetime diagram
  into one coordinate transformation and a table of both observers' values.
  State the axis units and interval sign convention. Calculate the interval
  in each frame, then change relative speed and ask which coordinates can
  change and which comparison must remain invariant.

### Quantum physics

- **Build:** Use a prepared two-state system and a specified measurement
  basis. Calculate possible outcomes before discussing repeated trials.
  Amplitudes are not probabilities, and the state is not a hidden classical
  trajectory through the apparatus.
- **Research:** Use a quantum text for the state, observable, and probability rule.
  Inspect the original experimental setup when explaining an empirical result.
- **Show and check:** Link each apparatus outcome label to its amplitude,
  squared magnitude, and bar in the probability plot. Repeated-trial counts
  sample that stated model. Change the preparation or measurement basis and
  ask for the new distribution; do not depict a basis change as an observed
  path between hidden states. Identify experimental data separately.

### Experimental physics

- **Build:** Start with an instrument reading and a calibration against a
  reference. Separate repeatability, resolution, and systematic offset.
  A precise fitted line can still give a biased physical estimate.
- **Research:** Inspect the instrument manual, calibration method, and original
  measurements. Use a laboratory-methods source to assess uncertainty and fit quality.
- **Show and check:** Map the measured quantity in the apparatus to a data
  column, graph axis, and fitted parameter with units. Pair the fit with
  residuals for the same observations. Add a plausible calibration offset
  and ask why residual scatter may look unchanged while the estimate moves;
  distinguish this from taking more repeated readings.

### Computational physics

- **Build:** Take one numerical step for a harmonic oscillator with specified
  initial position and velocity. Separate the continuous physical rule from
  the discrete update. A smooth computed trajectory can still be unstable
  or violate the model's conserved energy.
- **Research:** Use a numerical-methods source plus a known analytic or limiting case.
  Check discretization, solver tolerances, and conservation error.
- **Show and check:** Match the old and new state in the update table to
  code variables, phase-plane points, and the time trace. Plot energy error
  alongside trajectory error against an analytic case. Predict what halving
  the time step should improve, then test it with the same initial state;
  distinguish discretization error from a wrong force rule.

## Source use

Use [the source-use guide](../references/source-use.md). Catalog entries are
leads; inspect the relevant section before using it. Match the source to the
subfield and question. Start with an accessible explanation, then inspect the
technical argument or evidence needed for the agreed depth. Record the section,
its job, and any access limit in the course research notes.
