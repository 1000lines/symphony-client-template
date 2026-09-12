import assert from "node:assert/strict";
import test from "node:test";
import { reviewSetup, verifyServices, verifyInstallation, verifyEnvironment } from "../template/.agents/skills/cadence-onboarding/scripts/check-credentials.mjs";

const settings = {
  CADENCE_APP_PRIVATE_KEY: "synthetic-app-key",
  CADENCE_LINEAR_API_TOKEN: "synthetic-linear-key",
  CADENCE_APP_ID: "123", CADENCE_REVIEWER: "review-app[bot]",
  SYMPHONY_BOT_USER: "author-app[bot]",
  CADENCE_CODEX_MODEL: "test-codex-model", CADENCE_CLAUDE_MODEL: "claude-opus-5",
  LINEAR_TEAM_KEY: "100",
};

test("environment admission requires only the default branch before any credential probes", async () => {
  const target = { owner: "owner", repo: "client", defaultBranch: "release/main" };
  const policy = { custom_branch_policies: true, protected_branches: false };
  const branch = { name: target.defaultBranch, type: "branch" };
  const github = (deployment_branch_policy, rules) => ({
    request: async () => ({ data: { deployment_branch_policy } }),
    paginate: async () => rules,
  });
  await verifyEnvironment(github(policy, [branch]), target);
  for (const invalid of [null, {}, { custom_branch_policies: false, protected_branches: true }]) {
    await assert.rejects(() => verifyEnvironment(github(invalid, []), target), /Selected branches and tags/);
  }
  for (const rules of [[], [branch, { name: "feature/*", type: "branch" }],
    [{ ...branch, type: "tag" }], [{ ...branch, name: "main" }],
    [{ ...branch, name: "*" }], [{ name: target.defaultBranch }]]) {
    await assert.rejects(() => verifyEnvironment(github(policy, rules), target), /exactly one branch rule/);
  }
  for (const method of ["request", "paginate"]) {
    const api = github(policy, [branch]);
    api[method] = async () => { throw Object.assign(new Error("private response body"), { status: 403 }); };
    await assert.rejects(() => verifyEnvironment(api, target),
      error => /HTTP 403/.test(error.message) && !error.message.includes("private response"));
  }
});

test("the minted App must match the configured identity and single target installation", () => {
  const expected = { appSlug: "review-app", reviewer: "review-app[bot]", repository: "owner/client" };
  const target = { total_count: 1, repositories: [{ full_name: "owner/client" }] };
  verifyInstallation(expected, target);
  for (const changed of [{ appSlug: "" }, { appSlug: "another-app" }, { reviewer: "author-app[bot]" }]) {
    assert.throws(() => verifyInstallation({ ...expected, ...changed }, target), /does not match/);
  }
  for (const changed of [
    { total_count: 0, repositories: [] }, { total_count: 2, repositories: target.repositories },
    { total_count: 1, repositories: [{ full_name: "owner/other" }] },
  ]) assert.throws(() => verifyInstallation(expected, changed), /exactly the target/);
});

for (const [openai, anthropic, expected] of [
  [true, false, "codex"], [false, true, "claude"], [true, true, "codex"],
  [false, false, undefined],
]) {
  test(`provider selection: OpenAI=${openai}, Anthropic=${anthropic}`, async () => {
    const env = { ...settings, CADENCE_OPENAI_API_KEY: openai ? "synthetic-openai-key" : "",
      CADENCE_AI_REVIEW_ANTHROPIC_API_KEY: anthropic ? "synthetic-anthropic-key" : "" };
    const calls = [];
    const fetch = async (url, options) => {
      calls.push({ url, options });
      return { ok: true, json: async () => ({ data: { viewer: { id: "viewer" }, teams: { nodes: [{ key: "100" }] } } }) };
    };
    if (!expected) {
      await assert.rejects(() => verifyServices(env, fetch), /Neither provider key reached/);
      assert.equal(calls.length, 0);
      return;
    }
    const result = await verifyServices(env, fetch);
    assert.equal(result.provider, expected);
    assert.equal(calls.length, 2);
    assert.equal(calls[0].url, "https://api.linear.app/graphql");
    assert.equal(calls[0].options.headers.authorization, env.CADENCE_LINEAR_API_TOKEN);
    assert.match(calls[1].url, expected === "codex" ? /api.openai.com/ : /api.anthropic.com/);
    assert.equal(calls[1].options.headers[expected === "codex" ? "authorization" : "x-api-key"],
      expected === "codex" ? `Bearer ${env.CADENCE_OPENAI_API_KEY}` : env.CADENCE_AI_REVIEW_ANTHROPIC_API_KEY);
    assert.doesNotMatch(JSON.stringify(result), /synthetic-.*-key/);
  });
}

