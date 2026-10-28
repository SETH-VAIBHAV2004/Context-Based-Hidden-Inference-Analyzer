from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from app.settings import get_settings
from nlp.context import ContextWindow, format_model_text, get_target_turn
from nlp.datasets.validation import label_distribution, load_jsonl_examples, group_aware_split
from nlp.datasets.circa_io import load_circa_table
from nlp.models.tfidf_lr import train, evaluate, save_model, load_model, predict_one, TrainedBaseline
from nlp.registry import MODEL_REGISTRY
from nlp.schemas import DialogueTurn
from pathlib import Path
import json

settings = get_settings()
FIXTURE_PATH = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"
ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "artifacts"
METRICS_DIR = ARTIFACTS_DIR / "metrics"

app = FastAPI(
    title="Inferring the Unsaid API",
    version="0.1.0",
    description="Research API for pragmatic inference. Metrics are only returned from real evaluation runs.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class InferenceRequest(BaseModel):
    turns: list[DialogueTurn]
    target_turn_id: str
    context_window: ContextWindow = Field(default_factory=lambda: ContextWindow(name="prev_1"))
    model_id: str = "tfidf_lr"
    context_situation: str | None = None


class InferenceResponse(BaseModel):
    status: str
    model_id: str
    model_available: bool
    literal_utterance: str | None = None
    predicted_label: str | None = None
    class_probabilities: dict[str, float] | None = None
    context_text: str | None = None
    evidence: list[dict] = Field(default_factory=list)
    limitations: list[str]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "pragmatic-inference-api"}


@app.get("/api/v1/health")
def health_v1() -> dict:
    return health()


@app.get("/api/v1/datasets")
def list_datasets() -> dict:
    fixture_examples = load_jsonl_examples(FIXTURE_PATH)
    circa_configured = bool(settings.circa_path) and Path(settings.circa_path).exists()
    return {
        "datasets": [
            {
                "id": "synthetic_pragmatics",
                "name": "Synthetic polarity fixture",
                "language": "synthetic",
                "is_synthetic": True,
                "n_examples": len(fixture_examples),
                "labels": label_distribution(fixture_examples),
                "license": "Project MIT (synthetic content authored for tests)",
                "citation": "Not a published corpus. Do not report as Circa.",
                "available": True,
            },
            {
                "id": "circa",
                "name": "Circa (Louis et al., EMNLP 2020)",
                "language": "en",
                "is_synthetic": False,
                "n_examples": None,
                "labels": None,
                "license": "Creative Commons Attribution 4.0 (confirm deed before redistribution)",
                "citation": "Louis, Roth, and Radlinski. EMNLP 2020.",
                "source": "https://github.com/google-research-datasets/circa",
                "available": circa_configured,
                "limitation": (
                    None
                    if circa_configured
                    else "Official Circa file is not present. Set CIRCA_PATH after downloading from the authors."
                ),
            },
        ]
    }


@app.get("/api/v1/models")
def list_models() -> dict:
    models_info = []
    for model_id, model_name in [
        ("tfidf_lr", "TF-IDF + Logistic Regression"),
        ("transformer_baseline", "Transformer baseline"),
        ("context_transformer", "Context-aware transformer"),
        ("context_features", "Context plus linguistic features"),
    ]:
        is_trained = model_id in MODEL_REGISTRY
        trained_on = None
        if is_trained and model_id == "tfidf_lr":
            model = MODEL_REGISTRY[model_id]
            trained_on = model.dataset
        
        metrics_path = METRICS_DIR / f"{model_id}.json"
        models_info.append({
            "id": model_id,
            "name": model_name,
            "trained": is_trained,
            "trained_on": trained_on,
            "metrics_available": metrics_path.exists(),
        })
    
    return {
        "models": models_info,
        "note": "Train models via POST /api/v1/train. Metrics appear after evaluation.",
    }


@app.get("/api/v1/metrics")
def metrics() -> dict:
    if not METRICS_DIR.exists():
        return {"runs": [], "note": "No evaluation runs have been recorded yet."}
    
    runs = []
    for metrics_file in METRICS_DIR.glob("*.json"):
        try:
            with open(metrics_file) as f:
                metric_data = json.load(f)
                metric_data["model_id"] = metrics_file.stem
                runs.append(metric_data)
        except Exception:
            continue
    
    return {"runs": runs}


