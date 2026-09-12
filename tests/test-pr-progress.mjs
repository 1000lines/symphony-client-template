import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { markers, prUrl, refreshBody, renderMermaid, renderProgress, stateClass } from "../template/scripts/symphony/render-pr-progress.mjs";
import { fetchProgress, loadPlan, progressQuery } from "../template/scripts/symphony/fetch-pr-progress.mjs";

const url = (number) => `https://github.com/example/client/pull/${number}`;
const graph = {
  direction: "LR",
  nodes: [
    { id: "A", label: "100-49: Review — #43 — App checkpoint merged; provider pending" },
    { id: "B", label: "100-53: Integration — #48 — Checkpoint merged; three callers pending" },
    { id: "C", label: "100-61 — Generate progress" },
  ],
  edges: [{ from: "A", to: "C" }, { from: "B", to: "C" }],
};
const fixture = () => ({ graph: structuredClone(graph), states: { A: "Done", B: "Done", C: "Active" },
  prs: { A: [url(49)], B: [url(53)], C: [url(61)] }, currentNode: "C", snapshotTime: "2026-09-12T03:00:00Z" });
const plan = { graph, manifest: { nodes: graph.nodes.map((node, index) => ({
  id: node.id, existingIssue: ["100-49", "100-53", "100-61"][index],
  pr: { url: null, base: "main" },
})) } };
const response = () => ({ data: Object.fromEntries(plan.manifest.nodes.map((node, i) => [`n${i}`, {
  identifier: node.existingIssue, state: { name: i < 2 ? "Done" : "Active" },
  attachments: { nodes: [{ url: url([49, 53, 61][i]) }], pageInfo: { hasNextPage: false } },
}])) });
const readPr = async (link) => ({ url: link, title: `[100-${link.split("/").at(-1)}]: Change`,
  headRefName: "task", headRefOid: "a".repeat(40), baseRefName: "main", state: "OPEN", mergedAt: null });

