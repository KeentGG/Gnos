(() => {
  const ui = GNOSGraph.create({
    title: 'Step down a loss',
    question: 'Predict whether a larger learning rate gets closer to the minimum. Then take a step.',
    equation: 'L(w) = ½w²     w_next = w − ηw',
    model: 'This is a one-dimensional quadratic loss with derivative w and minimum at w = 0. All quantities are dimensionless. Constant-rate descent converges for 0 < η < 2; η = 2 alternates without shrinking.',
    task: 'From w = 3, compare η = 0.4 and η = 1.2. Why can crossing zero still reduce loss?',
    axes: 'x: parameter w. y: loss L(w). No units.',
    controlNote: 'Changing either control restarts from the selected initial w. Step applies one update; the dashed path records updates.',
    bounds: [-4.2, 9, 4.2, -1], initial: { eta: 0.4, start: 3 },
    controls: [
      { key: 'eta', label: 'Learning rate η', min: 0, max: 2, step: 0.1 },
      { key: 'start', label: 'Initial parameter w', min: -3.5, max: 3.5, step: 0.5 },
    ],
  });
  const { board, state, colors } = ui;
  let previousSettings = '';
  let history = [state.start];
  ui.history = history;
  const loss = board.create('functiongraph', [w => 0.5 * w * w], ui.curveStyle());
  const path = board.create('curve', [[], []], ui.curveStyle({ strokeColor: colors.secondary,
    highlightStrokeColor: colors.secondary, dash: 2 }));
  path.updateDataArray = () => { path.dataX = history.slice(); path.dataY = history.map(w => 0.5 * w * w); };
  ui.legend([['Loss L(w)', loss], ['Updates', path]]);
  const current = board.create('point', [() => history.at(-1), () => 0.5 * history.at(-1) ** 2], ui.pointStyle({ fixed: true }));
  ui.point = current;
  const step = document.createElement('button');
  step.id = 'step'; step.type = 'button'; step.textContent = 'Step';
  document.querySelector('.actions').prepend(step);
  ui.onReset = () => { previousSettings = ''; };
  ui.bind(() => {
    const settings = `${state.eta}/${state.start}`;
    if (settings !== previousSettings) { history = [state.start]; ui.history = history; previousSettings = settings; }
    const w = history.at(-1), next = w - state.eta * w;
    ui.readout(`Step ${history.length - 1}: w = ${w.toFixed(3)}, loss = ${(0.5 * w * w).toFixed(3)}. ` +
      `Next update: ${w.toFixed(3)} − ${state.eta.toFixed(1)} × ${w.toFixed(3)} = ${next.toFixed(3)}.`);
    step.disabled = history.length >= 21;
  });
  step.addEventListener('click', () => { history.push(history.at(-1) * (1 - state.eta)); ui.refresh(); });
  window.graph = ui;
})();
