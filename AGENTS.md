# AGENTS.md — Universal Project Plan & Engineering Rules

## 1. Objective & Stack

- **Goal:** Build a decoupled, zero-cost JavaScript + Python monorepo with reusable helper libraries and strict JSON boundaries.
- **Frontend (`apps/web`):** JavaScript (ES Modules, Vite).
- **Backend (`apps/py_service`):** Python 3.11+, FastAPI, Pydantic v2, Uvicorn.
- **Shared JS Helpers (`packages/js_helpers`):** Pure, framework-agnostic JavaScript utilities.

## 2. Repository Layout

- `apps/web/` — Browser UI and client-side orchestration only.
- `apps/py_service/` — FastAPI app (`main.py`), pure Python helpers (`helpers.py`), isolated `.venv/`.
- `packages/js_helpers/` — Shared JS helpers (`helpers.js`: `retryAsync`, `safeJsonParse`, `debounce`, `callPythonApi`).
- `package.json` — Root task runner (`concurrently`).

## 3. Canonical Commands (Run from Repo Root Unless Noted)

- **Install JS deps:** `npm install`
- **Install Python deps:** `cd apps/py_service && .venv/bin/pip install -r requirements.txt`
- **Start full dev stack:** `npm run dev` (Python on `127.0.0.1:8000`, Web on `localhost:5173`)
- **Run Python tests:** `cd apps/py_service && .venv/bin/pytest -v`
- **Run JS tests:** `node --test`
- **Lint & Format:**
  - Python: `cd apps/py_service && .venv/bin/ruff check . && .venv/bin/ruff format --check .`
  - JavaScript: `npx eslint .`

## 4. Phased Execution Plan

1. **Phase 1 (Foundation):** Verify `.gitignore`, `.env.example`, `.venv`, and simultaneous startup via `npm run dev`.
2. **Phase 2 (Helpers & Contract):** Keep business/data transformations in pure functions (`helpers.py`, `helpers.js`); validate all HTTP payloads with Pydantic models in `main.py`.
3. **Phase 3 (Frontend Slice):** Connect `apps/web` UI actions to FastAPI endpoints using `callPythonApi` with explicit loading, empty, and error states.
4. **Phase 4 (Verification):** Add unit tests for edge cases (empty inputs, malformed JSON, network failures) before adding new features.
5. **Phase 5 (Docs & Free Deploy):** Document setup and trade-offs in `README.md`; target $0/free-tier hosting only.

## 5. Strict Boundaries (For All AI Assistants)

- **ALWAYS:**
  - Keep functions small, pure, and typed/documented (Python type hints + JSDoc).
  - Run or provide exact verification commands (`curl`, `pytest`, `node --test`) after every change.
  - Preserve the `$0` local-first / free-tier budget constraint.
- **ASK FIRST:**
  - Before introducing new frameworks, ORMs, Docker services, or paid cloud dependencies.
  - Before changing API routes or Pydantic response schemas.
- **NEVER:**
  - Commit `.env`, `node_modules/`, or `apps/py_service/.venv/`.
  - Put Python data-processing logic inside `apps/web/` or duplicate helpers across packages.
  - Hardcode secrets or local absolute user paths (`/home/...`) inside source files.

## 5. Package Manager

Always use pnpm (pnpm install, pnpm dev, pnpm --filter ..., pnpm exec ...). Never emit npm or npx commands.
