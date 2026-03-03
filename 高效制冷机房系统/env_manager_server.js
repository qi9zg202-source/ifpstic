#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, spawnSync } = require('child_process');

const HOST = '127.0.0.1';
const PORT = 3845;
const ROOT_DIR = __dirname;
const SERVICE_NAME = 'env_manager_server.js';
const DB_PATH = path.join(ROOT_DIR, 'env_manager.sqlite');
const SOURCE_DB_PATH = '/Users/beckliu/Documents/0agentworkflowallinone/agentconf/claudecode_env.sqlite';
const USER_SETTINGS_PATH = path.join(os.homedir(), 'Library/Application Support/Code/User/settings.json');
const WORKSPACE_SETTINGS_PATH = path.join(ROOT_DIR, '.vscode/settings.json');
const ZSHRC_PATH = path.join(os.homedir(), '.zshrc');
const ZPROFILE_PATH = path.join(os.homedir(), '.zprofile');

const BLOCK_NAME = 'CLAUDE_ENV_MANAGER';
const START_COMMAND = `cd ${ROOT_DIR} && node ${SERVICE_NAME}`;
const STOP_COMMAND = `pkill -f "node ${path.join(ROOT_DIR, SERVICE_NAME)}"`;

function commandExists(command) {
  const result = spawnSync('which', [command], { encoding: 'utf8' });
  return result.status === 0;
}

function step(name, fn, required = true) {
  try {
    const details = fn();
    return { name, required, ok: true, details: details || '' };
  } catch (error) {
    return {
      name,
      required,
      ok: false,
      details: error instanceof Error ? error.message : String(error)
    };
  }
}

function runSql(sql) {
  return execFileSync('sqlite3', [DB_PATH, sql], { encoding: 'utf8' }).trim();
}

function queryJson(sql) {
  const out = execFileSync('sqlite3', ['-json', DB_PATH, sql], { encoding: 'utf8' }).trim();
  if (!out) return [];
  return JSON.parse(out);
}

function nowText() {
  return new Date().toLocaleString('zh-CN', { hour12: false });
}

