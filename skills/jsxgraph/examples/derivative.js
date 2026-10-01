(() => {
  const ui = GNOSGraph.create({
    title: 'Slope at a point',
    question: 'Move along y = x². Where does the tangent fall, flatten, or rise?',
    equation: 'y = x²     dy/dx = 2x',
    model: 'The curve is y = x² for real x. Its derivative is 2x. Both axes are dimensionless. The tangent describes local change; it is not the curve away from the contact point.',
    task: 'At x = −1, predict how y changes for a small increase in x. Check, then explain the tangent.',
    axes: 'Horizontal: x. Vertical: y. Both are dimensionless.',
    graphLabel: 'Parabola y equals x squared with a movable contact point and its tangent.',
    controlNote: 'Drag the point or use the x slider. The dashed line is the tangent. Reset restores x = 1.',
    bounds: [-3.2, 8, 3.2, -2], initial: { x: 1 },
    controls: [{ key: 'x', label: 'Contact point x', min: -2.5, max: 2.5, step: 0.1 }],
  });
  const { board, state, colors } = ui;
  const curve = board.create('functiongraph', [x => x * x], ui.curveStyle());
  const point = board.create('glider', [1, 1, curve], ui.pointStyle());
  const tangent = board.create('functiongraph', [x => 2 * state.x * (x - state.x) + state.x ** 2],
    ui.curveStyle({ strokeColor: colors.secondary, highlightStrokeColor: colors.secondary, dash: 2 }));
  ui.point = point;
  ui.tangent = tangent;
  ui.legend([['y = x²', curve], ['Tangent', tangent]]);
  point.on('drag', () => ui.set('x', point.X()));
  ui.bind(() => {
    point.moveTo([state.x, state.x ** 2]);
    const slope = 2 * state.x;
    ui.readout(`At x = ${state.x.toFixed(1)}, y = ${(state.x ** 2).toFixed(2)} and slope = ${slope.toFixed(1)}. ` +
      (slope < 0 ? 'The tangent falls as x increases.' : slope > 0 ? 'The tangent rises as x increases.' : 'The tangent is horizontal at this point.'));
  });
  window.graph = ui;
})();
