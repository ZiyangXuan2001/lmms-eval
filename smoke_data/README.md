# Smoke Data

This directory is intentionally tracked. Keep only small, shareable smoke-test fixtures here.

Large or remote-only datasets belong in `data/`, which is ignored by Git.

## Cholec80

`cholec80/` contains a tiny portable fixture for framework smoke tests only. It has one JSONL sample for each generated task family (`A1`, `A2`, `A3`, `B1`, `B2`, `B3`, `B4`, and `C1`), local 160x90 JPEG thumbnails for referenced frames, and compact video01 annotation snippets.

Do not treat this as an evaluation subset or use it for model-quality reporting. Keep this directory small enough to share in GitHub.
