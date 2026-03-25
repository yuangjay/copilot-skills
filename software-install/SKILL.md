---
name: software-install
description: >
  Install software packages and verify they are runnable. Handles pip, npm/yarn, and Docker.
  Runs a quick smoke test immediately after install, then a full test suite.
  Triggers on: install, setup, configure dependencies, add package, get X working,
  install and test, make sure X runs, check if X is installed.
argument-hint: 'Describe what to install and where (e.g., "install Flask in /my/project", "set up React in /app")'
---

# Software Install & Verify Skill

## Purpose

Install one or more software packages, confirm the install succeeded, run a **smoke test**
immediately, then run (or generate) a **full test suite**. Every step is logged so failures
can be diagnosed quickly.

---

## MANDATORY Pre-Install Gate

Before touching any package manager, run these checks in order:

```
1. Identify the install method needed (pip / npm / yarn / docker)
2. Confirm the target directory / project (ask if ambiguous)
3. Check whether software is ALREADY installed — do not reinstall needlessly
```

---

## Phase 1 — Environment Detection

### Python / pip projects
```bash
# Check Python
python --version || python3 --version

# Check pip
pip --version || pip3 --version

# Check for existing venv
ls .venv/ 2>/dev/null && echo "venv exists" || echo "no venv"
```

### Node.js / npm / yarn projects
```bash
node --version
npm --version
yarn --version 2>/dev/null || echo "yarn not installed"
```

### Docker projects
```bash
docker --version
docker compose version
```

---

## Phase 2 — Install

### Rule: ALWAYS use a virtual environment for Python packages

```bash
# Create venv if it doesn't exist
python -m venv .venv

# Activate
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# Install
pip install --no-cache-dir -r requirements.txt
# or: pip install <package-name>
```

### Node.js
```bash
cd <project-dir>
npm install           # if package-lock.json exists
# yarn install        # if yarn.lock exists
```

### Docker
```bash
# Pull image only
docker pull <image>:<tag>

# Or build + start via compose (preferred)
docker compose up -d --build
```

---

## Phase 3 — Smoke Test (MANDATORY, runs immediately after install)

Run the quickest possible check to confirm the software works at all.

### Python
```bash
# Import check
python -c "import <package>; print('<package> OK')"

# Or run the app for 3 seconds and check exit
timeout 3 python app.py && echo "App started OK" || echo "App failed to start"
```

### Node.js
```bash
node -e "require('<package>'); console.log('<package> OK')"
```

### Docker service
```bash
# Wait up to 15s for healthy status
for i in $(seq 1 15); do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' <container> 2>/dev/null)
  [ "$STATUS" = "healthy" ] && echo "Container healthy" && break
  echo "Waiting... ($i/15)"
  sleep 1
done

# HTTP health endpoint (if applicable)
curl -sf http://localhost:<PORT>/health && echo "Health check passed"
```

---

## Phase 4 — Full Test Suite

### If tests already exist — run them:

```bash
# Python
pytest --tb=short -q

# Node.js
npm test
# or: yarn test
```

### If NO tests exist — generate and run them:

1. Create `tests/test_<module>.py` (Python) or `tests/<module>.test.js` (Node).
2. Write at minimum:
   - **Import / require test** — package loads without error
   - **Basic functionality test** — core function returns expected output
   - **Error handling test** — invalid input is handled gracefully
3. Run the generated tests immediately.
4. All tests must pass before proceeding.

#### Python test template
```python
import pytest
import <module>

def test_import():
    assert <module> is not None

def test_basic_functionality():
    result = <module>.<function>(<valid_input>)
    assert result is not None

def test_error_handling():
    with pytest.raises(Exception):
        <module>.<function>(<invalid_input>)
```

#### Node.js test template (Jest)
```javascript
const pkg = require('<package>');

test('package loads', () => {
  expect(pkg).toBeDefined();
});

test('basic functionality', () => {
  const result = pkg.<function>(<valid_input>);
  expect(result).not.toBeNull();
});
```

---

## Phase 5 — Pass/Fail Report

After all tests, output a clear summary:

```
============================
INSTALL & TEST REPORT
============================
Package    : <name> <version>
Install    : [PASS]
Smoke test : [PASS]
Unit tests : [PASS] X/X passed
============================
Status     : READY
```

If ANY step fails:
- Show the exact error output
- Diagnose the cause (missing dep, wrong Python version, port conflict, etc.)
- Apply a fix and **re-run from the failing phase** — do not skip ahead

---

## Phase 6 — Git Commit (after all tests pass)

```bash
git add .
git commit -m "install: add <package> <version>

- Installed via <pip/npm/docker>
- Smoke test: PASS
- Unit tests: X/X passed
- Verification: run \`pytest\` or \`npm test\` to reproduce"
```

**RULE: Never commit if any test is failing.**

---

## Decision Tree — Failure Recovery

```
Test failed?
  ├── ImportError / ModuleNotFoundError
  │     └── pip install <missing-dep> → re-run smoke test
  ├── Port already in use
  │     └── find free port → update config → re-run smoke test
  ├── Permissions error
  │     └── check venv activation → re-run install
  ├── Version conflict
  │     └── pin version in requirements.txt → reinstall → re-run tests
  └── Unknown error
        └── show full traceback → fix → re-run from Phase 3
```

---

## Key Principles

- **Never skip the smoke test** — even a one-line import check catches 80% of failures early.
- **Never skip the venv** (Python) — global installs cause hard-to-debug conflicts.
- **Docker is preferred** for services — use `docker compose up` not bare `docker run`.
- **All tests must pass before git commit** — no partial commits.
- **Log everything** — show command output so failures are traceable.

---

## Examples

**Install Flask and verify:**
> `install Flask in /ephemeral/workspace/myapp and make sure it runs`

**Set up a Node API:**
> `install express and set it up in /ephemeral/workspace/api, run tests`

**Pull and verify a Docker image:**
> `install and test the redis Docker image`

**Install from requirements.txt:**
> `install all dependencies for /ephemeral/workspace/rag_skill and confirm they work`