function initDb() {
  runSql(`
    CREATE TABLE IF NOT EXISTS env_kv (
      env_key TEXT PRIMARY KEY,
      env_value TEXT NOT NULL,
      source_file TEXT,
      updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS env_state (
      id INTEGER PRIMARY KEY CHECK (id = 1),
      enabled INTEGER NOT NULL DEFAULT 1,
      last_refresh_at TEXT,
      last_result TEXT
    );

    CREATE TABLE IF NOT EXISTS sync_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action TEXT NOT NULL,
      result TEXT NOT NULL,
      message TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    );

    INSERT INTO env_state (id, enabled)
    VALUES (1, 1)
    ON CONFLICT(id) DO NOTHING;
  `);

  const count = Number(runSql('SELECT COUNT(*) FROM env_kv;'));
  if (count > 0) return;

  if (fs.existsSync(SOURCE_DB_PATH)) {
    const escaped = SOURCE_DB_PATH.replace(/'/g, "''");
    runSql(`
      ATTACH DATABASE '${escaped}' AS src;
      INSERT INTO env_kv (env_key, env_value, source_file, updated_at)
      SELECT env_key, env_value, env_file, datetime('now','localtime')
      FROM src.env_kv;
      DETACH DATABASE src;
    `);
  }
}

function getState() {
  const rows = queryJson('SELECT enabled, last_refresh_at, last_result FROM env_state WHERE id = 1;');
  const row = rows[0] || { enabled: 0, last_refresh_at: null, last_result: null };
  return {
    enabled: Number(row.enabled) === 1,
    lastRefreshAt: row.last_refresh_at || null,
    lastResult: row.last_result || null
  };
}

function setState(enabled, result) {
  const enabledInt = enabled ? 1 : 0;
  const resultSafe = String(result || '').replace(/'/g, "''");
  runSql(`
    UPDATE env_state
    SET enabled = ${enabledInt},
        last_refresh_at = datetime('now','localtime'),
        last_result = '${resultSafe}'
    WHERE id = 1;
  `);
}

function getEnvRows() {
  return queryJson('SELECT env_key, env_value, source_file, updated_at FROM env_kv ORDER BY env_key;');
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function readText(filePath) {
  if (!fs.existsSync(filePath)) return '';
  return fs.readFileSync(filePath, 'utf8');
}

function writeText(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
}

function replaceManagedBlock(original, lines) {
  const start = `# >>> ${BLOCK_NAME} START >>>`;
  const end = `# <<< ${BLOCK_NAME} END <<<`;
  const block = `${start}\n${lines.join('\n')}\n${end}`;

  const blockRegex = new RegExp(`\\n?# >>> ${BLOCK_NAME} START >>>[\\s\\S]*?# <<< ${BLOCK_NAME} END <<<\\n?`, 'g');
  let next = original.replace(blockRegex, '\n');
  next = next.replace(/\n{3,}/g, '\n\n').trimEnd();

  if (lines.length > 0) {
    if (next.length > 0) next += '\n\n';
    next += block + '\n';
  } else if (next.length > 0) {
    next += '\n';
  }

  return next;
}

function syncShellFiles(enabled, envRows) {
  const exportLines = enabled
    ? envRows.map((row) => `export ${row.env_key}=${shellQuote(row.env_value)}`)
    : [];

  for (const shellFile of [ZSHRC_PATH, ZPROFILE_PATH]) {
    const original = readText(shellFile);
    const next = replaceManagedBlock(original, exportLines);
    writeText(shellFile, next);
  }
}

function syncLaunchctl(enabled, envRows) {
  for (const row of envRows) {
    if (enabled) {
      spawnSync('launchctl', ['setenv', row.env_key, row.env_value], { stdio: 'ignore' });
    } else {
      spawnSync('launchctl', ['unsetenv', row.env_key], { stdio: 'ignore' });
    }
  }
}

function parseJsonFile(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try {
    const text = fs.readFileSync(filePath, 'utf8').trim();
    if (!text) return {};
    return JSON.parse(text);
  } catch {
    return {};
  }
}

function writeJsonFile(filePath, obj) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(obj, null, 4)}\n`, 'utf8');
}

function envRowsToSettingArray(enabled, envRows) {
  if (!enabled) return [];
  return envRows.map((row) => ({
    name: row.env_key,
    value: row.env_value
  }));
}

function syncVSCodeSettings(enabled, envRows) {
  const settingsFiles = [USER_SETTINGS_PATH, WORKSPACE_SETTINGS_PATH];
  const envArray = envRowsToSettingArray(enabled, envRows);

  for (const file of settingsFiles) {
    const settings = parseJsonFile(file);
    settings.claudeCode = settings.claudeCode || undefined;

    settings['claudeCode.useTerminal'] = true;
    settings['claudeCode.disableLoginPrompt'] = true;
    settings['claudeCode.allowDangerouslySkipPermissions'] = true;
    settings['claudeCode.initialPermissionMode'] = 'bypassPermissions';
    settings['claudeCode.environmentVariables'] = envArray;

    writeJsonFile(file, settings);
  }
}

function insertLog(action, result, message) {
  const actionSafe = String(action).replace(/'/g, "''");
  const resultSafe = String(result).replace(/'/g, "''");
  const messageSafe = String(message || '').replace(/'/g, "''");
  runSql(`
    INSERT INTO sync_log (action, result, message)
    VALUES ('${actionSafe}', '${resultSafe}', '${messageSafe}');
  `);
}

function refreshAll(action) {
  const state = getState();
  const envRows = getEnvRows();
  const enabled = state.enabled;

  syncShellFiles(enabled, envRows);
  syncLaunchctl(enabled, envRows);
  syncVSCodeSettings(enabled, envRows);

  setState(enabled, `OK @ ${nowText()}`);
  insertLog(action, 'OK', `enabled=${enabled}; env_count=${envRows.length}`);

  return {
    ok: true,
    enabled,
    envCount: envRows.length,
    dbPath: DB_PATH,
    syncedTargets: {
      shellFiles: [ZSHRC_PATH, ZPROFILE_PATH],
      vscodeFiles: [USER_SETTINGS_PATH, WORKSPACE_SETTINGS_PATH]
    }
  };
}

function setEnabledAndRefresh(enabled, action) {
  setState(enabled, `PENDING @ ${nowText()}`);
  return refreshAll(action);
}

function getPayload() {
  const state = getState();
  const envRows = getEnvRows();
  const logs = queryJson('SELECT id, action, result, message, created_at FROM sync_log ORDER BY id DESC LIMIT 20;');

  return {
    ok: true,
    dbPath: DB_PATH,
    state,
    envRows,
    logs,
    targets: {
      shellFiles: [ZSHRC_PATH, ZPROFILE_PATH],
      vscodeFiles: [USER_SETTINGS_PATH, WORKSPACE_SETTINGS_PATH]
    }
  };
}

function getServicePayload() {
  return {
    ok: true,
    service: {
      name: SERVICE_NAME,
      pid: process.pid,
      host: HOST,
      port: PORT,
      rootDir: ROOT_DIR,
      running: true
    },
    commands: {
      start: START_COMMAND,
      stop: STOP_COMMAND
    }
  };
}

function startAllDependencies() {
  const results = [];

  results.push(step('service-process', () => `pid=${process.pid}; running=true`, true));
  results.push(step('node-binary', () => `version=${process.version}`, true));
  results.push(step('sqlite3-binary', () => {
    if (!commandExists('sqlite3')) throw new Error('sqlite3 not found in PATH');
    return 'sqlite3 is available';
  }, true));
  results.push(step('launchctl-binary', () => {
    if (!commandExists('launchctl')) throw new Error('launchctl not found in PATH');
    return 'launchctl is available';
  }, false));
  results.push(step('source-db-check', () => {
    if (!fs.existsSync(SOURCE_DB_PATH)) throw new Error(`source db not found: ${SOURCE_DB_PATH}`);
    return SOURCE_DB_PATH;
  }, false));
  results.push(step('html-assets-check', () => {
    const requiredFiles = ['index.html', 'env_manager.html', SERVICE_NAME];
    const missing = requiredFiles.filter((file) => !fs.existsSync(path.join(ROOT_DIR, file)));
    if (missing.length > 0) throw new Error(`missing files: ${missing.join(', ')}`);
    return 'all required html/server files exist';
  }, true));

  results.push(step('db-init', () => {
    initDb();
    return `db initialized: ${DB_PATH}`;
  }, true));

  results.push(step('env-sync', () => {
    const refreshed = refreshAll('service-start-all');
    return `env_count=${refreshed.envCount}; enabled=${refreshed.enabled}`;
  }, true));

  const requiredFailures = results.filter((item) => item.required && !item.ok);
  const optionalFailures = results.filter((item) => !item.required && !item.ok);

  const summary = {
    requiredTotal: results.filter((item) => item.required).length,
    requiredFailed: requiredFailures.length,
    optionalFailed: optionalFailures.length,
    total: results.length
  };

  const ok = requiredFailures.length === 0;
  const message = ok
    ? `All required dependencies started (${summary.requiredTotal}/${summary.requiredTotal}).`
    : `Required dependency startup failed (${summary.requiredFailed} failed).`;

  insertLog('service-start-all', ok ? 'OK' : 'FAIL', `${message} optionalFailed=${summary.optionalFailed}`);

  return {
    ok,
    message,
    summary,
    dependencies: results,
    ...getServicePayload()
  };
}

function sendJson(res, statusCode, obj) {
  const text = JSON.stringify(obj, null, 2);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(text);
}

function sendHtml(res, htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(html);
}

function main() {
  initDb();

  const server = http.createServer((req, res) => {
    try {
      const url = new URL(req.url, `http://${HOST}:${PORT}`);

      if (req.method === 'OPTIONS') {
        sendJson(res, 200, { ok: true });
        return;
      }

      if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
        sendHtml(res, path.join(ROOT_DIR, 'index.html'));
        return;
      }

      if (req.method === 'GET' && url.pathname === '/env_manager.html') {
        sendHtml(res, path.join(ROOT_DIR, 'env_manager.html'));
        return;
      }

      if (req.method === 'GET' && url.pathname === '/api/status') {
        sendJson(res, 200, getPayload());
        return;
      }

      if (req.method === 'POST' && url.pathname === '/api/enable') {
        sendJson(res, 200, setEnabledAndRefresh(true, 'enable'));
        return;
      }

      if (req.method === 'POST' && url.pathname === '/api/pause') {
        sendJson(res, 200, setEnabledAndRefresh(false, 'pause'));
        return;
      }

      if (req.method === 'POST' && url.pathname === '/api/refresh') {
        sendJson(res, 200, refreshAll('refresh'));
        return;
      }

      if (req.method === 'GET' && url.pathname === '/api/service/info') {
        sendJson(res, 200, getServicePayload());
        return;
      }

      if (req.method === 'POST' && url.pathname === '/api/service/start') {
        const result = startAllDependencies();
        sendJson(res, result.ok ? 200 : 500, result);
        return;
      }

      if (req.method === 'POST' && url.pathname === '/api/service/stop') {
        sendJson(res, 200, {
          ok: true,
          message: 'Stop signal accepted. Service will exit shortly.',
          commands: { stop: STOP_COMMAND }
        });
        setTimeout(() => process.exit(0), 300);
        return;
      }

      sendJson(res, 404, { ok: false, error: 'Not Found' });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      insertLog('error', 'FAIL', message);
      sendJson(res, 500, { ok: false, error: message });
    }
  });

  server.listen(PORT, HOST, () => {
    console.log(`[env-manager] running at http://${HOST}:${PORT}`);
    console.log(`[env-manager] sqlite: ${DB_PATH}`);
  });
}

main();
