# Progress: `js-py-workbench`

## Completed Steps

- [x] **Monorepo Scaffolding:** Configured `pnpm` workspaces across `apps/web`, `apps/py_service`, and `packages/js_helpers` with root scripts (`dev`, `dev:py`, `dev:web`, `build`, `install:py`, `test`, `test:js`, `test:py`).
- [x] **Vite Dev Proxy:** Configured `apps/web/vite.config.js` to proxy `/api` and `/health` to `http://127.0.0.1:8000` (`host: 127.0.0.1`, `port: 5173`, `strictPort: true`) and updated `apps/web/src/main.js` to use relative/env-based API paths.
- [x] **Ruff Linting & Formatting:** Added `ruff` to `apps/py_service/requirements.txt` and added `lint:py`, `format:py`, and `lint` scripts in root `package.json`.
- [x] **ESLint v9 Flat Config & ESM Support:** Created root `eslint.config.js` with browser globals for `apps/web/src` and Node globals for `packages/js_helpers`, installed `@eslint/js` and `globals`, and added `"type": "module"` (with ESM `dev` script) to root `package.json`.
- [x] **Backend Endpoint Tests:** Added `apps/py_service/test_api.py` covering `/health` and `/api/batch-summary` (valid batches, remainders, and 422 validation errors) using FastAPI `TestClient`.
- [x] **GitHub Actions CI Workflow:** Created `.github/workflows/ci.yml` to run `pnpm lint`, `pnpm test`, and `pnpm run build` on pushes and pull requests.
- [x] **Extended `/api/batch-summary` Contract:** Updated Pydantic models and endpoint logic in `apps/py_service/main.py` to return `non_empty_items`, `char_stats` (`total_chars`, `min_chars`, `max_chars`, `avg_chars`), and `batch_previews`.

## Pending Steps

- [x] **Fix `retryAsync` Import in Frontend:** Confirmed `retryAsync` is imported alongside `callPythonApi` in `apps/web/src/main.js`.
- [ ] **Clean Port/Process State & Verify Full Dev Loop:** JS/Python lint and formatting plus frontend build pass. Python pytest stalls on its first `TestClient` request, and sandbox policy denies listening on ports `8000` and `5173`; port state cannot be inspected here.
- [x] **Render Richer Batch Summary Metrics in Frontend:** The UI now displays item counts, batch size/count, character statistics, and batch previews.
- [x] **Add Custom User Input Controls in UI:** Existing editable items and batch-size inputs are wired to the summary request.
- [ ] **Complete Git Commit & GitHub Push:** Stage intended workspace files, commit, and push `main` to `origin`.
- [x] **Add Project Documentation:** Added setup instructions, workspace commands, architecture notes, and CI workflow details to `README.md`.
