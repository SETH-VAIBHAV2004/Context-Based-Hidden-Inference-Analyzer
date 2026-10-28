from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from app.settings import get_settings
from nlp.context import ContextWindow, format_model_text, get_target_turn
from nlp.datasets.validation import label_distribution, load_jsonl_examples
from nlp.schemas import DialogueTurn
from pathlib import Path

settings = get_settings()
FIXTURE_PATH = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"

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
    return {
        "models": [
            {
                "id": "tfidf_lr",
                "name": "TF-IDF + Logistic Regression",
                "trained": False,
                "trained_on": None,
                "metrics_available": False,
            },
            {
                "id": "transformer_baseline",
                "name": "Transformer baseline",
                "trained": False,
                "metrics_available": False,
            },
            {
                "id": "context_transformer",
                "name": "Context-aware transformer",
                "trained": False,
                "metrics_available": False,
            },
            {
                "id": "context_features",
                "name": "Context plus linguistic features",
                "trained": False,
                "metrics_available": False,
            },
        ],
        "note": "No evaluation metrics are published until a training run writes them to artifacts/.",
    }


@app.get("/api/v1/metrics")
def metrics() -> dict:
    return {
        "runs": [],
        "note": "No evaluation runs have been recorded yet.",
    }


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
            "No trained model checkpoint is loaded yet.",
            "The API will not invent a pragmatic label.",
            "Train the TF-IDF baseline (Milestone 4) and place the artifact under artifacts/ before inference can return predictions.",
        ],
    )


@app.exception_handler(ValidationError)
async def validation_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "invalid_input", "detail": jsonable_encoder(exc.errors())},
    )
