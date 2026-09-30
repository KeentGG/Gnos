/* Run against rendered course pages, never against a graph editor preview. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

async function inspect(frame, name, width) {
  await frame.waitForFunction(() => window.graph && window.graph.board);
  for (const view of [...(width >= 1000 ? ['both'] : []), 'controls', 'model', 'result']) {
    await frame.locator(`button[data-view="${view}"]`).click();
    await frame.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const overflow = await frame.evaluate(() => {
    const elements = [document.documentElement, document.body, document.querySelector('.sim-shell'),
      ...document.querySelectorAll('.sim-pane:not([hidden]), .sim-pane:not([hidden]) .readout')];
    return elements.filter(element => element.scrollWidth > element.clientWidth + 2 ||
      element.scrollHeight > element.clientHeight + 2).map(element => ({
        element: element.className || element.tagName,
        width: [element.scrollWidth, element.clientWidth], height: [element.scrollHeight, element.clientHeight],
      }));
  });
    assert.deepEqual(overflow, [], `${name} ${view} at ${width}px overflows: ${JSON.stringify(overflow)}`);
  }
  await frame.waitForFunction(() => document.getElementById('graph-board').clientWidth > 100);
  const box = await frame.locator('#graph-board').boundingBox();
  assert(box.width > 100 && box.height > 200, `${name} graph is too small`);
  const expectedPalette = { derivative: '#445D48', 'gradient-descent': '#72383D', 'supply-demand': '#0274BD', wine: '#8B0000' };
  assert.equal(await frame.evaluate(() => window.graph.colors.primary), expectedPalette[name]);
}

(async () => {
  fs.mkdirSync(config.screenshots, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const errors = [], external = [];
    const context = await browser.newContext({ reducedMotion: 'reduce' });
    // The existing viewer requests web fonts; the graph itself must be offline.
    await context.route(/^https?:/, route => route.abort());
    context.on('request', request => {
      if (/^https?:/.test(request.url()) && request.frame().parentFrame()) external.push(request.url());
    });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(error.message));
    for (const [name, file] of Object.entries(config.pages)) {
      for (const width of [1200, 768, 390, 320]) {
        await page.setViewportSize({ width, height: 1000 });
        await page.goto(pathToFileURL(file).href);
        await page.locator('button[data-tab="lessons"]').click();
        const iframe = page.locator('iframe.simulation-frame');
        assert.equal(await iframe.count(), 1);
        assert.equal(await iframe.getAttribute('sandbox'), 'allow-scripts');
        await iframe.scrollIntoViewIfNeeded();
        const frame = await (await iframe.elementHandle()).contentFrame();
        const defaultView = (await iframe.boundingBox()).width >= 1000 ? 'both' : 'controls';
        await frame.waitForFunction(expected => document.querySelector('.sim-panes').dataset.view === expected, defaultView);
        await inspect(frame, name, width);
        if (width === 1200 || width === 390) {
          if (width === 1200) {
            await frame.locator('button[data-view="both"]').click();
            await frame.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
          }
          await iframe.screenshot({ path: path.join(config.screenshots, `${name}-${width}-initial.png`) });
        }
        await frame.locator('button[data-view="controls"]').click();
        const control = frame.locator('input[type="range"]').first();
        const before = await frame.evaluate(() => ({ ...window.graph.state }));
        await control.focus();
        await control.press('ArrowRight');
        const changed = await frame.evaluate(() => ({ ...window.graph.state }));
        assert.notDeepEqual(changed, before, 'Keyboard input must change the controlled value');
        await frame.locator('button[data-view="model"]').click();
        await frame.locator('button[data-view="result"]').click();
        assert.deepEqual(await frame.evaluate(() => ({ ...window.graph.state })), changed);
        await frame.locator('button[data-view="controls"]').click();
        await frame.locator('#reset').click();
        if (name === 'derivative' || name === 'wine') {
          await frame.evaluate(() => window.graph.set('x', -1));
          const values = await frame.evaluate(() => ({ x: graph.point.X(), y: graph.point.Y(),
            tangent: graph.tangent.Y(0), state: graph.state.x }));
          assert(Math.abs(values.x + 1) < 1e-9 && Math.abs(values.y - 1) < 1e-9);
          assert(Math.abs(values.tangent + 1) < 1e-9);
          assert.match(await frame.locator('#graph-readout').innerText(), /slope = −?\-?2\.0/);
          // Check both slider endpoints, then a pointer drag in the visible board.
          for (const x of [-2.5, 2.5]) {
            await frame.evaluate(value => graph.set('x', value), x);
            assert(Math.abs(await frame.evaluate(() => graph.point.Y()) - x * x) < 1e-8);
          }
          await frame.evaluate(() => graph.set('x', 1));
          await frame.locator('button[data-view="result"]').click();
          const coordinates = await frame.evaluate(() => {
            const board = graph.board, origin = board.origin.scrCoords;
            return { start: graph.point.coords.scrCoords.slice(1),
              end: [origin[1] - board.unitX, origin[2] - board.unitY] };
          });
          const rect = await frame.locator('#graph-board').boundingBox();
          await page.mouse.move(rect.x + coordinates.start[0], rect.y + coordinates.start[1]);
          await page.mouse.down();
          await page.mouse.move(rect.x + coordinates.end[0], rect.y + coordinates.end[1], { steps: 12 });
          await page.mouse.up();
          assert(await frame.evaluate(() => graph.state.x) < 0, 'Dragging must update the controlled x');
        } else if (name === 'gradient-descent') {
          for (const start of [-3.5, 3.5]) {
            await frame.evaluate(value => graph.set('start', value), start);
            assert.equal(await frame.evaluate(() => graph.point.X()), start);
            assert.equal(await frame.evaluate(() => graph.point.Y()), 6.125);
          }
          await frame.locator('#reset').click();
          await frame.evaluate(() => graph.set('eta', 1.2));
          await frame.locator('#step').click();
          assert(Math.abs(await frame.evaluate(() => graph.point.X()) + 0.6) < 1e-9);
          assert(Math.abs(await frame.evaluate(() => graph.point.Y()) - 0.18) < 1e-9);
          await frame.evaluate(() => graph.set('eta', 2));
          await frame.locator('#step').click();
          assert.equal(await frame.evaluate(() => graph.point.X()), -3);
          await frame.locator('#step').click();
          assert.equal(await frame.evaluate(() => graph.point.X()), 3);
          await frame.evaluate(() => graph.set('eta', 0));
          await frame.locator('#step').click();
          assert.equal(await frame.evaluate(() => graph.point.X()), 3);
          await frame.evaluate(() => graph.set('eta', 1.2));
          await frame.locator('#step').click();
        } else {
          for (const a of [5, 12, 11]) {
            await frame.evaluate(value => graph.set('a', value), a);
            const equilibrium = await frame.evaluate(() => [graph.point.X(), graph.point.Y()]);
            assert(Math.abs(equilibrium[0] - (a - 2) / 1.5) < 1e-9);
            assert(Math.abs(equilibrium[1] - (2 + 0.5 * equilibrium[0])) < 1e-9);
          }
        }
        await inspect(frame, name, width);
        if (width === 1200 || width === 390) {
          await iframe.screenshot({ path: path.join(config.screenshots, `${name}-${width}-changed.png`) });
        }
        if (name === 'derivative' && width === 1200) {
          await frame.locator('button[data-view="model"]').click();
          const beforeResize = await frame.evaluate(() => ({ ...window.graph.state }));
          for (const resized of [390, 1200]) {
            await page.setViewportSize({ width: resized, height: 1000 });
            await frame.waitForFunction(() => document.querySelector('.sim-panes').dataset.view === 'model');
            assert.deepEqual(await frame.evaluate(() => ({ ...window.graph.state })), beforeResize,
              'A viewport change must preserve the learner-selected view and graph state');
          }
        }
        await frame.locator('button[data-view="controls"]').click();
        await frame.locator('#reset').click();
        const reset = await frame.evaluate(() => ({ ...graph.state }));
        assert.deepEqual(reset, name === 'gradient-descent' ? { eta: 0.4, start: 3 } :
          name === 'supply-demand' ? { a: 8 } : { x: 1 });
        if (name === 'gradient-descent') assert.equal(await frame.evaluate(() => graph.history.length), 1);
      }
    }
    assert.deepEqual(errors, [], `Browser errors: ${errors.join('; ')}`);
    assert.deepEqual(external, [], `External requests: ${external.join('; ')}`);
    console.log('Verified four palettes and three models in course iframes at 1200, 768, 390, and 320px; numerical cases, keyboard, dragging, reset, and offline loading passed.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
