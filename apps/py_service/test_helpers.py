import pytest

from helpers import chunk_list, get_env, read_json, timer, write_json_atomic


def test_get_env_default_and_override(monkeypatch):
    monkeypatch.delenv("TEST_WORKBENCH_VAR", raising=False)
    assert get_env("TEST_WORKBENCH_VAR", "fallback") == "fallback"

    monkeypatch.setenv("TEST_WORKBENCH_VAR", "custom-value")
    assert get_env("TEST_WORKBENCH_VAR", "fallback") == "custom-value"


def test_get_env_required_raises_when_missing(monkeypatch):
    monkeypatch.delenv("REQUIRED_TEST_VAR", raising=False)
    with pytest.raises(RuntimeError, match="REQUIRED_TEST_VAR"):
        get_env("REQUIRED_TEST_VAR", required=True)


def test_timer_logs_elapsed_time(capsys):
    @timer("UnitTest")
    def sample_add(a: int, b: int) -> int:
        return a + b

    assert sample_add(2, 3) == 5
    captured = capsys.readouterr()
    assert "[UnitTest] sample_add took" in captured.out
    assert "ms" in captured.out


def test_read_and_write_json_atomic(tmp_path):
    target = tmp_path / "nested" / "state.json"
    assert read_json(target, default={"init": True}) == {"init": True}

    payload = {"items": ["alpha", "beta"], "count": 2}
    write_json_atomic(target, payload)
    assert read_json(target) == payload

    # Leftover temp file should not remain after atomic replace
    assert not target.with_suffix(".json.tmp").exists()


def test_read_json_corrupt_file_returns_default(tmp_path):
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("{not-valid-json", encoding="utf-8")
    assert read_json(bad_file, default=[]) == []


def test_chunk_list_batches_and_remainder():
    assert chunk_list(["a", "b", "c", "d", "e"], 2) == [["a", "b"], ["c", "d"], ["e"]]
    assert chunk_list([], 3) == []


def test_chunk_list_invalid_size():
    with pytest.raises(ValueError, match="greater than 0"):
        chunk_list(["a", "b"], 0)
