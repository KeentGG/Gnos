/* Run with Node and Playwright available on NODE_PATH; uses an installed Chrome.
   Checks delivered sandboxed HTML, not editor state. No learner data is read. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const escape=s=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
const viewerCSS=fs.readFileSync(path.join(root,'skills/course-viewer/references/example.html'),'utf8').match(/<style>([\s\S]*?)<\/style>/)[1];
const palettes={luxe:['#322d29','#72383d','#ac9c8d','#d1c7bd','#d9d9d9','#efe9e1'],wine:['#ede7c7','#8b0000','#5b0202','#200e01'],forest:['#445d48','#fde5d4','#d6cc99','#001524','#5e3023'],blue:['#0274bd','#e9e6dd','#c4ad9d','#000000','#f57251']};
(async()=>{
 const browser=await chromium.launch({channel:process.env.GNOS_BROWSER_CHANNEL||'chrome'});
 const page=await browser.newPage({reducedMotion:'reduce'});
 await page.emulateMedia({reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 async function load(file,width){
  await page.setViewportSize({width,height:900});
  const html=fs.readFileSync(file,'utf8');
  await page.setContent(`<style>${viewerCSS}body{margin:0}.media{margin:0;border:0;border-radius:0}</style><div class="media"><iframe class="simulation-frame" style="--simulation-max-height:800px" sandbox="allow-scripts" srcdoc="${escape(html)}"></iframe></div>`);
  const frame=page.frames()[1];await frame.waitForLoadState();await frame.locator('.sim-shell').waitFor();
  assert.equal(await page.locator('iframe').evaluate(e=>e.getBoundingClientRect().height),800);
  return frame;
 }
 async function fits(frame,label){
  // Wait for the model's debounced canvas resize to finish.
  await frame.waitForTimeout(label.startsWith('S06/')?160:30);
  const data=await frame.evaluate(()=>{
   const d=document.documentElement,footer=document.querySelector('.sim-footer').getBoundingClientRect();
   return {w:innerWidth,h:innerHeight,sw:d.scrollWidth,sh:d.scrollHeight,
    panes:[...document.querySelectorAll('.sim-pane:not([hidden])')].map(e=>({name:e.dataset.pane,bottom:e.getBoundingClientRect().bottom,scroll:e.scrollHeight,client:e.clientHeight})),
    controls:[...document.querySelectorAll('.sim-pane:not([hidden]) input,.sim-pane:not([hidden]) button')].map(e=>{const r=e.getBoundingClientRect();return {id:e.id,left:r.left,right:r.right,top:r.top,bottom:r.bottom}}),footer:footer.top};
  });
  assert.ok(data.sw<=data.w&&data.sh<=data.h,`${label}: document overflow ${JSON.stringify(data)}`);
  for(const p of data.panes) assert.ok(p.bottom<=data.footer-4&&p.scroll<=p.client+1,`${label}: pane overlaps footer or scrolls ${JSON.stringify(data)}`);
  for(const c of data.controls) assert.ok(c.left>=0&&c.right<=data.w&&c.top>=0&&c.bottom<=data.footer,`${label}: control clipped ${JSON.stringify(c)}`);
 }
 async function view(f,v){await f.locator(`.sim-nav button[data-view="${v}"]`).click()}
 async function set(f,id,value){await f.locator('#'+id).evaluate((e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))},String(value))}
 const layoutChecks=[];
 for(const width of [1200,768,390,320])for(let i=1;i<=10;i++){
  const id='S'+String(i).padStart(2,'0');const f=await load(path.join(root,`tests/visual-levels/${id}/sim.html`),width);
  for(const v of width>=1000?['both','controls','result','model']:['controls','result','model']){await view(f,v);await fits(f,`${id}/${width}/${v}`);layoutChecks.push(`${id}/${width}/${v}`)}
  await view(f,'controls');
  const ranges=await f.locator('input[type="range"]').evaluateAll(es=>es.map(e=>({id:e.id,min:e.min,max:e.max,value:e.value})));
  for(const end of ['min','max']){
   for(const r of ranges)await set(f,r.id,r[end]);
   if(id==='S09'){await f.locator('#pred').fill('A larger limit may recover more failures and use more attempts.');await f.locator('#runBtn').click()}
   if(id==='S03'){await f.locator('#btnReset').click();for(let j=0;j<3;j++)await f.locator('#btnNext').click()}
   if(id==='S07')await f.locator('#runBtn').click();
   for(const v of ['controls','result','model']){await view(f,v);await fits(f,`${id}/${width}/${end}/${v}`)}
   await view(f,'controls');
  }
  if(width===390&&['S03','S09','S10'].includes(id)){await view(f,'result');await page.screenshot({path:`/tmp/gnos-${id}-390-verified.png`})}
 }
 // Model assertions exercise the relationships, reset, and keyboard operation.
 let f=await load(path.join(root,'tests/visual-levels/S01/sim.html'),390);
 await set(f,'slopeSlider',-2);assert.equal(await f.locator('#signValue').textContent(),'negative');
 await view(f,'result');await view(f,'controls');assert.equal(await f.locator('#slopeSlider').inputValue(),'-2');
 await f.locator('#resetBtn').click();assert.equal(await f.locator('#slopeSlider').inputValue(),'2');
 await f.locator('#slopeSlider').focus();await page.keyboard.press('ArrowRight');assert.ok(Number(await f.locator('#slopeSlider').inputValue())>2);
 f=await load(path.join(root,'tests/visual-levels/S02/sim.html'),390);await set(f,'length',2);assert.equal(await f.locator('#period').textContent(),'2.84');
 await f.locator('#resetBtn').click();assert.equal(await f.locator('#period').textContent(),'2.01');
 await f.waitForTimeout(50);const frozen=await f.locator('canvas').evaluate(e=>e.toDataURL());await f.waitForTimeout(100);assert.equal(await f.locator('canvas').evaluate(e=>e.toDataURL()),frozen,'S02 ignores reduced motion');
 f=await load(path.join(root,'tests/visual-levels/S03/sim.html'),390);await f.locator('#btnNext').click();assert.match(await f.locator('#queueBox').textContent(),/B, C/);assert.match(await f.locator('#visitedBox').textContent(),/A/);await f.locator('#btnReset').click();assert.match(await f.locator('#queueBox').textContent(),/\[A\]/);
 f=await load(path.join(root,'tests/visual-levels/S04/sim.html'),390);await set(f,'threshold',1);assert.equal(await f.locator('#countAbove').textContent(),'0 / 100');assert.equal(await f.locator('#fracExpected').textContent(),'0.00');await set(f,'threshold',0);assert.equal(await f.locator('#countAbove').textContent(),'100 / 100');
 f=await load(path.join(root,'tests/visual-levels/S05/sim.html'),390);await set(f,'angle',30);const range30=Number(await f.locator('#rangeval').textContent());await set(f,'angle',60);assert.ok(Math.abs(Number(await f.locator('#rangeval').textContent())-range30)<.02);await set(f,'angle',45);assert.ok(Number(await f.locator('#rangeval').textContent())>range30);
 f=await load(path.join(root,'tests/visual-levels/S06/sim.html'),390);await f.waitForTimeout(100);const stillT=await f.locator('#tOut').textContent();await f.waitForTimeout(100);assert.equal(await f.locator('#tOut').textContent(),stillT,'S06 ignores reduced motion');assert.equal(await f.locator('#playBtn').textContent(),'Play');await set(f,'kSlider',1500);assert.equal(await f.locator('#kOut').textContent(),'1500');await f.locator('#resetBtn').click();assert.equal(await f.locator('#kOut').textContent(),'1000');await f.locator('#playBtn').click();await f.waitForFunction(()=>Number(document.getElementById('tOut').textContent)>0);await f.locator('#playBtn').click();const pausedT=await f.locator('#tOut').textContent();await f.waitForTimeout(100);assert.equal(await f.locator('#tOut').textContent(),pausedT);
 f=await load(path.join(root,'tests/visual-levels/S07/sim.html'),390);await f.locator('#runBtn').click();const mean=await f.locator('#meanOut').textContent();await f.locator('#resetBtn').click();await f.locator('#runBtn').click();assert.equal(await f.locator('#meanOut').textContent(),mean);assert.equal(await f.locator('#nOut').textContent(),'100');
 f=await load(path.join(root,'tests/visual-levels/S08/sim.html'),390);assert.equal(await f.locator('#xval').textContent(),'1.00','S08 ignores reduced motion');await f.locator('#pause').click();await f.waitForFunction(()=>document.getElementById('xval').textContent!=='1.00');await f.locator('#reset').click();assert.equal(await f.locator('#xval').textContent(),'1.00');
 f=await load(path.join(root,'tests/visual-levels/S09/sim.html'),390);await set(f,'thr',0);await f.locator('#runBtn').click();assert.equal(await f.locator('#att').textContent(),'20');const rate=await f.locator('#rate').textContent();await f.locator('#resetBtn').click();await f.locator('#runBtn').click();assert.equal(await f.locator('#rate').textContent(),rate);
 f=await load(path.join(root,'tests/visual-levels/S10/sim.html'),390);await set(f,'coolant',0);await set(f,'feed',10);assert.equal(await f.locator('#tVal').textContent(),'400.0');assert.equal(await f.locator('#cVal').textContent(),'2.50');await view(f,'result');assert.ok(await f.locator('#alarmBanner').isVisible());await fits(f,'S10/longest-alarm');await view(f,'controls');await f.locator('#resetBtn').click();assert.equal(await f.locator('#tVal').textContent(),'230.0');assert.equal(await f.locator('#cVal').textContent(),'1.00');
 // Every preset uses only its approved colors, and the reusable shell resets.
 for(const preset of Object.keys(palettes)){
  const file=path.join(root,'skills/lesson-design/templates/simulation.html');f=await load(file,320);
  await f.evaluate(p=>document.documentElement.dataset.palette=p,preset);
  const colors=await f.evaluate(()=>{const s=getComputedStyle(document.documentElement);return ['surface','ink','muted','primary','soft','line','secondary'].map(n=>s.getPropertyValue('--'+n).trim().toLowerCase())});
  for(const color of colors)assert.ok(palettes[preset].includes(color),`${preset}: unexpected ${color}`);
  await set(f,'slope',-3);await view(f,'result');await fits(f,`template/${preset}`);await page.screenshot({path:`/tmp/gnos-palette-${preset}.png`});await view(f,'controls');await f.locator('#reset').click();assert.equal(await f.locator('#slope').inputValue(),'2');
 }
 assert.deepEqual(errors,[],'Browser script failures');
 console.log(`Passed ${layoutChecks.length} initial view checks, 240 input-extreme view checks, 10 model/interaction checks, and 4 palette/reset checks.`);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
