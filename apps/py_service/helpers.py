import json
import os
import time
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


def get_env(key: str, default: str | None = None, required: bool = False) -> str:
    """Reads an environment variable with optional default or strict requirement."""
    value = os.getenv(key, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value or ""


def timer(label: str = "Task") -> Callable:
    """Logs execution time of a function for quick performance checks."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                print(f"[{label}] {func.__name__} took {elapsed_ms:.1f} ms")

        return wrapper

    return decorator


def read_json(file_path: str | Path, default: Any = None) -> Any:
    """Safely reads JSON from disk, returning `default` if missing or invalid."""
    path = Path(file_path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json_atomic(file_path: str | Path, data: Any) -> None:
    """Writes JSON safely via a temporary file to prevent half-written files."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(path)


def chunk_list(items: list[T], size: int) -> list[list[T]]:
    """Splits a list into smaller batches of at most `size` items."""
    if size <= 0:
        raise ValueError("Batch size must be greater than 0")
    return [items[i : i + size] for i in range(0, len(items), size)]
