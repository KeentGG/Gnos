/* Shared presentation for ordinary JSXGraph scenes. Model logic lives in the scene. */
window.GNOSGraph = {
  create(config) {
    const text = (id, value) => { document.getElementById(id).textContent = value || ''; };
    document.title = config.title;
    text('graph-title', config.title);
    text('graph-question', config.question);
    text('graph-equation', config.equation);
    text('graph-model', config.model);
    text('graph-task', config.task);
    text('control-note', config.controlNote);
    text('axis-note', config.axes);
    if (config.resultTitle) text('result-title', config.resultTitle);
    const styles = getComputedStyle(document.documentElement);
    const colors = Object.fromEntries(['ink', 'primary', 'secondary', 'line', 'surface'].map(
      key => [key, styles.getPropertyValue('--' + key).trim()]));
    const state = { ...config.initial };
    const controls = {};
    let render = () => {};
    const ui = {
      state, controls, colors,
      curveStyle: (extra = {}) => ({ strokeColor: colors.primary, highlightStrokeColor: colors.primary,
        strokeWidth: 2.5, ...extra }),
      pointStyle: (extra = {}) => ({ name: '', withLabel: false, size: 4, showInfobox: false,
        fillColor: colors.primary, strokeColor: colors.primary,
        highlightFillColor: colors.primary, highlightStrokeColor: colors.primary, ...extra }),
      readout: value => text('graph-readout', value),
      legend: entries => {
        const legend = document.getElementById('graph-legend');
        legend.replaceChildren();
        for (const [label, curve] of entries) {
          const item = document.createElement('span');
          const sample = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
          sample.setAttribute('aria-hidden', 'true');
          sample.setAttribute('viewBox', '0 0 22 10');
          const line = document.createElementNS(sample.namespaceURI, 'line');
          Object.entries({ x1: 0, x2: 22, y1: 5, y2: 5, 'stroke-width': 2.5 }).forEach(
            ([key, value]) => line.setAttribute(key, value));
          for (const key of ['stroke', 'stroke-dasharray']) {
            const value = curve.rendNode.getAttribute(key);
            if (value) line.setAttribute(key, value);
          }
          sample.append(line);
          item.append(sample, document.createTextNode(label));
          legend.append(item);
        }
        legend.hidden = entries.length === 0;
      },
      bind: callback => { render = callback; refresh(); },
      set: (key, value) => {
        const input = controls[key];
        if (!input) throw new Error('Unknown graph control: ' + key);
        input.value = value;
        state[key] = Number(input.value);
        refresh();
      },
      reset: () => {
        Object.assign(state, config.initial);
        Object.entries(controls).forEach(([key, input]) => { input.value = state[key]; });
        if (ui.onReset) ui.onReset();
        refresh();
      },
      refresh: () => refresh(),
    };
    function refresh() {
      for (const item of config.controls || []) {
        text(item.key + '-value', Number(state[item.key]).toFixed(item.decimals ?? 1));
      }
      render();
      if (ui.board) ui.board.update();
    }
    for (const item of config.controls || []) {
      const label = document.createElement('label');
      label.htmlFor = item.key;
      label.append(document.createTextNode(item.label));
      const output = document.createElement('output');
      output.id = item.key + '-value';
      output.htmlFor = item.key;
      label.append(output);
      const input = document.createElement('input');
      Object.assign(input, { id: item.key, type: 'range', min: item.min, max: item.max,
        step: item.step, value: state[item.key] });
      input.addEventListener('input', () => { state[item.key] = Number(input.value); refresh(); });
      document.getElementById('graph-controls').append(label, input);
      controls[item.key] = input;
    }
    const area = document.getElementById('graph-board');
    area.setAttribute('aria-label', config.graphLabel || config.axes);
    const ticks = { strokeColor: colors.ink, minorTicks: 0, majorHeight: 5,
      label: { fontSize: 14, strokeColor: colors.ink } };
    ui.board = JXG.JSXGraph.initBoard('graph-board', {
      boundingbox: config.bounds, keepaspectratio: !!config.equalScale,
      axis: true, showNavigation: false, showCopyright: false, showInfobox: false,
      pan: { enabled: false }, zoom: { enabled: false },
      defaultAxes: {
        x: { strokeColor: colors.ink, highlight: false, ticks },
        y: { strokeColor: colors.ink, highlight: false, ticks },
      },
    });
    function resize() {
      if (!area.getClientRects().length) return;
      const { width, height } = area.getBoundingClientRect();
      if (width > 0 && height > 0) {
        ui.board.resizeContainer(width, height, true);
        ui.board.setBoundingBox(config.bounds, !!config.equalScale);
      }
    }
    new ResizeObserver(resize).observe(area);
    window.addEventListener('resize', () => requestAnimationFrame(resize));
    document.getElementById('reset').addEventListener('click', ui.reset);
    requestAnimationFrame(resize);
    return ui;
  },
};
