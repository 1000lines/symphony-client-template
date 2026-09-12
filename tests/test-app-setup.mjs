import test from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPairSync } from 'node:crypto';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, statSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { api, permissions, manifestFor, prepare, complete, validateReadback, verify } from '../template/.github/symphony/setup-app.mjs';

const manifest = role => ({ name: `example-${role}`, url: 'https://github.com/example/widget', public: false,
  default_events: [], default_permissions: { ...permissions[role] } });
const app = { id: 20, slug: 'example-cadence', owner: { login: 'example' }, permissions: permissions.cadence };
const other = { id: 10, slug: 'example-symphony' };
const installation = { id: 30, app_id: 20, account: { login: 'example' }, suspended_at: null,
  repository_selection: 'selected', permissions: permissions.cadence };
const repositories = [{ id: 40, full_name: 'example/widget' }];
const state = () => ({ config: { role: 'cadence', owner: 'example', otherApp: other.slug,
  repositories: ['example/widget'], manifest: manifest('cadence') }, app, otherApp: other });

function fixture(t, overrides = {}) {
  // Outside the package's Git tree, but inside the issue workspace in CI/local.
  const root = mkdtempSync(resolve('../.app-setup-test-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const path = join(root, 'manifest.json');
  writeFileSync(path, JSON.stringify(manifest('cadence')));
  return { owner: 'example', repositories: 'example/widget', role: 'cadence',
    'other-app': other.slug, manifest: path, directory: join(root, 'setup'), ...overrides };
}

const discovery = type => async path => {
  if (path === 'users/example') return { login: 'example', type };
  if (path === 'user') return { login: 'example' };
  if (path === 'repos/example/widget') return repositories[0];
  if (path === 'apps/example-cadence') return app;
  throw new Error(`Unexpected fixture request ${path}`);
};

test('production App API transport uses in-memory Bearer JWT and unauthenticated conversion', async t => {
  const calls = [];
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    calls.push({ url, options });
    return { ok: true, status: 200, json: async () => ({ id: 20 }) };
  });
  await api('app', { token: 'fixture.jwt.signature' });
  await api('app-manifests/fixturecode/conversions', { method: 'POST' });
  assert.equal(calls[0].options.headers.Authorization, 'Bearer fixture.jwt.signature');
  assert.equal(calls[1].options.headers.Authorization, undefined);
  assert.equal(calls[1].options.method, 'POST');
  assert.equal(calls[1].options.redirect, 'error');
});

test('role presets reject missing/excess grants, events and credential-bearing fields', () => {
  for (const role of Object.keys(permissions)) {
    assert.equal(manifestFor(manifest(role), role).name, `example-${role}`);
    const missing = manifest(role);
    delete missing.default_permissions.checks;
    assert.throws(() => manifestFor(missing, role), /permissions/);
    assert.throws(() => manifestFor({ ...manifest(role), pem: 'fixture-secret' }, role), /inert/);
    assert.throws(() => manifestFor({ ...manifest(role), default_events: ['push'] }, role), /empty/);
  }
  assert.throws(() => manifestFor(manifest('cadence'), 'author'), /Role/);
  const excessive = manifest('cadence');
  excessive.default_permissions.contents = 'write';
  assert.throws(() => manifestFor(excessive, 'cadence'), /permissions/);
});

for (const type of ['User', 'Organization']) {
  test(`${type} registration emits native browser POST, and repeats reuse state`, async t => {
    const options = fixture(t);
    const saved = await prepare(options, discovery(type));
    const html = readFileSync(join(options.directory, 'register.html'), 'utf8');
    assert.ok(html.includes(type === 'User' ? 'https://github.com/settings/apps/new' : 'https://github.com/organizations/example/settings/apps/new'));
    assert.ok(html.includes('name="manifest"'));
    assert.ok(html.includes('http://127.0.0.1:8765/callback'));
    assert.equal(statSync(options.directory).mode & 0o777, 0o700);
    const repeated = await prepare(options, () => { throw new Error('Repeat must not call GitHub'); });
    assert.deepEqual(saved, repeated);
    await assert.rejects(prepare({ ...options, name: 'another-app' }, discovery(type)), /different inputs/);
  });
}

test('existing App reuse skips registration and does not require the opposite App to exist yet', async t => {
  const options = fixture(t, { 'existing-app': app.slug });
  const saved = await prepare(options, discovery('Organization'));
  assert.equal(saved.app.id, app.id);
  assert.equal(existsSync(join(options.directory, 'register.html')), false);
  assert.deepEqual(await complete(options.directory, '', null, () => assert.fail('No conversion')), saved);
  await assert.rejects(prepare(fixture(t, { 'existing-app': app.slug, 'other-app': app.slug }), discovery('Organization')), /different Apps/);
});

test('registration rejects wrong personal operator and cross-owner repositories', async t => {
  await assert.rejects(prepare(fixture(t), async path => path === 'user' ? { login: 'someone-else' } : discovery('User')(path)), /signed in as owner/);
  await assert.rejects(prepare(fixture(t, { repositories: 'other/widget' }), discovery('Organization')), /belonging to owner/);
});

