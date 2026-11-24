from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from helpers import chunk_list, get_env, timer

app = FastAPI(title="JS + Python Workbench API", version="0.1.0")

# Allow local JS dev servers (Vite / React) during local development
allowed_origins = [
    origin.strip()
    for origin in get_env("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(
        ","
    )
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BatchRequest(BaseModel):
    items: list[str] = Field(default_factory=list, min_length=1)
    batch_size: int = Field(default=3, ge=1, le=100)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "py_service"}


@app.post("/api/batch-summary")
@timer("API")
def batch_summary(payload: BatchRequest) -> dict:
    batches = chunk_list(payload.items, payload.batch_size)
    return {
        "total_items": len(payload.items),
        "batch_size": payload.batch_size,
        "batch_count": len(batches),
        "batches": batches,
    }
