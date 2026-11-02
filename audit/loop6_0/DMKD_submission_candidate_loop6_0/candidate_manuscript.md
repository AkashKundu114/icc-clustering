# Stability and external reference alignment in six biomedical clustering cohorts: a saved-partition reconstruction

**Loop 6.0 conservative candidate — not submission-ready.** This candidate narrows the research question to the evidence that Loop 5.9 reconstructed. It is not a substitute for author approval, full supplementary evidence review, or a fresh historically traceable experiment. The target canonical file was SHA-256 `A0C4274EC5DFBB40311D3D33D7AD8179B17DEE145851FD2E5B255E498054E75F` at baseline.

## Abstract

Clustering stability and external reference alignment describe different properties: agreement under perturbation does not by itself establish agreement with externally supplied categories. We examined their relationship in six high-dimensional biomedical cohorts (CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT) using a recovered set of 4,320 saved subsample partitions for 12 methods. For each cohort-method cell, resampling stability was the mean adjusted Rand index (ARI) over 435 pairwise comparisons on the samples shared by each pair of partitions; external alignment was the mean ARI to reference labels over 30 subsamples. Recalculation from the saved partition arrays yielded mean cell stability 0.516586 and mean external ARI 0.052312 across 72 cells. Their difference, averaged across cells, was 0.464274; the median cell difference was 0.448407. These are descriptive summaries of distinct metrics, not independent-observation estimates or a calibrated measure of validity. The resampling design used reference-label-stratified sampling and reference-derived cluster counts, and the historical producer of the recovered outputs could not be authenticated. Thus the results show that high pairwise agreement under this particular saved-output protocol can coexist with low alignment to the available reference labels in these cohorts; they do not establish label-blind robustness, initialization robustness, biological reproducibility, or population-wide generality.

## 1. Introduction

Clustering is often applied when class labels are absent or incomplete, making stability under data perturbation an appealing diagnostic. Yet stability and external validation answer different questions. Stability asks whether a procedure returns similar partitions after a specified perturbation. External validation asks whether a partition aligns with a chosen reference classification. Neither property entails the other: a stable partition can reflect structure that is not represented by the available reference labels, while a useful external alignment need not imply that the partition is insensitive to sampling.

This distinction is not a new general hypothesis. Amorim and Cardoso compared clustering stability with recovery of known clusters in controlled numerical experiments, and Hennig showed that stable clusters can arise from method inflexibility and that cluster-wise interpretation matters. A review by Liu et al. surveys stability estimation and its challenges. The contribution here is narrower: a descriptive reconstruction of the relationship between one pairwise subsample-agreement measure and reference-label ARI across six biomedical cohorts under the specific saved protocol audited here. We do not claim that the relationship has not previously been studied.

The paper asks: under this protocol, can agreement among resampled partitions coexist with poor alignment to the cohort reference labels? The answer is assessed at the level supported by saved data. The analysis is not a comparison establishing superiority of ICC or any other method.

## 2. Data and experimental records

The six cohorts are CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT. Twelve method labels appear in the recovered results, yielding 72 cohort-method cells. The archived protocol records 30 without-replacement 80% class-stratified subsamples per cohort, with shared subsample schedules across methods, repeat seeds 5000–5029, null seeds 6000–6029, and a fixed model seed of 0. The real and column-permuted arms share split indices. The saved matrices, sample identities, preprocessing lineage, and producer execution trace were not sufficient to authenticate the historical model invocations.

Reference labels influenced the experiment: they were used to stratify subsamples and to set the requested cluster count. Therefore these results do not estimate performance under a fully label-blind pipeline. The labels are external evaluation references, not complete biological truth; low ARI means low agreement with those labels under the stated metric.

## 3. Measures and reconstruction

For a cohort-method cell with 30 saved partitions, let each partition contain assignments and the indices of the samples it represents. For every one of the 435 unordered pairs of partitions, assignments were restricted to the intersection of their sample indices, and ARI was computed on that intersection. The mean of these pairwise ARIs is termed **pairwise subsample stability**. Since partitions, sample subsets, and observations recur across comparisons, the 435 values are dependent. This statistic concerns sensitivity to the observed row-subsampling procedure; the fixed model seed does not test initialization robustness.

For each saved real-mode partition, ARI was calculated between predicted assignments and reference labels for the corresponding sampled observations. The mean over 30 draws is termed **external reference alignment**. This is paired at the protocol level through shared cohort, method, and sampled observations, but it is not a one-to-one pairing of one stability value to one external ARI draw: stability is one summary over 435 pairs, whereas external alignment averages 30 partition-to-label comparisons.

A cell-level descriptive difference is stability minus external ARI. Because it subtracts averages with different comparison populations and interpretations, we report it as an arithmetic contrast, not as a universal “excess reproducibility” scale. No cell-level iid test, pair-level significance test, or confirmatory confidence interval is used.