test('conversion validates callback state, provisions PEM via stdin and persists only identity', async t => {
  const options = fixture(t);
  const saved = await prepare(options, discovery('Organization'));
  const callback = `http://127.0.0.1:8765/callback?code=fixturecode&state=${saved.nonce}`;
  const pem = '-----BEGIN PRIVATE KEY-----\nsynthetic-test-only\n-----END PRIVATE KEY-----';
  let conversions = 0;
  let handoffs = 0;
  const request = async path => {
    if (path.startsWith('app-manifests/')) { conversions++; return { ...app, pem, client_secret: 'fixture-client-secret', webhook_secret: 'fixture-hook-secret' }; }
    return app;
  };
  await assert.rejects(complete(options.directory, callback.replace(saved.nonce, 'wrong'), ['provision'], request), /state/);
  assert.equal(conversions, 0);
  const done = await complete(options.directory, callback, ['provision', 'cadence'], request, (argv, input) => {
    handoffs++;
    assert.deepEqual(argv, ['provision', 'cadence']);
    assert.equal(input, pem);
  });
  assert.equal(done.keyHandedOff, true);
  const stored = readFileSync(join(options.directory, 'state.json'), 'utf8');
  for (const secret of [pem, 'fixturecode', 'fixture-client-secret', 'fixture-hook-secret']) assert.ok(!stored.includes(secret));
  await complete(options.directory, callback, ['provision'], request, () => assert.fail('No rotation'));
  assert.equal(conversions, 1);
  assert.equal(handoffs, 1);
});

test('failed provisioning preserves created identity and suppresses the command output', async t => {
  const options = fixture(t);
  const saved = await prepare(options, discovery('Organization'));
  const callback = `http://127.0.0.1:8765/callback?code=fixturecode&state=${saved.nonce}`;
  const command = [process.execPath, '-e', 'process.stdin.on("data", d => process.stderr.write(d)); process.stdin.on("end", () => process.exit(1));'];
  await assert.rejects(complete(options.directory, callback, command, async () => ({ ...app, pem: 'PRIVATE KEY synthetic-secret' })), error => {
    assert.match(error.message, /Output withheld/);
    assert.ok(!error.message.includes('synthetic-secret'));
    return true;
  });
  const recovered = await complete(options.directory, callback, command, () => assert.fail('No new App'));
  assert.equal(recovered.app.id, app.id);
  assert.notEqual(recovered.keyHandedOff, true);
});

test('uncertain conversion is never silently retried', async t => {
  const options = fixture(t);
  const saved = await prepare(options, discovery('Organization'));
  const callback = `http://127.0.0.1:8765/callback?code=fixturecode&state=${saved.nonce}`;
  await assert.rejects(complete(options.directory, callback, ['provision'], () => { throw new Error('Fixture timeout'); }));
  await assert.rejects(complete(options.directory, callback, ['provision'], () => assert.fail('No retry')), /already attempted/);
});

test('readback rejects pending grants, suspension, identity errors and wrong repository scope', () => {
  const token = { permissions: permissions.cadence };
  assert.equal(validateReadback(state(), app, installation, token, repositories).installationId, 30);
  for (const changed of [
    { ...installation, permissions: { ...permissions.cadence, checks: 'read' } },
    { ...installation, account: { login: 'other' } },
    { ...installation, suspended_at: '2026-01-01' },
    { ...installation, app_id: 999 },
    { ...installation, permissions: { ...permissions.cadence, contents: 'write' } },
  ]) assert.throws(() => validateReadback(state(), app, changed, token, repositories));
  assert.throws(() => validateReadback(state(), other, installation, token, repositories), /identity/);
  assert.throws(() => validateReadback(state(), app, installation, token, [...repositories, { id: 99, full_name: 'example/unselected' }]), /selection/);
  assert.throws(() => validateReadback(state(), app, installation, { permissions: { contents: 'read' } }, repositories), /Missing/);
});

test('App JWT verification narrows tokens, reads repositories and revokes even on failure', async () => {
  const { privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });
  const pem = privateKey.export({ type: 'pkcs8', format: 'pem' });
  for (const badScope of [false, true]) {
    const calls = [];
    const request = async (path, options = {}) => {
      calls.push({ path, options });
      if (path === 'apps/example-symphony') return other;
      if (path === 'app') return app;
      if (path.startsWith('users/')) return { login: 'example-cadence[bot]', type: 'Bot', id: 50 };
      if (path === 'repos/example/widget/installation') return installation;
      if (path.endsWith('/access_tokens')) return { token: 'fixture-installation-token', permissions: permissions.cadence };
      if (path.startsWith('installation/repositories')) return { repositories: badScope ? [] : repositories };
      if (path === 'installation/token') return null;
      assert.fail(`Unexpected path ${path}`);
    };
    if (badScope) await assert.rejects(verify(state(), pem, request), /selection/);
    else {
      const result = await verify(state(), pem, request);
      assert.equal(result.botLogin, 'example-cadence[bot]');
      assert.ok(!JSON.stringify(result).includes('fixture-installation-token'));
    }
    const mint = calls.find(call => call.path.endsWith('/access_tokens'));
    assert.deepEqual(mint.options.body, { repositories: ['widget'], permissions: permissions.cadence });
    assert.equal(calls.at(-1).path, 'installation/token');
    assert.equal(calls.at(-1).options.method, 'DELETE');
  }
});
