(() => {
  const ui = GNOSGraph.create({
    title: 'A shift in demand',
    question: 'Raise demand with supply fixed. Predict how equilibrium price and quantity change.',
    equation: 'Demand: P = a − Q     Supply: P = 2 + ½Q',
    model: 'This illustrative market uses linear inverse demand and supply. Price is in dollars per unit and quantity is in units. The demand intercept a changes; supply and both slopes remain fixed. The model is not an empirical forecast.',
    task: 'Set a = 11. Find the equilibrium. Explain why demand shifts but supply does not.',
    axes: 'x: quantity Q (units). y: price P ($/unit).',
    controlNote: 'The dashed demand curve keeps a = 8 for comparison. The solid demand curve follows a; supply is fixed.',
    bounds: [-1.3, 13, 13, -1.3], initial: { a: 8 },
    controls: [{ key: 'a', label: 'Demand intercept a ($/unit)', min: 5, max: 12, step: 0.5 }],
  });
  const { board, state, colors } = ui;
  const baseline = board.create('functiongraph', [q => 8 - q, 0, 8], ui.curveStyle({ dash: 2 }));
  const demand = board.create('functiongraph', [q => state.a - q, 0, () => state.a], ui.curveStyle());
  const supply = board.create('functiongraph', [q => 2 + 0.5 * q, 0, 13], ui.curveStyle({
    strokeColor: colors.secondary, highlightStrokeColor: colors.secondary, dash: 3 }));
  ui.legend([['Demand', demand], ['Baseline', baseline], ['Supply', supply]]);
  const quantity = () => (state.a - 2) / 1.5;
  const price = () => 2 + 0.5 * quantity();
  ui.point = board.create('point', [quantity, price], ui.pointStyle({ fixed: true }));
  board.create('segment', [[quantity, 0], [quantity, price]], ui.curveStyle({ strokeColor: colors.ink,
    highlightStrokeColor: colors.ink, strokeWidth: 1, dash: 2 }));
  board.create('segment', [[0, price], [quantity, price]], ui.curveStyle({ strokeColor: colors.ink,
    highlightStrokeColor: colors.ink, strokeWidth: 1, dash: 2 }));
  ui.bind(() => ui.readout(`Equilibrium: Q = ${quantity().toFixed(2)}, P = $${price().toFixed(2)}. ` +
    'Baseline: Q = 4, P = $4.'));
  window.graph = ui;
})();
