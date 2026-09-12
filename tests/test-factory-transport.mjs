// Contract rehearsal only: factory orchestration is human/agent guidance, not a
// shipped automation API. Exercise the real script against loopback fixtures;
// this does not establish live setup or an agent's compliance with the skill.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { mkdtemp, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const script = resolve(
  process.env.FACTORY_CLIENT_ROOT ||
    fileURLToPath(new URL("../template", import.meta.url)),
  ".agents/skills/linear-graphql/scripts/linear-graphql.mjs"
);
const identity = {
  viewer: { id: "viewer", name: "Fixture lead" },
  organization: { id: "workspace", name: "Fixture workspace" },
  teams: { nodes: [{ id: "team", key: "FIX", name: "Fixture team" }] },
};
const preflight = {
  team: {
    states: {
      nodes: [
        { id: "backlog", name: "Backlog" },
        { id: "active", name: "Active" },
      ],
    },
    labels: { nodes: [{ id: "cyan", name: "cyan" }] },
    members: { nodes: [{ id: "viewer" }] },
  },
};
const projectInput = {
  name: "Fixture project",
  teamIds: ["team"],
  color: "#00bcd4",
  content:
    "project-code: fixture\nproject-color: cyan\nrepository: example/fixture\nbase-branch: main\nhuman-lead: Fixture lead\nGoal: contract rehearsal",
};
const titles = [
  "Create requirements & design doc",
  "Plan project - seed ticket",
  "Trigger fan out",
];
const fields = `id title description project { id } team { id } state { id }
  labels { nodes { id } } assignee { id }
  relations { nodes { id type issue { id } relatedIssue { id } } }`;

