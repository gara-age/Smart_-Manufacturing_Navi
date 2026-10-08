"""Audio-to-text service adapted from the VisionNavi faster-whisper flow.

The Whisper model is loaded only on the first voice request so normal text-only
operation does not pay the model startup cost.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from app.core.application_config import settings
from app.service.manufacturing_transcript_normalizer import ManufacturingTranscriptNormalizer


class AudioTranscriptionService:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._lock = threading.Lock()
        self._normalizer = ManufacturingTranscriptNormalizer()

    def transcribe(self, audio_path: Path, language_hint: str | None = "ko") -> dict[str, Any]:
        model = self._get_model()
        language = self._normalize_language(language_hint)
        segments, info = model.transcribe(
            str(audio_path),
            language=language,
            vad_filter=settings.AUDIO_TRANSCRIPTION_VAD_FILTER,
            beam_size=settings.AUDIO_TRANSCRIPTION_BEAM_SIZE,
            condition_on_previous_text=False,
            initial_prompt=settings.AUDIO_TRANSCRIPTION_INITIAL_PROMPT,
        )
        raw_text = " ".join(
            segment.text.strip() for segment in segments if getattr(segment, "text", "").strip()
        ).strip()
        text = self._normalizer.normalize(raw_text)
        return {
            "text": text,
            "raw_text": raw_text,
            "detected_language": getattr(info, "language", None),
            "language_probability": getattr(info, "language_probability", None),
            "model": settings.AUDIO_TRANSCRIPTION_MODEL,
        }

    def _get_model(self) -> Any:
        with self._lock:
            if self._model is not None:
                return self._model
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise RuntimeError(
                    "Voice input dependencies could not be imported "
                    f"({exc}). Run: python -m pip install -r requirements.txt"
                ) from exc
            self._model = WhisperModel(
                settings.AUDIO_TRANSCRIPTION_MODEL,
                device=settings.AUDIO_TRANSCRIPTION_DEVICE,
                compute_type=settings.AUDIO_TRANSCRIPTION_COMPUTE_TYPE,
            )
            return self._model

    @staticmethod
    def _normalize_language(language_hint: str | None) -> str | None:
        if not language_hint or language_hint.strip().lower() == "auto":
            return None
        value = language_hint.strip().lower()
        if value in {"korean", "ko-kr", "한국어"}:
            return "ko"
        return value
