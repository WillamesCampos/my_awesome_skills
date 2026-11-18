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

console.log("schema tests passed");

