"""Call the Watson NLP emotion classification endpoint and format its result."""

from __future__ import annotations

import os
from typing import Any

import requests


DEFAULT_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


class EmotionServiceError(RuntimeError):
    """Raised when the emotion service cannot return a usable prediction."""


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return individual emotion scores and the dominant emotion.

    Configure ``WATSON_EMOTION_URL`` when your course provides a different
    Watson NLP endpoint. The endpoint accepts the IBM Watson NLP v1 request
    format used by the EmotionPredict service.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        raise ValueError("Please enter text to analyze.")

    url = os.getenv("WATSON_EMOTION_URL", DEFAULT_URL)
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json",
    }
    payload = {"raw_document": {"text": text_to_analyze.strip()}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise EmotionServiceError("The Watson emotion service is unavailable.") from exc
    except ValueError as exc:
        raise EmotionServiceError("The Watson emotion service returned invalid JSON.") from exc

    try:
        scores = result["emotionPredictions"][0]["emotion"]
        normalized = {name: float(scores[name]) for name in EMOTION_NAMES}
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise EmotionServiceError("The Watson response did not contain valid emotion scores.") from exc

    normalized["dominant_emotion"] = max(EMOTION_NAMES, key=normalized.__getitem__)
    return normalized
