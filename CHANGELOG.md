# Changelog

## 0.3.1 — 2025-09
- Bugfix: spatial probe was generating samples without checking the actual relation
- More forgiving answer parsing in counting

## 0.3.0 — 2025-04
- Added `spatial_rel`, `size_compare`, `presence`, `negation` probes
- New `OpenAIRunner` for gpt-4o-style endpoints
- Sweep script for yaml-driven model comparisons

## 0.2.0 — 2024-11
- Refactor: probe registry, CLI entry point
- `color_binding`, `text_read`, `temporal_order` probes

## 0.1.0 — 2024-06
- Initial release with counting probe
