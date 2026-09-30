# Chemical engineering

Choose the process boundary, basis, units, composition, and conserved quantities
before algebra. Distinguish steady state from equilibrium, and conversion from
selectivity. Supply chemistry only where bonding, reactions, or equilibrium
blocks the explanation.

## Ways to show the idea

Use [Excalidraw](../../excalidraw/SKILL.md) for fixed streams and control volumes,
[Pinepaper](../../pinepaper/SKILL.md) when a process state and its graph must
change together, and property tables for exact values.
Use [Manim](../../manim-voice-animation/SKILL.md) for narrated transient change
and a simulation to test flow, temperature, residence time, or controller
settings. Match stream names and units across the picture and balance.
Keep property ranges, assumptions, and physical limits visible. A teaching
simulation does not validate equipment or an operating procedure.

Chemical engineering owns process assumptions and feasibility. Math, physics,
and CS support the needed equation, mechanism, or implementation. No chemical
engineering teacher is assigned by default.

## Teaching each area

Choose the matching section. Its order suggests how to build the topic; it is
not a complete syllabus. Course design uses the starting point and source
checks. Lesson design chooses the views that explain the difficult steps.
Treat the named confusion as a possibility, not a diagnosis of this learner.

### Material and energy balances

- **Build:** Begin with a mixing tank, named inlet and outlet streams, and
  a stated mass or molar basis. Separate total-mass balance from species
  balance, including reaction terms where needed. Steady state means zero
  accumulation, not zero flow or no reaction.
- **Research:** Use an engineering balances chapter and a stated process case. Check
  units, basis, composition, and which quantities are conserved.
- **Show and check:** Carry each stream label and composition from the
  control-volume drawing into a balance-table row and signed equation term.
  Connect accumulation to the slope of the inventory trace. Change an inlet
  and ask whether the outlet can change immediately under the stated mixing
  and flow assumptions. Check a steady limit and the corresponding energy
  balance before adding process complexity.

### Thermodynamics

- **Build:** Follow a pure fluid through heating or a mixture toward phase
  equilibrium with its state and composition specified. Distinguish a state
  property, an equilibrium condition, and a process path. A steady flowing
  process need not be at equilibrium.
- **Research:** Use thermodynamic property references and the relevant model
  documentation. Check phase, composition, reference state, and validity range.
- **Show and check:** Match the state point on a phase diagram to the table
  lookup, reference state, and property values used in the energy calculation.
  For a pure fluid changing phase at fixed pressure, track phase fraction
  rather than assuming all added energy raises temperature. Change pressure
  or composition and ask which property lookup and equilibrium relation
  must change; keep the model's
  validity range visible.

### Transport phenomena

- **Build:** Start with heat conduction through a slab or diffusion across
  a layer. State boundaries, geometry, and properties before using the flux
  law. Distinguish a local flux from the total transfer rate and from the
  accumulation inside the region.
- **Research:** Use a transport text for constitutive laws and boundary conditions.
  Inspect measured property data before assigning numerical values.
- **Show and check:** Connect the profile's local slope to the signed flux
  arrow and multiply by area for total rate. Map the difference between
  inward and outward rates to accumulation in the balance. Double thickness
  or change a boundary value and predict the steady profile and rate under
  the same property assumptions; for a transient, connect a marked location
  to its time trace and test conservation.

### Reaction engineering

- **Build:** Use a stated reaction in a batch vessel, then compare a flow
  reactor if needed. Define rate per volume, conversion, and selectivity
  separately. Residence time, elapsed batch time, and mixing assumptions
  cannot be interchanged without changing the balance.
- **Research:** Use a reaction-engineering chapter plus measured kinetic data for the
  stated reaction. Check rate units, temperature range, and mixing assumptions.
- **Show and check:** Carry reactor volume, stream labels, and concentration
  from the sketch into the rate law and species balance. For a batch, map
  the rate to the concentration trace's slope; for flow, distinguish time
  variation from change along the reactor. Change residence time or
  temperature and predict conversion under the stated kinetics, then check
  the balance and whether selectivity follows the same trend.

### Separations

- **Build:** Use a binary feed with a target product purity and recovery.
  State the physical separation mechanism before a stage calculation.
  Purity and recovery differ; an equilibrium limit does not establish the
  rate or equipment needed to approach it.
- **Research:** Use a separations text with equilibrium and mass-transfer data. Check
  composition range, stage assumptions, and the definition of the target purity.
- **Show and check:** Match phase-plot coordinates to compositions on the
  stage diagram and stream terms in the material balance. Label ideal-stage
  or transfer assumptions explicitly. Change feed composition or a relevant
  operating ratio and ask how product amount, purity, and recovery respond;
  use rate data separately when explaining departure from equilibrium.

### Process design and control

- **Build:** Start with a tank-level or temperature disturbance and identify
  the measured, controlled, and manipulated variables. Feedback responds to
  a measured error; it does not remove sensor delay or actuator limits.
  Correcting one variable can encounter another process constraint.
- **Research:** Use process-dynamics and control references with stated equipment
  limits. Teaching models do not establish safe operating procedures.
- **Show and check:** Map the sensor, controller, and actuator on the
  flowsheet to signal labels in the block diagram and traces of setpoint,
  output, and manipulated input. Apply the same disturbance when comparing
  settings. Add delay or an actuator limit and ask why recovery changes;
  mark constraints and distinguish the teaching response from validated
  equipment behavior or an operating procedure.

## Source use

Use [the source-use guide](../references/source-use.md). Catalog entries are
leads; inspect the relevant section before using it. Match the source to the
subfield and question. Start with an accessible explanation, then inspect the
technical argument or evidence needed for the agreed depth. Record the section,
its job, and any access limit in the course research notes.
