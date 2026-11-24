from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "py_service",
    }


def test_batch_summary_even_and_remainder_batches():
    payload = {
        "items": ["alpha", "beta", "gamma", "delta", "epsilon"],
        "batch_size": 2,
    }
    response = client.post("/api/batch-summary", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 5
    assert data["batch_size"] == 2
    assert data["batch_count"] == 3
    assert data["batches"] == [
        ["alpha", "beta"],
        ["gamma", "delta"],
        ["epsilon"],
    ]


def test_batch_summary_single_batch():
    payload = {
        "items": ["one", "two"],
        "batch_size": 5,
    }
    response = client.post("/api/batch-summary", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "total_items": 2,
        "batch_size": 5,
        "batch_count": 1,
        "batches": [["one", "two"]],
    }


def test_batch_summary_rejects_empty_items():
    response = client.post(
        "/api/batch-summary",
        json={"items": [], "batch_size": 2},
    )

    assert response.status_code == 422


def test_batch_summary_rejects_invalid_batch_size():
    response = client.post(
        "/api/batch-summary",
        json={"items": ["alpha", "beta"], "batch_size": 0},
    )

    assert response.status_code == 422
