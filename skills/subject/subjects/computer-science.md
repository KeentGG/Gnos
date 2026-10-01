# Computer science

Teacher: `teachers/computer-science/SOUL.md` (Theo Park).

Choose the branch by the behavior the learner wants to explain or build.
Name inputs, outputs, state, and failure assumptions. Develop a small working
case before adding an abstraction. A passing run is evidence about that run;
use an invariant or argument for a claim over all inputs.

## Ways to show the idea

Use [Excalidraw](../../excalidraw/SKILL.md) for structure and boundaries,
[Manim](../../manim-voice-animation/SKILL.md) for narrated state changes, and
[Pinepaper](../../pinepaper/SKILL.md) for linked or interactive diagrams.
Code and traces connect those pictures to executable behavior. Use JSXGraph
to compare mathematical cost functions and scientific plots for measured
timings; do not infer complexity from a timing curve. Algorithm graphs remain
node-and-edge diagrams rather than coordinate plots.
Read [the CS reference](../references/computer-science.md) when the lesson
needs a detailed trace, invariant, or visual construction pattern.

Theo leads the explanation. Math supports a specific proof or quantitative
step; the application subject owns the meaning of data and success.

## Teaching each area

Choose the matching section. Its order suggests how to build the topic; it is
not a complete syllabus. Course design uses the starting point and source
checks. Lesson design chooses the views that explain the difficult steps.
Treat the named confusion as a possibility, not a diagnosis of this learner.

### Programming

- **Build:** Use two names referring to one list, or a short function with
  one call. Predict each line's effect before executing it. Separate values,
  names, objects, mutation, and rebinding; a function's local state and return
  value have different roles.
- **Research:** Inspect the language reference and a small runnable example for the
  actual version. Separate language guarantees from library behavior.
- **Show and check:** Give each object the same identity in code annotations,
  the trace table, and memory sketch. Show which arrow changes on rebinding
  and which object changes on mutation. Replace an alias with a shallow copy
  of a nested list and ask which later mutations remain shared. For a
  function, trace a boundary input through the actual return path.

### Data structures

- **Build:** Insert one item into an array or linked list and state the
  required operations. Separate the logical sequence from storage layout,
  ownership, and the work required to preserve the structure.
- **Research:** Use a data-structures chapter and the chosen runtime documentation.
  Check ownership, operation costs, and iterator or mutation guarantees.
- **Show and check:** Match an index or node identity in the diagram to each
  access and update in the code trace. Show the before and after links or
  shifted entries, then check the invariant. Move the insertion to the head
  or an empty collection and ask which steps and costs change. If stepping
  is interactive, the code position and structure must show the same state.

### Algorithms

- **Build:** Compare linear search with binary search on a small sorted
  list. Fix whether interval endpoints are included before tracing. The
  shrinking search region explains the method only when its invariant and
  sorted-input assumption are explicit.
- **Research:** Inspect a university algorithms chapter with pseudocode and proof. Check
  the input domain, invariant, termination argument, and cost model.
- **Show and check:** Map each pseudocode step to the table's bounds and the
  highlighted surviving interval. Explain why discarded values cannot be
  answers and why the interval shrinks. Test an absent target and a singleton
  list before deriving a cost bound. For graph methods, use the same mapping
  between code step, frontier entry, and visited or finalized node.

### Systems and operating systems

- **Build:** Follow a read or allocation from one program through the
  runtime and operating-system boundary. Distinguish the requested operation
  from the resources and mechanisms that implement it. A language value,
  virtual address, and physical location are different accounts.
- **Research:** Use an operating-systems chapter for the mechanism and platform
  documentation for actual behavior. Check the memory model or system-call contract.
- **Show and check:** Match each boundary crossing in the layered diagram
  to a trace event and its input, result, or state change. For concurrency,
  put two read-modify-write sequences beside one shared counter so the lost
  update is visible. Change the interleaving or resource limit and predict
  the result; verify the relevant platform contract rather than generalizing
  from one observed run.

### Networks and distributed systems

- **Build:** Let a server complete a request but lose its response. State
  what the client and server each know when the client times out. Missing a
  response does not establish that the operation failed or make a retry safe.
- **Research:** Inspect the protocol specification for messages and guarantees. Use a
  distributed-systems chapter or original paper for failure assumptions.
