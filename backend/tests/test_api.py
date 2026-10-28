from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_datasets_do_not_invent_circa_counts():
    response = client.get("/api/v1/datasets")
    body = response.json()
    circa = next(item for item in body["datasets"] if item["id"] == "circa")
    assert circa["available"] is False
    assert circa["n_examples"] is None
    synthetic = next(item for item in body["datasets"] if item["id"] == "synthetic_pragmatics")
    assert synthetic["is_synthetic"] is True
    assert synthetic["n_examples"] == 12


def test_metrics_empty():
    response = client.get("/api/v1/metrics")
    assert response.json()["runs"] == []


def test_inference_refuses_to_hallucinate_when_untrained():
    response = client.post(
        "/api/v1/inference",
        json={
            "turns": [
                {"turn_id": "t0", "speaker": "X", "text": "Do you like jazz?"},
                {"turn_id": "t1", "speaker": "Y", "text": "I have every Coltrane record."},
            ],
            "target_turn_id": "t1",
            "context_window": {"name": "prev_1"},
            "model_id": "tfidf_lr",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "model_unavailable"
    assert body["predicted_label"] is None
    assert body["literal_utterance"] == "I have every Coltrane record."
    assert "[TARGET]" in body["context_text"]


def test_inference_rejects_bad_target():
    response = client.post(
        "/api/v1/inference",
        json={
            "turns": [{"turn_id": "t0", "speaker": "X", "text": "Hello"}],
            "target_turn_id": "nope",
        },
    )
    assert response.status_code == 422