test("#49 regression: pending prose keeps both Done nodes green, topology and links intact", () => {
  const snapshot = fixture();
  const before = structuredClone(snapshot);
  const result = renderMermaid(snapshot);
  assert.match(result, /A\[".*provider pending.*Done.*"\]:::completed/);
  assert.match(result, /B\[".*callers pending.*Done.*"\]:::completed/);
  assert.match(result, /C\[".*Current PR"\]:::inProgress/);
  assert.deepEqual([...result.matchAll(/^  (\w+) --> (\w+)$/gm)].map((m) => ({ from: m[1], to: m[2] })), graph.edges);
  assert.deepEqual([...result.matchAll(/^  (\w+)\[/gm)].map((m) => m[1]), ["A", "B", "C"]);
  assert.match(result, /click A href "https:\/\/github.com\/example\/client\/pull\/49"/);
  assert.equal(renderMermaid(snapshot), result);
  assert.deepEqual(snapshot, before);
});

for (const [expected, states] of Object.entries({
  completed: ["Done", " done "], inProgress: ["Active", "Evaluating", "In Progress", "Rework"],
  waiting: ["Inactive", "Unhappy", "Waiting for CI", "In Review", "Human Input Needed", "Blocked"],
  neutral: ["Backlog", "Todo", "Canceled", "Cancelled", "Duplicate", "Unknown", "Custom state", "", null],
})) {
  test(`all ${expected} states retain the independent purple current outline`, () => {
    for (const state of states) {
      const snapshot = fixture();
      snapshot.states.C = state;
      assert.equal(stateClass(state), expected);
      const output = renderMermaid(snapshot);
      assert.match(output, new RegExp(`C\\[".*Current PR"\\]:::${expected}`));
      assert.match(output, /style C stroke:#8250df,stroke-width:4px/);
      assert.doesNotMatch(output, /classDef .*stroke/);
    }
  });
}

test("hostile labels and URLs cannot add Mermaid or HTML instructions", () => {
  const snapshot = fixture();
  snapshot.graph.nodes[0].label = 'quote"\nX --> Y <script> & #quot; `code` \\ [a] ${noShell}';
  snapshot.prs.A = ['javascript:alert(1)', 'https://github.com/example/client/pull/1"\nclick C call bad()',
    'https://github.com@evil.test/example/client/pull/1', 'https://github.com/example/client/pull/1?x="'];
  const text = renderMermaid(snapshot);
  assert.equal(text.split("\n").filter((line) => line.includes("A[")).length, 1);
  assert.match(text, /#34; X --#62; Y #60;script#62;/);
  assert.doesNotMatch(text, /<script>|click A|call bad|javascript:/);
  assert.match(text, /A\[".*no PR yet/);
  assert.equal(prUrl(url(1) + "/"), url(1));
  assert.equal(prUrl("https://evil.test/pull/1"), null);
});

test("either undersized threshold omits diagrams, with no fabricated topology", () => {
  for (const [nodes, edges] of [[graph.nodes.slice(0, 1), []], [graph.nodes.slice(0, 2), [{ from: "A", to: "B" }]], [graph.nodes, graph.edges.slice(0, 1)]]) {
    const snapshot = { ...fixture(), graph: { direction: "LR", nodes, edges }, currentNode: "A" };
    assert.equal(renderMermaid(snapshot), "");
    assert.doesNotMatch(renderProgress(snapshot), /```mermaid/);
  }
  for (const edit of [
    (s) => s.graph.nodes.push(s.graph.nodes[0]),
    (s) => s.graph.nodes[0].id = 'A; click A call bad()',
    (s) => s.graph.edges.push(s.graph.edges[0]),
    (s) => s.graph.edges[0].to = "MISSING",
    (s) => s.currentNode = "MISSING",
  ]) {
    const snapshot = fixture(); edit(snapshot);
    assert.throws(() => renderMermaid(snapshot), /Invalid progress/);
  }
});

test("failed state and PR lookups are explicit; attachment errors preserve known Done", async () => {
  const data = response();
  data.data.n0.attachments.pageInfo.hasNextPage = true;
  data.errors = [{ path: ["n0", "attachments"], message: "Failure" }, { path: ["n1", "state"], message: "Failure" }];
  const snapshot = await fetchProgress(plan, data, { currentNode: "C", readPr: async () => { throw Error("private error"); } });
  assert.deepEqual(snapshot.states, { A: "Done", B: "Unknown", C: "Active" });
  assert.deepEqual(snapshot.prs, { A: [], B: [], C: [] });
  assert.match(renderProgress(snapshot), /attachments incomplete/);
  assert.doesNotMatch(renderProgress(snapshot), /private error/);
  const failed = await fetchProgress(plan, { errors: [{ message: "unavailable" }] }, { currentNode: "C", readPr });
  assert.deepEqual(Object.values(failed.states), ["Unknown", "Unknown", "Unknown"]);
});

test("read-only request uses commissioned identities and safe GraphQL strings", () => {
  const unresolved = structuredClone(plan);
  unresolved.manifest.nodes[0].existingIssue = null;
  unresolved.manifest.nodes[0].payloadKey = "TE-A";
  assert.doesNotMatch(progressQuery(unresolved), /n0:/);
  assert.match(progressQuery(unresolved, { A: '100-1"\n} mutation {' }), /100-1\\"\\n} mutation/);
  assert.match(progressQuery(unresolved, { A: "100-49" }), /n0: issue\(id: "100-49"\)/);
  assert.match(progressQuery(plan), /^query PrProgress/);
});

test("creation and refresh verify real links and reject wrong issue/base/URL", async () => {
  const data = response(); data.data.n2.attachments.nodes = [];
  const first = await fetchProgress(plan, data, { currentNode: "C", readPr });
  assert.match(renderMermaid(first), /C\[".*no PR yet.*Current PR/);
  const next = await fetchProgress(plan, data, { currentNode: "C", currentPr: url(61), readPr });
  assert.deepEqual(next.prs.C, [url(61)]);
  for (const patch of [{ baseRefName: "other" }, { title: "Unrelated" }, { url: url(999) }]) {
    const bad = await fetchProgress(plan, data, { currentNode: "C", currentPr: url(61), readPr: async (link) => ({ ...await readPr(link), ...patch }) });
    assert.deepEqual(bad.prs.C, []);
  }
  await assert.rejects(fetchProgress(plan, data, { currentNode: "C", currentPr: "javascript:bad()" }));
});

test("multiple verified PRs deduplicate with the current link first", async () => {
  const data = response(); data.data.n2.attachments.nodes.push({ url: url(62) }, { url: url(61) });
  const snapshot = await fetchProgress(plan, data, { currentNode: "C", currentPr: url(62), readPr: async (link) => ({ ...await readPr(link), title: "[100-61]: Change" }) });
  assert.deepEqual(snapshot.prs.C, [url(62), url(61)]);
  assert.match(renderMermaid(snapshot), /click C href ".*\/62"/);
  assert.match(renderProgress(snapshot), /C: \[PR #62\].*\[PR #61\]/);
});

test("body refresh is idempotent, retains surrounding prose, and rejects ambiguous markers", () => {
  const body = `Context\n${markers[0]}\nold snapshot\n${markers[1]}\nSummary: pending artifacts.\n`;
  const updated = refreshBody(body, fixture());
  assert.equal(refreshBody(updated, fixture()), updated);
  assert.match(updated, /^Context\n/);
  assert.match(updated, /\nSummary: pending artifacts\.\n$/);
  for (const bad of ["no markers", markers[1] + markers[0], body + markers[0]]) assert.throws(() => refreshBody(bad, fixture()));
});

test("CLI renders offline and loader calls only the installed shared parser export", async () => {
  const root = mkdtempSync(join(tmpdir(), "pr-progress-"));
  try {
    const snapshot = join(root, "snapshot.json"); writeFileSync(snapshot, JSON.stringify(fixture()));
    const script = fileURLToPath(new URL("../template/scripts/symphony/render-pr-progress.mjs", import.meta.url));
    assert.equal(execFileSync(process.execPath, [script, snapshot], { encoding: "utf8" }), renderProgress(fixture()));
    assert.notEqual(spawnSync(process.execPath, [script]).status, 0);
    await assert.rejects(loadPlan(snapshot, join(root, "missing")), /Cannot find module/);
    // A transport fixture verifies the import/call boundary; it is not a second plan parser.
    const dist = join(root, "tools/symphony-dag/dist"); mkdirSync(dist, { recursive: true });
    writeFileSync(join(dist, "projectManifest.js"), 'exports.parseProjectPlan = text => ({ sharedParserInput: text });');
    assert.deepEqual(await loadPlan(snapshot, root), { sharedParserInput: readFileSync(snapshot, "utf8") });
  } finally { rmSync(root, { recursive: true, force: true }); }
});