test("missing settings, mismatched identities and invalid model fail before requests", async () => {
  const valid = { ...settings, CADENCE_OPENAI_API_KEY: "synthetic-openai-key" };
  for (const name of Object.keys(settings).filter(key => !["CADENCE_CLAUDE_MODEL", "CADENCE_CODEX_MODEL"].includes(key))) {
    await assert.rejects(() => verifyServices({ ...valid, [name]: "" }, () => assert.fail("must fail before network")), new RegExp(name));
  }
  for (const changed of [
    { CADENCE_APP_ID: "review-app" }, { CADENCE_APP_ID: "0" },
    { CADENCE_REVIEWER: "review-app" }, { CADENCE_REVIEWER: valid.SYMPHONY_BOT_USER },
    { SYMPHONY_BOT_USER: "example-author[bot]" }, { CADENCE_CODEX_MODEL: "model\nINJECT=value" },
    { CADENCE_OPENAI_API_KEY: "", CADENCE_AI_REVIEW_ANTHROPIC_API_KEY: "fixture", CADENCE_CLAUDE_MODEL: "unapproved" },
  ]) assert.throws(() => reviewSetup({ ...valid, ...changed }));
});

test("invalid selected key never falls back or echoes service bodies/secrets", async () => {
  const env = { ...settings, CADENCE_OPENAI_API_KEY: "synthetic-openai-key",
    CADENCE_AI_REVIEW_ANTHROPIC_API_KEY: "synthetic-anthropic-key" };
  const calls = [];
  await assert.rejects(() => verifyServices(env, async url => {
    calls.push(url);
    return url.includes("linear")
      ? { ok: true, json: async () => ({ data: { viewer: { id: "viewer" }, teams: { nodes: [{ key: "100" }] } } }) }
      : { ok: false, status: 401, json: () => assert.fail("must not log service body") };
  }), error => /CADENCE_OPENAI_API_KEY.*HTTP 401/.test(error.message) && !error.message.includes("synthetic"));
  assert.equal(calls.length, 2);
  assert.ok(calls.every(url => !url.includes("anthropic")));
  await assert.rejects(() => verifyServices(env, async () => { throw new Error(env.CADENCE_OPENAI_API_KEY); }),
    error => !error.message.includes(env.CADENCE_OPENAI_API_KEY));
  await assert.rejects(() => verifyServices(env, async () => ({ ok: true, json: async () => ({ errors: [{ message: env.CADENCE_LINEAR_API_TOKEN }] }) })),
    error => /cannot read Linear/.test(error.message) && !error.message.includes(env.CADENCE_LINEAR_API_TOKEN));
  await assert.rejects(() => verifyServices(env, async () => ({ ok: true, json: async () => ({ data: { viewer: { id: "viewer" }, teams: { nodes: [{ key: "OTHER" }] } } }) })), /cannot access the target/);
});

test("Codex default model authenticates without claiming inference or model readiness", async () => {
  const env = { ...settings, CADENCE_OPENAI_API_KEY: "synthetic-key", CADENCE_CODEX_MODEL: "" };
  const urls = [];
  const result = await verifyServices(env, async url => {
    urls.push(url);
    return { ok: true, json: async () => ({ data: { viewer: { id: "viewer" }, teams: { nodes: [{ key: "100" }] } } }) };
  });
  assert.equal(result.provider, "codex");
  assert.equal(result.model, undefined);
  assert.equal(urls[1], "https://api.openai.com/v1/models");
  assert.deepEqual(Object.keys(result).sort(), ["model", "provider"]);
});
