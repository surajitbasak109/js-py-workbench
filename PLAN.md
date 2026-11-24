# Plan: `js-py-workbench` Monorepo

## Goal

Build and maintain a high-performance JavaScript + Python full-stack monorepo (`js-py-workbench`) managed with `pnpm` workspaces, pairing a Vite frontend (`apps/web`), a FastAPI + Pydantic backend (`apps/py_service`), and shared JS utilities (`packages/js_helpers`), backed by automated linting, unit/endpoint tests, and GitHub Actions CI.

## Architecture & Conventions

- **Package & Workspace Manager:** `pnpm` (`pnpm-workspace.yaml`), root `package.json` with `"type": "module"`.
- **Frontend (`apps/web`):** Vite dev server on `127.0.0.1:5173` (`strictPort: true`), proxying `/api` and `/health` to `http://127.0.0.1:8000` via `apps/web/vite.config.js`.
- **Backend (`apps/py_service`):** FastAPI + Uvicorn on `127.0.0.1:8000` with an isolated virtual environment at `apps/py_service/.venv`, Pydantic v2 request/response models, `pytest`, and `ruff`.
- **Shared JS Helpers (`packages/js_helpers`):** ESM modules (`@repo/js-helpers`) tested with `node --test`.
- **Code Quality & CI:** ESLint v9 flat config (`eslint.config.js`), Ruff check/format, `pnpm lint`, `pnpm test`, `pnpm run build`, and GitHub Actions (`.github/workflows/ci.yml`).

## Execution Roadmap

1. **Scaffold Monorepo & Dev Workflow:** Set up `apps/web`, `apps/py_service`, `packages/js_helpers`, `pnpm` scripts, and Vite proxy routing.
2. **Enforce Linting & Formatting:** Configure ESLint v9 flat config + ESM package type, and add Ruff check/format scripts.
3. **Establish Test & CI Pipelines:** Add `node:test` and `pytest` (`TestClient`) suites and configure `.github/workflows/ci.yml`.
4. **Version Control & Remote Sync:** Configure `.gitignore`, commit project files, link `origin`, and push `main` to GitHub.
5. **Expand API & UI Features:** Extend `/api/batch-summary` with item counts, character statistics, and batch previews; add interactive UI inputs and README documentation.
