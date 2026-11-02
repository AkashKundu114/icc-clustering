# Loop 5.8 final adjudication

## Scope and evidence boundary

The target repository was fetched before work. At baseline, `HEAD=origin/main=29bcc279589d4a6c1e6747885cc857085ac8d6d0` (`2026-11-02T17:13:17+05:30`, subject `5.7`); the tracked working tree was clean. Loop 5.8 outputs are uncommitted. The target checkout lacks the reviewed submission manuscript. The local FYP worktree at `D:\Final Year Project` was available, but its separate manuscript candidate has SHA-256 `BB09E87B34E529E3D8CA83BBF69BDFBBCB57AEDF75B2BC3BB49D6336A7911C53` and is not the same version boundary as the target repository. See `baseline_state.md`.

The recovered local stability evidence includes 4,320 partition arrays, 4,320 per-fit Parquet records, six cached cohort matrices and the saved aggregate summary. Loop 5.7's independent reconstruction reported 72/72 cells matching the saved summary with maximum absolute differences below 1.2e-16; Loop 5.8 independently forensically checked duplicate partition payloads and recalculated bootstrap sensitivity. No clustering model fits were rerun. Successful internal recalculation is not historical execution authentication.

## Dimension decisions

| Dimension | Verdict | Supporting evidence | Remaining blocker / required action |
|---|---|---|---|
| Scientific contribution | **CONDITIONALLY SUPPORTED** | Six-cohort reconstructed descriptive separation between pairwise subsample ARI and external-label ARI | Bound claim to these cohorts/protocol; avoid “correctness,” causal, universal or clinical inference |
| Numerical correctness | **VERIFIED, conditional on local files** | 72 aggregate cells match; mean stability .516586, mean external ARI .052312, mean gap .464274, median .448407 | Run-to-input and producer lineage are not authenticated |
| Statistical validity | **HOLD** | Corrected E1/E2 estimates and clustered bootstrap variants; sensitivity reports | Remove primary inferential CI; six selected cohorts lack sampling frame; 435 pairs and method cells dependent; subset post hoc |
| Experimental provenance | **HOLD** | Saved partition/record grid internally matches IDs, seeds, sizes and split schedules per Loop 5.7; duplicate census now independently inspected | No authenticated execution commit/log/producer script, fit-to-cache digests, or resolution of exact duplicate-generation path |
| Reproducibility | **HOLD** | Fresh public clone at 29bcc Tier 1 aggregate arithmetic exits 0 | Tier 2 files absent; Tier 3 not run; no public Loop 5.8 release archive |
| Data rights | **HOLD** | Rights matrix enumerates 13 datasets and marks redistribution conservatively; Yale B restriction noted | Dataset-specific legal/attribution clearance for transformed inputs and partitions remains incomplete |
| Manuscript accuracy | **HOLD** | Separate FYP candidate reviewed claim-by-claim; proposed bounded abstract and availability text prepared | Exact target manuscript unavailable; bootstrap, seed schedules, scope, public availability and high-priority ancillary claims need correction/verification |
| DMKD submission readiness | **HOLD** | Material evidence and manuscript/package blockers remain | Resolve blockers listed in `unresolved_blockers.md` before submission |

## Direct answers

