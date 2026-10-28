"""Global model registry for trained models in memory."""

from __future__ import annotations

from typing import Any

# In-memory registry of trained models
# Keys are model IDs, values are trained model instances
MODEL_REGISTRY: dict[str, Any] = {}
