# JS + Python Workbench

A local-first monorepo with a Vite JavaScript frontend, a FastAPI service, and shared JavaScript helpers. `pnpm` manages the JavaScript workspaces; the Python service uses its own virtual environment.

## Requirements

- Node.js and pnpm
- Python 3.11 or newer

## Setup

Install the JavaScript workspace dependencies and create/install the Python environment:

```sh
pnpm install
python3 -m venv apps/py_service/.venv
pnpm run install:py
```

## Run locally

Start both services from the repository root:

```sh
pnpm dev
```

The web app is at <http://127.0.0.1:5173>; FastAPI listens at <http://127.0.0.1:8000>. Vite proxies `/api` and `/health` to FastAPI. The UI sends a comma-separated item list and batch size to `POST /api/batch-summary`, then displays counts, character statistics, and batch previews.

## Workspace commands

| Command | Purpose |
| --- | --- |
| `pnpm run dev:web` | Start only the Vite frontend |
| `pnpm run dev:py` | Start only the FastAPI service |
| `pnpm run build` | Build the frontend for production |
| `pnpm lint` | Run JavaScript and Python lint/format checks |
| `pnpm test` | Run JavaScript and Python tests |
| `pnpm run install:py` | Install Python requirements into the service venv |

## Project layout

- `apps/web/` — Vite UI and API client
- `apps/py_service/` — FastAPI endpoints, data helpers, and endpoint tests
- `packages/js_helpers/` — Reusable ESM helpers and unit tests
- `.github/workflows/ci.yml` — CI for linting, tests, and frontend build

Python dependencies and generated build/test files are excluded from version control. The backend can be configured with `ALLOWED_ORIGINS`; its default permits the local Vite origins.
