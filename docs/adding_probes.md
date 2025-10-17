# Adding a New Probe

A probe is a class that inherits from `mmprobe.base.Probe` and is decorated
with `@register`. It needs two methods:

- `generate(n, seed)` — yield `Sample(image, prompt, answer, meta)` instances
- `score(sample, model_answer)` — return a bool

## Template

```python
from mmprobe.base import Probe, Sample, register


@register
class MyProbe(Probe):
    name = "my_probe"

    def generate(self, n, seed=0):
        import random
        rng = random.Random(seed)
        for _ in range(n):
            # ... build image and prompt ...
            yield Sample(image=img, prompt=q, answer=a, meta={...})

    def score(self, sample, model_answer):
        return sample.answer.lower() in model_answer.lower()
```

Drop the file in `mmprobe/`, import it from `mmprobe/__init__.py`, and the
CLI will pick it up automatically.

## Notes

- Keep N small per config — these probes are meant to be cheap.
- Put all randomness behind the `seed` argument so runs are reproducible.
- If the model's free-form answer doesn't trivially substring-match the gold,
  override `score` (see `counting.py` for an example using a regex).

## Reproducibility

When reporting numbers, pin both the probe version (git tag) and the model checkpoint hash.
