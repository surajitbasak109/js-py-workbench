# AGENTS.md

## Repository Overview

`js-py-workbench` is a monorepo combining a Vite JavaScript frontend (`apps/web`), a FastAPI Python backend (`apps/py_service`), and shared JavaScript helpers (`packages/js_helpers`), orchestrated via `pnpm` workspaces.

## Directory Layout

- `apps/web/`: Vite frontend (`vite.config.js` proxies `/api` and `/health` to `http://127.0.0.1:8000`).
- `apps/py_service/`: FastAPI service (`main.py`, `test_api.py`, `requirements.txt`) using an isolated virtual environment at `apps/py_service/.venv`.
- `packages/js_helpers/`: Shared ESM JavaScript helpers (`@repo/js-helpers`) with unit tests (`node --test`).
- `.github/workflows/ci.yml`: Automated CI pipeline running lint, tests, and production build.
- `PLAN.md` & `PROGRESS.md`: Architecture roadmap and task tracking.

## Key Commands (Run from Repo Root)

- **Install Python deps:** `pnpm run install:py`
- **Start full dev stack:** `pnpm dev` (`http://127.0.0.1:5173` and `http://127.0.0.1:8000`)
- **Lint all (JS + Python):** `pnpm lint` (`pnpm run lint:js`, `pnpm run lint:py`)
- **Format Python:** `pnpm run format:py`
- **Run all tests (JS + Python):** `pnpm test` (`pnpm run test:js`, `pnpm run test:py`)
- **Build frontend:** `pnpm run build`

## Engineering Guidelines for Agents

- Keep root `package.json` as an ES module (`"type": "module"`) and follow ESLint v9 flat config rules in `eslint.config.js`.
- Always run Python commands (`pytest`, `ruff`, `uvicorn`) through `apps/py_service/.venv/bin/` via the `pnpm` scripts.
- Validate FastAPI request/response shapes with Pydantic models and keep `TestClient` tests in `apps/py_service/test_api.py` updated when endpoints change.
- Never commit `.venv/`, `node_modules/`, `dist/`, `__pycache__/`, `.pytest_cache/`, or `.ruff_cache/`.
- Update `PROGRESS.md` when completing tasks or adding new pending work.

## Current Status Snapshot

- **Done:** Monorepo structure, `pnpm` scripts, Vite `/api` and `/health` proxy, Ruff setup, ESLint v9 flat config + ESM root setup, `TestClient` endpoint tests, `.github/workflows/ci.yml`, and extended `/api/batch-summary` models/metrics (`non_empty_items`, `char_stats`, `batch_previews`) in `apps/py_service/main.py`.
- **Pending:** Fixing the `retryAsync` import in `apps/web/src/main.js`, clearing any lingering listeners on ports `8000`/`5173`, rendering the new batch metrics/previews in `apps/web`, adding custom UI inputs, completing the full Git commit and push to `origin/main`, and writing `README.md`.
