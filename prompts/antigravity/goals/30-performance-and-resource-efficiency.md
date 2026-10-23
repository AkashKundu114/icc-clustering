# Goal: Performance and Resource Efficiency

Reduce unnecessary CPU, RAM, VRAM, disk, startup, and inference cost without sacrificing correctness or safety.

## Required method
1. Measure or establish a reproducible baseline before optimizing.
2. Identify the bottleneck using available profiling or instrumentation.
3. Choose one targeted change at a time.
4. Preserve a correctness test and compare before/after measurements under equivalent conditions.
5. Record hardware, workload, warm-up, repetitions, variance, memory usage, and configuration.
6. Prefer bounded workloads; avoid filling disks, exhausting VRAM, or starting uncontrolled parallel jobs.

## Acceptance criteria
- Report measured results only when actually measured.
- State when a benchmark is noisy or not comparable.
- Do not optimize by dropping validation, reducing test coverage, or changing the workload silently.
- Keep the simpler implementation if improvement is negligible or unproven.
