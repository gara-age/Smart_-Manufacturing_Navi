"""Conservative correction for frequently misheard smart-factory terms.

The result is still shown to the operator and physical control keeps its
existing confirmation step. This normalizer corrects known equipment and
command phrases only; it does not rewrite general Korean speech.
"""

from __future__ import annotations

import re


class ManufacturingTranscriptNormalizer:
    _REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
        # Common Korean Whisper variants of "컨베이어".
        (re.compile(r"(?:건배|컨배|콘베|컨베)\s*(?:이어|이여|여|어)"), "컨베이어"),
        # Speakable Korean variants of the AGV abbreviation.
        (re.compile(r"에이\s*지\s*(?:브이|비)"), "AGV"),
        # The phrase used by the device read tool.
        (re.compile(r"상대\s*확인"), "상태 확인"),
    )

    def normalize(self, text: str) -> str:
        normalized = " ".join(text.strip().split())
        for pattern, replacement in self._REPLACEMENTS:
            normalized = pattern.sub(replacement, normalized)
        return normalized
