from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from helpers import chunk_list, get_env, timer

app = FastAPI(title="js-py-workbench API", version="0.1.0")

allowed_origins = [
    origin.strip()
    for origin in get_env("ALLOWED_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(
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


class BatchSummaryRequest(BaseModel):
    items: list[str] = Field(..., min_length=1)
    batch_size: int = Field(default=2, ge=1, le=500)


class BatchPreview(BaseModel):
    batch_index: int
    item_count: int
    first_item: str
    last_item: str


class CharacterStats(BaseModel):
    total_chars: int
    min_chars: int
    max_chars: int
    avg_chars: float


class BatchSummaryResponse(BaseModel):
    total_items: int
    non_empty_items: int
    batch_size: int
    batch_count: int
    char_stats: CharacterStats
    batch_previews: list[BatchPreview]
    batches: list[list[str]]


def _compute_char_stats(items: list[str]) -> CharacterStats:
    lengths = [len(item) for item in items]
    total = sum(lengths)
    count = len(lengths)
    return CharacterStats(
        total_chars=total,
        min_chars=min(lengths),
        max_chars=max(lengths),
        avg_chars=round(total / count, 2),
    )


def _build_batch_previews(batches: list[list[str]]) -> list[BatchPreview]:
    return [
        BatchPreview(
            batch_index=idx,
            item_count=len(batch),
            first_item=batch[0],
            last_item=batch[-1],
        )
        for idx, batch in enumerate(batches)
    ]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "py_service"}


@app.post("/api/batch-summary", response_model=BatchSummaryResponse)
@timer("API")
async def batch_summary(payload: BatchSummaryRequest) -> BatchSummaryResponse:
    batches = chunk_list(payload.items, payload.batch_size)
    non_empty_items = sum(1 for item in payload.items if item.strip())

    return BatchSummaryResponse(
        total_items=len(payload.items),
        non_empty_items=non_empty_items,
        batch_size=payload.batch_size,
        batch_count=len(batches),
        char_stats=_compute_char_stats(payload.items),
        batch_previews=_build_batch_previews(batches),
        batches=batches,
    )