The Loop 5.9 reconstruction script independently loaded the local partition arrays and per-fit records and regenerated the 72 cells. It reported 30 real and 30 null repeats per cell, 435 pairwise ARIs per mode, and no validation errors; maximum cell-level discrepancies against stored summaries were at floating-point rounding scale (stability 1.11e-16; external ARI 9.71e-17; null stability 9.92e-17). This is saved-output reconstruction, not rerunning the models.

## 4. Results

Across 72 cohort-method cells, mean pairwise subsample stability was 0.516586, mean external ARI was 0.052312, and the mean of the 72 cell-wise differences was 0.464274. The median cell-wise difference was 0.448407. The mean null-arm stability was 0.006620. The mean summaries weight each of the 72 cells equally. Because each cohort contributes 12 cells, those means also give each of the six cohorts equal total weight. The median is calculated across the 72 cell differences. Cohort-level averages (each averaging 12 method summaries) are provided in `cohort_descriptives.csv` to expose heterogeneity rather than imply independent replication. The largest cohort-average difference is observed in Prostate, while Leukemia and SRBCT have higher cohort-average external ARI; the overall pattern is not uniform across cohorts.

The post-hoc non-degeneracy analysis is not part of the primary result. Rule (i) selected 20 cells; Rule (i-prime), which additionally required a minimum cluster proportion of 5% in at least 27 of 30 repeats, selected 18; a recurrence rule selected nine cells across three methods. These thresholds were not prespecified. The nine-cell means (stability 0.683764, external ARI -0.002853, difference 0.686617) are therefore exploratory and selection-conditioned. They are not independent confirmation and should be relegated to supplementary material or omitted. The Rule (i-prime) set must not be confused with all cohort-method cells belonging to recurring methods.

## 5. Discussion

The saved outputs support a bounded observation: in these six cohorts and under this particular resampling protocol, the average pairwise agreement among partitions was appreciably higher than their average ARI to the available reference labels. This illustrates why stability should not be interpreted as a stand-alone validation criterion. It does not show that stability is generally useless, that the labels capture every meaningful structure, or that the same relation holds in new cohorts.

Several design features narrow interpretation. Label-informed stratification affects which samples enter each draw, and label-derived K supplies information about the intended number of groups. A fixed model seed isolates neither initialization sensitivity nor full algorithmic variability. The cohorts are a small, non-probability sample; method-by-cohort cells and pairwise comparisons are dependent. In addition, the original partition-writing producer and historical execution lineage could not be recovered, and 140 cross-cell duplicate-hash groups remain unexplained. Numerical reconstruction confirms consistency of the files with the stored aggregates, but not authenticity of the historical fits.

The separate 13-dataset benchmark evaluates saved external-ARI score rows and is not a 13-dataset stability experiment. It should not be used to enlarge the scope of the stability result or to claim ICC superiority. Benchmark scores have seed-schedule and method-fidelity limitations documented separately in the audit.

## 6. Limitations and conclusion

This analysis is descriptive, based on six biomedical cohorts and locally recovered saved outputs. It lacks authenticated original execution logs, a recovered partition producer, and a public Tier 2 reproduction package. The sampling and K choices use reference labels; the fixed model seed addresses neither initialization robustness nor biological replication. Reference labels are incomplete operational standards, and ARI does not establish clinical utility.

Under the examined protocol, resampling agreement and external reference alignment were distinct: average agreement among subsampled partitions coexisted with low average agreement to the supplied reference labels. This observation motivates reporting stability alongside external validation and degeneracy checks. Independent confirmation requires a prospective, traceable experiment with immutable inputs, complete execution logs, and an appropriate cohort-level design.

## Data availability

The current public repository supports aggregate arithmetic checks only. The recovered partitions, per-fit records, caches, and raw benchmark score files used for this reconstruction are not present in a clean public clone. No claim of full experimental reproduction or redistribution of third-party data is made. Dataset access and terms must be obtained from the original providers.

## Code availability

The public repository contains the aggregate verification script. Partition-level reconstruction requires local files not included in the current public release, and a full fit-level reproduction workflow was not recovered. Loop 6.0 audit scripts and candidate outputs have not yet been publicly released. See the audit package for exact limitations.

## References (verification pointers; format and complete bibliographic details require editorial verification)

1. Amorim, M. J., and M. G. M. S. Cardoso. 2015. “Clustering Stability and Ground Truth: Numerical Experiments.” In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 1: KDIR*, 259–264. DOI: 10.5220/0005597702590264.
2. Hennig, C. (2007). “Cluster-wise assessment of cluster stability.” *Computational Statistics & Data Analysis*, 52(1), 258–271. DOI: 10.1016/j.csda.2006.11.025.
3. Liu, T., H. Yu, and R. H. Blair. 2022. “Stability estimation for unsupervised clustering: A review.” *Wiley Interdisciplinary Reviews: Computational Statistics* 14(6): e1575. DOI: 10.1002/wics.1575.

**Candidate boundary:** this text intentionally omits the manuscript’s GAC ablations, synthetic causal language, scalability, Prostate mechanism, theory, marker-recovery and broad benchmark claims because Loop 5.9 did not independently verify those workstreams. It is an evidence-bounded replacement candidate, not a fully validated submission package.
