// Run from any directory with Node.js 18 or later. The UI and canvas are test doubles.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
assert.equal(new Set(ids).size, ids.length, 'HTML ids must be unique');
const noop = () => {};
const canvas = new Proxy({
  measureText: text => ({ width: text.length * 8 }),
  createLinearGradient: () => ({ addColorStop: noop })
}, { get: (target, name) => target[name] ?? noop });

function element() {
  return {
    value: '', selectedIndex: 0, style: {}, clientWidth: 800,
    addEventListener: noop, setAttribute: noop, setPointerCapture: noop,
    getContext: kind => kind === '2d' ? canvas : null
  };
}
const nodes = Object.fromEntries(ids.map(id => [id, element()]));
nodes.reading.value = 'ALERT';
const context = vm.createContext({
  assert, console, performance, requestAnimationFrame: () => 1, cancelAnimationFrame: noop,
  document: { getElementById: id => nodes[id], createElement: element }, window: element()
});
vm.runInContext(html.match(/<script>([\s\S]+?)<\/script>/)[1], context);

function checkDeliveries() {
  let runs = 0;
  for (let district = 0; district < levels.length; district++) {
    for (const signal of ['ALERT', 'CLEAR']) {
      for (const strategy of [0, 1]) {
        for (const manual of [false, true]) {
          $('reading').value = signal;
          $('routeMode').selectedIndex = strategy;
          configureLevel(district);
          paintCampus(performance.now());
          for (let n = 0; !ended && n < 70; n++) {
            assert(plan.path.length >= 2, 'A reachable goal must have a next step');
            const next = plan.path[1];
            if (manual) drive(next.x - robot.x, next.y - robot.y);
            else $('dispatch').onclick();
            assert.equal(campusMap[robot.y][robot.x], 0);
          }
          assert(ended, 'Delivery should finish');
          assert.deepEqual(robot, lab);
          if (district === 0) {
            const expectedTurns = signal === 'CLEAR' ? 4 : strategy === 0 ? 6 : 5;
            assert.equal(turns, expectedTurns);
          }
          $('nextLevel').onclick();
          assert.equal(levelIndex, (district + 1) % levels.length);
          runs++;
        }
      }
    }
  }
  console.log(runs + ' delivery scenarios passed');
}

function checkTerrain() {
  configureLevel(1);
  robot = {x: 2, y: 0};
  drive(1, 0);
  assert.equal(turns, 2, 'Grate entry takes two turns');
  configureLevel(2);
  robot = {x: 0, y: 3};
  drive(0, 1);
  assert.equal(turns, 0);
  assert.equal(robot.y, 3, 'Deep water blocks movement');
  robot = {x: 2, y: 1};
  drive(1, 0);
  assert.equal(turns, 2, 'Shallow water takes two turns');
  configureLevel(3);
  robot = {x: 4, y: 4};
  drive(0, -1);
  assert.equal(waits, 1);
  assert.equal(robot.y, 4, 'Red crossing keeps the rover in place');
  drive(0, -1);
  assert.equal(robot.y, 3);
  console.log('Terrain and rail crossing checks passed');
}
for (const check of [checkDeliveries, checkTerrain]) {
  vm.runInContext('(' + check.toString() + ')()', context);
}

