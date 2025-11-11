# MM-Probe-Suite: Probing Tasks for Multimodal LLMs

![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat)
![PyTorch](https://img.shields.io/badge/pytorch-2.1+-ee4c2c.svg?style=flat)
![License](https://img.shields.io/badge/license-Apache--2.0-green.svg?style=flat)

> Small, targeted probes that isolate what a multimodal model actually
> perceives — beyond aggregate VQA scores.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Probes](#probes)
- [Adding a New Probe](#adding-a-new-probe)
- [Benchmarks](#benchmarks)
- [Citation](#citation)
- [License](#license)

## Overview

Most multimodal benchmarks bundle perception, reasoning, language, and world
knowledge into a single accuracy number. When a model gets 62%, you have no
idea *why*. MM-Probe-Suite collects a growing set of minimal probes — each
focused on a single, controllable aspect — so you can decompose model behavior
into something diagnosable.

Each probe is a small generator that produces images and questions where the
ground truth is controlled by construction, plus an evaluator that decides
whether the model's natural-language answer is correct.

We currently ship eight probes covering perception, binding, spatial reasoning,
and reading. They are designed to be cheap to run (under 1000 samples each)
so you can sweep models without burning a week on inference.

## Architecture

```
              ┌──────────────────┐
              │   Probe config   │   (yaml)
              └────────┬─────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────┐             ┌──────────────────┐
│  Generator    │── images ──▶│   ModelRunner    │── answers ──▶ Evaluator
│  (synthetic)  │  + prompts  │  (HF / OpenAI)   │
└───────────────┘             └──────────────────┘                  │
                                                                    ▼
                                                            ┌──────────────┐
                                                            │ JSONL report │
                                                            └──────────────┘
```

Each probe is independently runnable; runners and evaluators are interchangeable.

## Installation

```bash
git clone https://github.com/pulgog/mm-probe-suite
cd mm-probe-suite
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
pre-commit install  # optional
```

## Quick Start

Run a single probe against a local Hugging Face model:

```python
from mmprobe import load_probe
from mmprobe.runners import HFModelRunner

probe = load_probe("counting")
runner = HFModelRunner("llava-hf/llava-1.5-7b-hf", device="cuda")

report = probe.evaluate(runner, n=200)
print(f"counting accuracy: {report.accuracy:.3f}")
print(f"per-bucket: {report.per_bucket}")
```

Or from the command line:

```bash
python -m mmprobe.cli run \
    --probe counting \
    --model llava-hf/llava-1.5-7b-hf \
    --n 200 \
    --out reports/llava-counting.jsonl
```

## Probes

| Probe | What it tests | # configs |
|-------|--------------|-----------|
| `counting` | counts of 1-10 simple shapes with controlled clutter | 24 |
| `color_binding` | "which shape is red?" with multiple colored distractors | 18 |
| `spatial_rel` | above / below / left / right between two objects | 16 |
| `size_compare` | which of two objects is larger | 8 |
| `text_read` | synthetic single-word OCR on textured backgrounds | 12 |
| `temporal_order` | 2-frame side-by-side, "which happened first" | 10 |
| `presence` | is object X present, yes/no | 14 |
| `negation` | "is there NO X" — easy to fail by ignoring negation | 9 |

## Adding a New Probe

A probe is just a class that implements two methods. See
[`docs/adding_probes.md`](docs/adding_probes.md) for a tutorial.

```python
from mmprobe.base import Probe, Sample

class MyProbe(Probe):
    name = "myprobe"

    def generate(self, n, seed):
        # yield Sample(image=..., prompt=..., answer=...)
        ...

    def score(self, sample, model_answer):
        return sample.answer.lower() in model_answer.lower()
```

## Benchmarks

Preliminary results on a few open multimodal models (April 2025 snapshot):

| Model | counting | color | spatial | text | avg |
|-------|---------:|------:|--------:|-----:|----:|
| LLaVA-1.5-7B | 0.42 | 0.71 | 0.55 | 0.18 | 0.46 |
| LLaVA-1.5-13B | 0.48 | 0.76 | 0.61 | 0.22 | 0.52 |
| Qwen-VL-Chat | 0.51 | 0.74 | 0.58 | 0.34 | 0.54 |
| InstructBLIP-7B | 0.37 | 0.63 | 0.49 | 0.12 | 0.40 |

> Caveat: numbers will shift as probe configs evolve. Re-run with the version
> tag pinned for any comparison you publish.

## Citation

```bibtex
@software{linzihan_mmprobe_2024,
  author = {Lin, Zihan},
  title  = {MM-Probe-Suite: Probing Tasks for Multimodal LLMs},
  year   = {2024},
  url    = {https://github.com/pulgog/mm-probe-suite}
}
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).


## A note on prompt sensitivity

Probe scores can shift several points depending on how the prompt is phrased. The shipped prompts were chosen to be unambiguous, not to maximize any single model's score.
