"""Probe base classes."""
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class Sample:
    image: Any  # PIL.Image or np.ndarray
    prompt: str
    answer: str
    meta: dict = None


class Probe:
    name = "base"

    def generate(self, n: int, seed: int = 0) -> Iterable[Sample]:
        raise NotImplementedError

    def score(self, sample: Sample, model_answer: str) -> bool:
        # default: substring match, case-insensitive
        return str(sample.answer).lower().strip() in (model_answer or "").lower()