@app.post("/api/v1/inference", response_model=InferenceResponse)
def infer(payload: InferenceRequest) -> InferenceResponse:
    from nlp.schemas import PragmaticExample

    try:
        example = PragmaticExample(
            example_id="adhoc",
            dataset="user_input",
            dataset_version="live",
            conversation_id="live",
            turns=payload.turns,
            target_turn_id=payload.target_turn_id,
            label_scheme="unknown",
            context_situation=payload.context_situation,
            group_key="live",
            language="en",
            source_attribution="user-provided conversation",
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": "invalid_input", "messages": jsonable_encoder(exc.errors())},
        ) from exc
    
    target = get_target_turn(example)
    context_text = format_model_text(example, payload.context_window)
    
    # Check if model is trained
    if payload.model_id not in MODEL_REGISTRY:
        return InferenceResponse(
            status="model_unavailable",
            model_id=payload.model_id,
            model_available=False,
            literal_utterance=target.text,
            predicted_label=None,
            class_probabilities=None,
            context_text=context_text,
            evidence=[],
            limitations=[
                f"Model '{payload.model_id}' is not trained yet.",
                "Train the model via POST /api/v1/train before running inference.",
            ],
        )
    
    # Run inference with trained model
    if payload.model_id == "tfidf_lr":
        model = MODEL_REGISTRY[payload.model_id]
        predicted_label, probabilities = predict_one(model, example)
        
        return InferenceResponse(
            status="ok",
            model_id=payload.model_id,
            model_available=True,
            literal_utterance=target.text,
            predicted_label=predicted_label,
            class_probabilities=probabilities,
            context_text=context_text,
            evidence=[
                {
                    "turn_id": payload.target_turn_id,
                    "text": target.text,
                    "role": "target_utterance",
                    "source": "conversation",
                }
            ],
            limitations=[
                "Evidence is currently rule-based (target utterance highlight).",
                "Sufficiency/necessity diagnostics are planned for Milestone 5.",
            ],
        )
    
    return InferenceResponse(
        status="model_unavailable",
        model_id=payload.model_id,
        model_available=False,
        literal_utterance=target.text,
        predicted_label=None,
        class_probabilities=None,
        context_text=context_text,
        evidence=[],
        limitations=[f"Model type '{payload.model_id}' is not implemented yet."],
    )


class TrainRequest(BaseModel):
    dataset_id: str = "synthetic_pragmatics"
    model_id: str = "tfidf_lr"
    context_window: ContextWindow = Field(default_factory=lambda: ContextWindow(name="prev_1"))
    seed: int = 13
    test_ratio: float = Field(default=0.2, ge=0.1, le=0.5)


class TrainResponse(BaseModel):
    status: str
    model_id: str
    dataset_used: str
    n_train: int
    n_test: int
    test_metrics: dict | None = None
    limitations: list[str]


@app.post("/api/v1/train", response_model=TrainResponse)
def train_model(payload: TrainRequest) -> TrainResponse:
    # Load dataset
    if payload.dataset_id == "synthetic_pragmatics":
        examples = load_jsonl_examples(FIXTURE_PATH)
        is_synthetic = True
    elif payload.dataset_id == "circa":
        if not settings.circa_path or not Path(settings.circa_path).exists():
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "dataset_unavailable",
                    "message": "Circa file not configured. Set CIRCA_PATH environment variable.",
                },
            )
        try:
            examples = load_circa_table(Path(settings.circa_path))
            is_synthetic = False
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail={"error": "dataset_load_failed", "message": str(exc)},
            ) from exc
    else:
        raise HTTPException(
            status_code=400,
            detail={"error": "unknown_dataset", "message": f"Dataset '{payload.dataset_id}' not supported."},
        )
    
    # Split data
    splits = group_aware_split(
        examples,
        seed=payload.seed,
        train_ratio=1.0 - payload.test_ratio - 0.1,  # Save 10% for validation
        val_ratio=0.1,
    )
    train_examples = splits["train"]
    test_examples = splits["test"]
    
    if payload.model_id == "tfidf_lr":
        # Train model
        trained_model = train(train_examples, payload.context_window, seed=payload.seed)
        
        # Evaluate on test set
        test_metrics = evaluate(trained_model, test_examples)
        
        # Save model
        model_path = ARTIFACTS_DIR / "models" / f"{payload.model_id}.joblib"
        save_model(trained_model, model_path)
        
        # Save metrics
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        metrics_path = METRICS_DIR / f"{payload.model_id}.json"
        with open(metrics_path, "w") as f:
            json.dump(test_metrics, f, indent=2)
        
        # Register model
        MODEL_REGISTRY[payload.model_id] = trained_model
        
        limitations = []
        if is_synthetic:
            limitations.append("Trained on synthetic fixture data. Real Circa evaluation pending.")
        
        return TrainResponse(
            status="ok",
            model_id=payload.model_id,
            dataset_used=payload.dataset_id,
            n_train=len(train_examples),
            n_test=len(test_examples),
            test_metrics=test_metrics,
            limitations=limitations,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "model_not_implemented",
                "message": f"Training for '{payload.model_id}' is not implemented yet.",
            },
        )


@app.exception_handler(ValidationError)
async def validation_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "invalid_input", "detail": jsonable_encoder(exc.errors())},
    )
