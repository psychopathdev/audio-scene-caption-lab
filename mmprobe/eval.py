"""Evaluation entry point."""
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Iterable
from .base import Probe


@dataclass
class Report:
    probe: str
    n: int
    accuracy: float
    per_bucket: dict = field(default_factory=dict)


def evaluate(probe: Probe, runner, n: int = 200, seed: int = 0, progress: bool = False) -> Report:
    correct = 0
    total = 0
    bucket = defaultdict(lambda: [0, 0])
    samples: Iterable = probe.generate(n, seed=seed)
    if progress:
        try:
            from tqdm import tqdm
            samples = tqdm(samples, total=n, desc=probe.name)
        except ImportError:
            pass
    for sample in samples:
        ans = runner.answer(sample.image, sample.prompt)
        ok = probe.score(sample, ans)
        correct += int(ok)
        total += 1
        if sample.meta:
            k0 = next(iter(sample.meta))
            bucket[f"{k0}={sample.meta[k0]}"][0] += int(ok)
            bucket[f"{k0}={sample.meta[k0]}"][1] += 1
    return Report(
        probe=probe.name,
        n=total,
        accuracy=correct / total if total else 0.0,
        per_bucket={k: v[0] / v[1] for k, v in bucket.items() if v[1]},
    )
