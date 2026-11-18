import assert from "node:assert/strict";
import {DEFAULT_POST_DATA, parsePostVisualData} from "./schema.ts";

const parsed = parsePostVisualData(DEFAULT_POST_DATA);
assert.equal(parsed.headline, DEFAULT_POST_DATA.headline);
assert.equal(parsed.nodes.length, 3);

assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, headline: ""}),
  /headline/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, nodes: ["um"]}),
  /nodes/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, durationSeconds: 20}),
  /durationSeconds/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, headline: "x".repeat(91)}),
  /headline/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, nodes: ["x".repeat(25), "ok"]}),
  /nodes\[0\]/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, series: "x".repeat(25)}),
  /series/,
);
assert.throws(
  () => parsePostVisualData({...DEFAULT_POST_DATA, footer: "x".repeat(49)}),
  /footer/,
);

console.log("schema tests passed");