1. **Does the central stability–accuracy discordance result survive?** As a descriptive pattern in the six named biomedical cohorts under this exact saved protocol, yes: mean of 72 cell gaps is .464274 and median .448407. Each gap is a cell's mean stability (435 overlapping-sample pairwise ARIs) minus mean external ARI (30 label comparisons), averaged across cells. It is not a universal “excess reproducibility over validity” quantity or an independent-observation test.
2. **Are 4,320 partitions and fit records internally consistent?** Conditionally yes: Loop 5.7 found complete 6×12×2×30 grids and matching metadata/status/splits, and Loop 5.8 directly checked all duplicate groups and named payloads. 140 exact repeated digest groups cover 291 files; all matched successful Parquet rows. This does not exclude copy/overwrite or authenticate the fit event.
3. **Can historical execution provenance be authenticated?** No. The available protocol/source commits are not execution attestations; the actual partition-writing code/log and fit-to-cache hashes are missing.
4. **Are nine cells defensible as exploratory evidence?** Yes, with strong post-hoc qualification only. They are selected by Rule(i), Rule(i′), and recurrence of FCAG/FCM/FastMVC across three cohorts. Mean stability .683764, mean ARI −.002853, gap .686617. They are not independent confirmation. The “18 cells” statement is ambiguous: the recurrent-method-by-six-cohort set is not the 18 Rule(i′)-eligible cells.
5. **Is the bootstrap interval aligned with .485376?** No. .485376 is cell-weighted across 60 eligible cells. The archived [.379,.662] interval is equal-cohort bootstrap, centered near .499925. Corrected fresh seed-42 intervals are E1 cell-weighted [.377121,.644985] and E2 equal-cohort [.378581,.661716]; historical sequential RNG for E2 gives [.381104,.653002]. Remove interval from the primary manuscript; only retain as exploratory with exact estimand and six-cluster limitations.
6. **Are 3,000 benchmark rows independently reproducible from raw scores?** The local saved score rows were recalculated: 2,750 Pass F + 250 CoHiRF = 3,000, 13 datasets, 12 methods, 156 complete dataset-method cells; Friedman χ²=11.556213, df=11, p=.397908, ICC-v2 average rank 5.615385 (rank 4/12). This reproduces arithmetic, not fit execution. Seed schedules differ; exact Pass F generator is unresolved.
7. **Can a reviewer reproduce original experiments from a clean clone?** No. A fresh current-main clone ran Tier 1 aggregate arithmetic. Tier 2 partition files/caches and raw benchmark scores were absent; Tier 3 was not run.
8. **Are all manuscript claims supported?** No. The actual target manuscript is missing. The local FYP candidate includes unverified confirmatory, ablation, causal, scaling, mechanism, clinical, theoretical and superiority claims; see matrix and remaining-claims plan.
9. **What prevents submission?** Manuscript version not frozen; experiment provenance; unresolved duplicate producer lineage; primary bootstrap mismatch; seed/config mismatch; no public evidence package beyond aggregate arithmetic; rights clearance; unreviewed headline claims.
10. **Minimum remaining work?** Freeze the actual submission source and tables; apply bounded wording corrections; resolve or explicitly disclose provenance/duplicate uncertainty; remove the mismatched CI from primary claims; reconcile seed description; audit remaining abstract/conclusion claims from raw evidence; document rights; create a permitted immutable release and test its exact commit at tiers claimed. The FYP candidate claim matrix now has 81 coverage rows, including 62 explicitly marked not audited; this is not evidence that those additional result families passed review.

## Major finding status and confidence

| Finding | Status | Confidence | Evidence classification |
|---|---|---:|---|
| 72-cell aggregate gap calculations | VERIFIED | High numerical; conditional provenance | Local saved partition reconstruction vs saved summaries |
| Saved 4,320 partition and 4,320 fit grid authentic to claimed execution | UNVERIFIED | Moderate internal consistency; low historical authenticity | Local ignored/untracked evidence without producer logs/input digests |
| Three named duplicate payload identities and census | CONDITIONALLY VERIFIED | High on inspected local bytes | Dynamic byte hashes and array comparison; generation cause unresolved |
| Nine-cell values/membership | VERIFIED computationally; DESCRIPTIVE ONLY inferentially | High numeric, low confirmatory | Reconstructed subset, selected post hoc |
| Manuscript .485 point paired with [.379,.662] CI | CONTRADICTED | High | Bootstrap code, corrected outputs and equal-cell/equal-cohort estimands |
| 3,000-row Friedman arithmetic | VERIFIED from local saved scores | High arithmetic; conditional execution provenance | Raw local score CSVs, no fit attestation |
| Pass F seed generator identity | UNVERIFIED | High that rows use 0-based values; low on generator | Saved CSV vs conflicting extant source schedules |
| Public full reproduction | CONTRADICTED | High | Fresh clone has Tier 1 inputs only |
| Redistribution rights across all datasets | UNVERIFIED | Moderate | Conservative audit matrix; clearance not obtained |

## Final verdict

# **HOLD**

Numerical reconstruction strengthens the descriptive six-cohort observation, but does not cure execution provenance, inferential scope, versioned manuscript, legal, or public reproducibility blockers. Do not submit until required actions above are completed and re-audited.