- **Show and check:** Carry request IDs from participant lanes into logs and
  the server's resulting state. Compare a lost request with a lost response;
  both can produce the same client timeout. Add a retry and ask whether the
  operation can happen twice, then trace any deduplication rule and its
  persistence assumptions. Keep local event order distinct from a claimed
  global clock order.

### Relational data and queries

- **Build:** Ask for customers and their orders from two tiny tables with
  explicit keys. A join produces matching row combinations, so one customer
  can appear more than once. Decide whether the question asks for rows,
  distinct customers, or an aggregate before writing SQL.
- **Research:** Use a relational-database chapter for keys and query meaning. Check
  official engine documentation for NULL, ordering, constraints, and query plans.
- **Show and check:** Match each result row to its two source rows and the
  join predicate beside the SQL. Use the key diagram to explain cardinality,
  then add a second order or a customer with none. Predict multiplicity and
  the difference between inner and outer joins before execution. A plan tree
  explains how the engine obtains the result, separately from its meaning.

### Transactions and storage

- **Build:** Use a two-step transfer and another transaction reading the
  balances, or a crash between writes. Separate partial effects, concurrent
  visibility, and committed-state recovery: atomicity, isolation, and
  durability answer different questions.
- **Research:** Inspect the engine documentation for the chosen isolation level and
  recovery behavior. Use a database-systems chapter for locking, logging, indexes, or
  storage.
- **Show and check:** Carry transaction IDs and row values from the lanes
  into a state table at each read, write, and commit. Move a competing read
  or crash to another point and ask what the documented guarantee permits.
  For storage, connect a page or index change to its log and recovery step;
  label a schematic trace as such rather than implying it was observed.

### Theory and languages

- **Build:** Use a tiny recognizer, such as binary strings with an even
  number of ones, or an expression with ambiguous grouping. State the
  language or grammar before tracing. Acceptance, syntactic grouping, and
  program meaning are different claims.
- **Research:** Use a theory or language-semantics text with explicit definitions and
  proofs. Verify the accepted language and the domain of each claim.
- **Show and check:** Map each consumed symbol to a transition-table row
  and state-diagram edge; explain the state invariant before proving
  acceptance. Change one symbol and predict the result. For a grammar,
  map tokens to parse-tree leaves and then to evaluation steps; change
  parentheses to reveal the difference between grouping and meaning.

### AI and machine learning

- **Build:** Trace one prediction from input features to output, alongside
  a baseline and held-out case. Separate what the code computes from whether
  the learned rule generalizes. The AI guide owns model and evaluation claims.
- **Research:** Inspect official implementation documentation and a reproducible
  evaluation. Use the AI guide for model assumptions and evidence.
- **Show and check:** Match each tensor in the shape diagram to a code
  variable and one numeric example, then carry the prediction into the error
  table. Change batch size or supply an invalid shape and ask which contracts
  change and where a failure occurs. Return questions about leakage, model
  assumptions, or generalization to the AI guide.

### APIs and software design

- **Build:** Start with a paginated read or state-changing request and its
  documented contract. Separate a successful example from promises about
  errors, compatibility, and retries. Use an interface already relevant to
  the learner's task rather than introducing a new service.
- **Research:** Inspect the API specification, provider documentation, and relevant
  protocol standard for the actual version. Check authentication, errors, pagination,
  timeouts, and retries as needed.
- **Show and check:** Match each field in a concrete request and response
  to its interface rule and place each exchange on a sequence diagram.
  Carry a pagination token or request ID through the next step. Change an
  input or interrupt the response, then predict behavior from the contract
  before tracing it; mark unspecified behavior instead of inventing it.

### Security

- **Build:** Follow one untrusted value toward a query, rendered page, or
  file operation in a bounded teaching example. Name the asset, attacker
  capability, and trust boundary. Validation, encoding, parameterization,
  and authorization solve different problems.
- **Research:** Inspect the relevant security or interface specification and a minimal
  reproducer. Verify the source-to-sink path and the guarantee of the defense.
- **Show and check:** Match the data-flow arrows to the exact source,
  transformations, and sink in the code. Compare the vulnerable operation
  with the defense at the relevant boundary. Change the sink or required
  permission and ask whether that defense still applies. Keep toy results
  separate from verified claims about a deployed system.

## Source use

Use [the source-use guide](../references/source-use.md). Catalog entries are
leads; inspect the relevant section before using it. Match the source to the
subfield and question. Start with an accessible explanation, then inspect the
technical argument or evidence needed for the agreed depth. Record the section,
its job, and any access limit in the course research notes.
