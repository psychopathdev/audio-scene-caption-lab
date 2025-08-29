"""Probe base classes and registry."""
from dataclasses import dataclass, field
from typing import Any, Iterable, Optional

_REGISTRY = {}


@dataclass
class Sample:
    image: Any
    prompt: str
    answer: str
    meta: dict = field(default_factory=dict)


class Probe:
    name: str = "base"

    def generate(self, n: int, seed: int = 0) -> Iterable[Sample]:
        raise NotImplementedError

    def score(self, sample: Sample, model_answer: str) -> bool:
        gold = str(sample.answer).lower().strip()
        pred = (model_answer or "").lower().strip()
        return gold in pred


def register(cls):
    _REGISTRY[cls.name] = cls
    return cls


def load_probe(name: str) -> Probe:
    if name not in _REGISTRY:
        raise KeyError(f"unknown probe {name!r}, available: {list(_REGISTRY)}")
    return _REGISTRY[name]()


def list_probes():
    return sorted(_REGISTRY.keys())
