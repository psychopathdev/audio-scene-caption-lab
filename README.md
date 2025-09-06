# MM-Probe-Suite: Probing Tasks for Multimodal LLMs

> Small, targeted probes that try to isolate what a multimodal model actually
> perceives, beyond aggregate VQA scores.

## Overview

Most multimodal benchmarks bundle perception, reasoning, language, and world
knowledge into a single accuracy number. When a model gets 62%, you have no
idea *why*. This repo collects a growing set of minimal probes — each focused
on a single, controllable aspect — so you can decompose model behavior.

Right now we cover:

- counting (1-10 objects, controlled clutter)
- spatial relations (above/below/left/right with single-object distractors)
- color binding
- text-in-image reading (synthetic OCR)
- temporal ordering on 2-frame composites

## Installation

```bash
git clone https://github.com/pulgog/mm-probe-suite
cd mm-probe-suite
pip install -r requirements.txt
```

## Quick Start

```python
from probes import load_probe
from runners import HFModelRunner

probe = load_probe("counting")
runner = HFModelRunner("llava-hf/llava-1.5-7b-hf")

acc = probe.evaluate(runner)
print(f"counting accuracy: {acc:.3f}")
```

## License

Apache-2.0