async function fixture(t, mode, fault = {}) {
  const requests = [],
    issues = [],
    relations = [];
  let project,
    failed = false;
  const handle = ({ query, variables = {} }) => {
    requests.push({ query, variables });
    if (fault.auth) throw new Error("Authentication failed");
    if (query.includes("query Identity"))
      return {
        ...identity,
        organization: fault.workspace
          ? { id: "wrong-workspace" }
          : identity.organization,
      };
    if (query.includes("query Preflight"))
      return fault.label
        ? { team: { ...preflight.team, labels: { nodes: [] } } }
        : preflight;
    if (query.includes("query Readback")) return { projects: { nodes: project ? [{
      ...project, teams: { nodes: project.teamIds.map(id => ({ id })) }, issues: { nodes: issues.map(issue => ({
        id: issue.id, title: issue.title, description: issue.description,
        project: { id: issue.projectId }, team: { id: issue.teamId }, state: { id: issue.stateId },
        labels: { nodes: issue.labelIds.map(id => ({ id })) }, assignee: { id: issue.assigneeId },
        relations: { nodes: relations.filter(r => r.issueId === issue.id).map(r => ({
          id: r.id, type: r.type, issue: { id: fault.direction ? r.relatedIssueId : r.issueId },
          relatedIssue: { id: fault.direction ? r.issueId : r.relatedIssueId },
        })) },
      })) },
    }] : [] } };
    const { input, id } = variables;
    if (query.includes("projectCreate")) {
      assert.equal(project, undefined, "retry must reuse project");
      assert.deepEqual(input, projectInput);
      project = { ...input, id: "project" };
      return { projectCreate: { success: true, project } };
    }
    if (query.includes("issueCreate")) {
      assert.equal(input.stateId, "backlog");
      assert.deepEqual(input.labelIds, ["cyan"]);
      assert.equal(input.assigneeId, "viewer");
      assert.equal(input.teamId, "team");
      assert.equal(input.projectId, "project");
      const issue = { ...input, id: `seed-${issues.length}` };
      issues.push(issue);
      return { issueCreate: { success: true, issue } };
    }
    if (query.includes("issueRelationCreate")) {
      if (fault.partial && relations.length === 1 && !failed) {
        failed = true;
        throw new Error("Relation write interrupted");
      }
      assert.equal(input.type, "blocks");
      assert.equal(input.issueId, `seed-${relations.length}`);
      assert.equal(input.relatedIssueId, `seed-${relations.length + 1}`);
      const issueRelation = { ...input, id: `relation-${relations.length}` };
      relations.push(issueRelation);
      return { issueRelationCreate: { success: true, issueRelation } };
    }
    assert.ok(query.includes("issueUpdate"));
    assert.equal(relations.length, 2, "activation requires both relations");
    Object.assign(
      issues.find((issue) => issue.id === id),
      input
    );
    return { issueUpdate: { success: true } };
  };
  const server = createServer(async (req, res) => {
    assert.equal(req.headers.authorization, "fixture-token");
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      res.end(JSON.stringify({ data: handle(JSON.parse(body)) }));
    } catch (error) {
      res.end(JSON.stringify({ errors: [{ message: error.message }] }));
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(() => new Promise((resolve) => server.close(resolve)));
  const directory = await mkdtemp(join(tmpdir(), "factory-transport-"));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const tokenFile = join(directory, "token");
  await writeFile(tokenFile, "fixture-token\n", { mode: 0o600 });
  let scriptCalls = 0;
  const cli = (body, extra = []) =>
    new Promise((resolve, reject) => {
      scriptCalls++;
      const child = spawn(
        process.execPath,
        [
          script,
          "--variables-json",
          JSON.stringify(body.variables || {}),
          "--no-aws-secret",
          ...(fault.missingAuth
            ? ["--no-token-file"]
            : ["--token-file", tokenFile]),
          ...extra,
        ],
        {
          // No real credentials, AWS settings or personal home/token files inherited.
          env: {
            PATH: process.env.PATH,
            LINEAR_GRAPHQL_URL: `http://127.0.0.1:${server.address().port}`,
          },
          stdio: ["pipe", "pipe", "pipe"],
          timeout: 10000,
        }
      );
      let stdout = "",
        stderr = "";
      child.stdout.on("data", (data) => (stdout += data));
      child.stderr.on("data", (data) => (stderr += data));
      child.on("error", reject);
      child.on("close", (code) =>
        code === 0 ? resolve(JSON.parse(stdout)) : reject(new Error(stderr))
      );
      child.stdin.end(body.query);
    });
  const injected =
    mode === "injected"
      ? async (body) => structuredClone(handle(body))
      : undefined;
  return {
    call: injected || cli,
    cli,
    requests,
    issues,
    relations,
    get scriptCalls() {
      return scriptCalls;
    },
  };
}

// Bounded synthetic rehearsal of SKILL.md's preflight/preview/staging contract.
async function setup(f, { preview = false, hold = false, source = true } = {}) {
  const who = await f.call({
    query:
      "query Identity { viewer { id name } organization { id name } teams { nodes { id key name } } }",
  });
  assert.deepEqual(who, identity, "viewer/workspace/team identity");
  assert.ok(source, "required source unavailable");
  const ready = await f.call({
    query:
      'query Preflight { team(id:"team") { states { nodes { id name } } labels { nodes { id name } } members { nodes { id } } } }',
  });
  assert.deepEqual(ready, preflight, "state/label/assignee preflight");
  const seedInputs = titles.map((title) => ({
    title,
    description: `Rendered template: ${title}`,
    teamId: "team",
    projectId: "project",
    stateId: "backlog",
    labelIds: ["cyan"],
    assigneeId: "viewer",
  }));
  const relationInputs = [0, 1].map((i) => ({
    issueId: `seed-${i}`,
    relatedIssueId: `seed-${i + 1}`,
    type: "blocks",
  }));
  const plan = {
    project: projectInput,
    seeds: seedInputs,
    relations: relationInputs,
  };
  if (preview) return plan;
  // Refresh server state before retrying; confirmed IDs are never discarded.
  const read = async () => {
    const data = await f.call({ query: `query Readback { projects(filter:{name:{eq:"Fixture project"}}) {
      nodes { id name content color teams { nodes { id } } issues { nodes { ${fields} } } } } }` });
    const p = data.projects.nodes[0];
    return { project: p && { id: p.id, name: p.name, content: p.content, color: p.color,
      teamIds: p.teams.nodes.map(t => t.id) }, issues: (p?.issues.nodes || []).map(i => ({
        id: i.id, title: i.title, description: i.description, projectId: i.project.id,
        teamId: i.team.id, stateId: i.state.id, labelIds: i.labels.nodes.map(l => l.id), assigneeId: i.assignee.id,
      })), relations: (p?.issues.nodes || []).flatMap(i => i.relations.nodes.map(r => ({
        id: r.id, type: r.type, issueId: r.issue.id, relatedIssueId: r.relatedIssue.id,
      }))) };
  };
  let saved = await read();
  const mutate = async (name, type, input, selection, id) => {
    const data = await f.call({
      query: `mutation Write($input:${type}!${
        id ? ", $id:String!" : ""
      }) { ${name}(${
        id ? "id:$id, " : ""
      }input:$input) { success ${selection} } }`,
      variables: { input, ...(id ? { id } : {}) },
    });
    assert.equal(data[name].success, true);
    return data[name];
  };
  if (!saved.project)
    await mutate(
      "projectCreate",
      "ProjectCreateInput",
      projectInput,
      "project { id }"
    );
  for (const input of seedInputs) {
    if (!saved.issues.some((issue) => issue.title === input.title))
      await mutate("issueCreate", "IssueCreateInput", input, "issue { id }");
  }
  for (const input of relationInputs) {
    if (
      !saved.relations.some(
        (r) =>
          r.issueId === input.issueId &&
          r.relatedIssueId === input.relatedIssueId
      )
    )
      await mutate(
        "issueRelationCreate",
        "IssueRelationCreateInput",
        input,
        "issueRelation { id }"
      );
  }
  saved = await read();
  assert.deepEqual(saved.project, { ...projectInput, id: "project" });
  assert.deepEqual(
    saved.issues,
    seedInputs.map((input, i) => ({ ...input, id: `seed-${i}` }))
  );
  assert.deepEqual(
    saved.relations,
    relationInputs.map((input, i) => ({ ...input, id: `relation-${i}` }))
  );
  if (!hold)
    for (const issue of saved.issues)
      await mutate(
        "issueUpdate",
        "IssueUpdateInput",
        { stateId: "active" },
        "",
        issue.id
      );
  assert.deepEqual(
    (await read()).issues.map((i) => i.stateId),
    Array(3).fill(hold ? "backlog" : "active")
  );
  return plan;
}

for (const mode of ["injected", "script"]) {
  test(`${mode}: preflight, concrete preview, two blockers and activation`, async (t) => {
    const f = await fixture(t, mode);
    const plan = await setup(f, { preview: true });
    assert.equal(f.requests.length, 2);
    assert.deepEqual(plan.project, projectInput);
    assert.deepEqual(
      plan.seeds.map((s) => s.title),
      titles
    );
    assert.equal(plan.relations.length, 2);
    assert.equal(f.issues.length, 0);
    assert.deepEqual(await setup(f), plan);
    assert.equal(f.issues.length, 3);
    if (mode === "injected")
      assert.equal(
        f.scriptCalls,
        0,
        "available tool wins over configured script"
      );
  });
  for (const fault of ["workspace", "auth", "label", "source"]) {
    test(`${mode}: ${fault} failure stops before writes`, async (t) => {
      const f = await fixture(t, mode, { [fault]: true });
      await assert.rejects(setup(f, { source: fault !== "source" }));
      assert.equal(f.issues.length, 0);
      assert.equal(
        f.requests.filter((r) => r.query.startsWith("mutation")).length,
        0
      );
      if (["workspace", "auth", "source"].includes(fault))
        assert.equal(f.requests.length, 1);
      if (mode === "injected")
        assert.equal(
          f.scriptCalls,
          0,
          "tool auth failure must not trigger fallback"
        );
    });
  }
  test(`${mode}: partial relation failure keeps staged IDs reusable on retry`, async (t) => {
    const f = await fixture(t, mode, { partial: true });
    await assert.rejects(setup(f), /Relation write interrupted/);
    assert.deepEqual(
      f.issues.map((i) => i.stateId),
      ["backlog", "backlog", "backlog"]
    );
    const ids = f.issues.map((i) => i.id);
    await setup(f);
    assert.deepEqual(
      f.issues.map((i) => i.id),
      ids
    );
    assert.equal(
      f.requests.filter((r) => r.query.includes("projectCreate")).length,
      1
    );
    assert.equal(
      f.requests.filter((r) => r.query.includes("issueCreate")).length,
      3
    );
  });
  test(`${mode}: wrong relation direction blocks activation`, async (t) => {
    const f = await fixture(t, mode, { direction: true });
    await assert.rejects(setup(f));
    assert.deepEqual(
      f.issues.map((i) => i.stateId),
      ["backlog", "backlog", "backlog"]
    );
  });
  test(`${mode}: explicit hold retains both relations without activation`, async (t) => {
    const f = await fixture(t, mode);
    await setup(f, { hold: true });
    assert.equal(f.relations.length, 2);
    assert.deepEqual(
      f.issues.map((i) => i.stateId),
      ["backlog", "backlog", "backlog"]
    );
  });
}

test("script: missing auth fails without a network request; dry-run needs no auth", async (t) => {
  const f = await fixture(t, "script", { missingAuth: true });
  await assert.rejects(setup(f), /Set LINEAR_API_KEY/);
  assert.equal(f.requests.length, 0);
  const body = {
    query: 'mutation { projectCreate(input:{name:"Preview"}) { success } }',
    variables: {},
  };
  assert.deepEqual(await f.cli(body, ["--dry-run"]), body);
  assert.equal(f.requests.length, 0);
});
