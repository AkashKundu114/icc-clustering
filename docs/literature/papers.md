# Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data

### Research Preparation Document - CSE_PROJECT_68

**Team:** Akash Kundu (Lead), Trinankur Guha, Rupankar Ghatak, Anubhav Naskar
**Mentor:** Prof. Kalyan Kumar Das

---

## PART A - PROJECT DECONSTRUCTION

The title has four load-bearing terms. Get each one precise before touching code.

**"Cluster Stability"** - Run a clustering algorithm many times under small perturbations (different random seeds, bootstrap resamples, feature subsets, added noise). If the same samples keep landing in the same groups, the clustering is *stable*; if assignments swing around, it's *unstable*. Stability is a proxy for "did we find a real structure, or did we just fit noise/initialization?" It is measured, not assumed - via pairwise agreement between repeated runs (a co-association / co-occurrence matrix), or via distance between partitions (e.g., Adjusted Rand Index between runs).

**"Ensemble Learning"** - applied here specifically as *ensemble/consensus clustering*: instead of trusting one clustering algorithm's output, generate many base clusterings (different algorithms, hyperparameters, feature subsets, samples) and fuse them into a single consensus partition that is more robust than any individual one.

**"Noisy Data"** - data corrupted by random feature noise, outliers, mislabeled points (if labels exist for evaluation), or irrelevant/redundant features. Noise degrades distance-based clustering because it distorts the geometry the algorithm relies on.

**"High-Dimensional Data"** - data with many features relative to samples, where the curse of dimensionality causes distances between points to concentrate (all pairwise distances become similar), making density- and distance-based clustering unreliable unless dimensionality is reduced or handled directly.

**Put together**, the title asks: *can we use measured cluster stability to build a better ensemble/consensus clustering, specifically in conditions of noise and high dimensionality where individual clustering algorithms are known to degrade?* That is a legitimate, non-trivial research question - not just "run K-Means then Random Forest."

Note the natural two-stage structure implied by the pipeline your mentor sketched: an **unsupervised stage** (stability-aware ensemble clustering) followed by an optional **supervised stage** (classification using cluster-derived labels/features). Don't assume the classification stage is core to the contribution - it may be a downstream validation step. Confirm this with your mentor; it's listed as an open decision in Part G.

---

## PART B - RESEARCH LANDSCAPE (What Already Exists)

**1. Clustering stability theory.** The foundational work is not about *combining* clusterings - it's about whether stability is even a valid signal of correctness. Ben-David, von Luxburg, and Pál's "A Sober Look at Clustering Stability" (COLT 2006) and von Luxburg's survey "Clustering Stability: An Overview" (*Foundations and Trends in Machine Learning*, 2010) show that for algorithms like k-means, stability is largely governed by the number of *symmetries/optimal solutions* of the objective function on that particular dataset - not purely by whether k is "correct." This is an important caution for your project: stability is a useful heuristic, not a guarantee of validity, and your literature review and discussion sections should acknowledge this rather than treat "more stable = more correct" as an axiom.

Ben-Hur, Elisseeff, and Guyon's "A Stability Based Method for Discovering Structure in Clustered Data" (Pacific Symposium on Biocomputing, 2002) is the classic resampling-based approach: cluster repeatedly on subsamples, compare pairs of runs, use the distribution of agreement scores to pick k or judge structure.

**2. Ensemble / consensus clustering.** The umbrella technique goes back to Strehl and Ghosh's "Cluster Ensembles - A Knowledge Reuse Framework" (JMLR, 2002) and Fred and Jain's evidence-accumulation approach, "Combining Multiple Clusterings Using Evidence Accumulation" (IEEE TPAMI, 2005), which introduced the now-standard **co-association matrix**: count, over many base clusterings, how often each pair of samples ends up in the same cluster, then cluster that similarity matrix itself to get the consensus. Vega-Pons and Ruiz-Shulcloper's "A Survey of Clustering Ensemble Algorithms" (*International Journal of Pattern Recognition and AI*, 2011) is the standard taxonomy paper dividing consensus functions into co-occurrence-based and median-partition approaches, and remains a widely cited entry point into the field.

**3. Stability-weighted / sample-weighted ensembles (most directly relevant).** This is exactly your mentor's suggested paper: Li, Qian, Wang, Dang, and Jing, "Clustering Ensemble Based on Sample's Stability" (*Artificial Intelligence*, vol. 273, 2019, pp. 37–55, DOI: 10.1016/j.artint.2018.12.007). Its core idea, explained in Part C below, is that not all samples contribute equally to a base clustering's agreement - some are consistently grouped ("core"), others flip between clusters across runs ("halo") - and treating them differently improves the consensus. A related, more recent line by the same/adjacent group is Zhou, Du, Liu, Shen, Fan, and Li's "Self-Paced Clustering Ensemble" (IEEE TNNLS, 2021), which similarly avoids treating all samples/base-clusterings equally, but by gradually incorporating "easy" instances first (curriculum-style) rather than a stability statistic. These two papers together frame the core tension your project can sit in: *how* should an ensemble decide which samples/clusterings to trust more?

**4. High-dimensional and noisy clustering.** The curse of dimensionality is well documented: as dimensionality grows, pairwise distances concentrate and lose discriminative power, which is why conventional k-means/hierarchical clustering degrades (see Parsons, Haque, and Liu's widely cited review "Subspace Clustering for High Dimensional Data," *SIGKDD Explorations*, 2004, and more recent treatments confirming the same mechanism). The standard mitigations are feature selection, feature extraction (PCA and successors), and subspace/projected clustering, each with real trade-offs your methodology section needs to justify rather than assume.

**5. Metaheuristic optimization for feature selection/clustering.** GA and PSO have both been used extensively for feature selection prior to clustering or classification, particularly in high-dimensional domains like microarray/gene-expression data and text. This is a well-populated but still active area - useful as an *optional* enhancement (e.g., PSO-optimized feature weighting or ensemble weighting) rather than a load-bearing novelty claim on its own, since "GA/PSO for feature selection" by itself is not new.

**What is comparatively under-explored** (this is where Part D's research gap should live): joint treatment of *sample-level stability* and *high-dimensional noise robustness* within the same ensemble-weighting scheme, with a systematic, controlled noise-level experiment (not just one fixed benchmark run) and a proper ablation isolating the contribution of stability-weighting versus dimensionality reduction versus base-clustering diversity.

---

## PART C - LITERATURE REVIEW TABLE (10–15 Papers)

| # | Paper | Year | Problem | Method | Dataset(s) | Metrics | Key Result | Limitation / Gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Li, Qian, Wang, Dang, Jing - *Clustering Ensemble Based on Sample's Stability*, Artificial Intelligence 273 | 2019 | Existing ensemble methods treat all samples equally despite unequal contribution | Defines sample stability via co-association; splits data into cluster "core" (stable) and "halo" (unstable); builds pre-structure from core, then assigns halo samples | 8 synthetic sets, 10 UCI real sets, 6 document datasets, image segmentation case study | Outperforms 12 state-of-the-art ensemble methods (statistically) | No explicit high-dimensionality or controlled-noise-level analysis; stability computed only at sample level, not jointly with feature-level noise |
| 2 | Zhou, Du, Liu, Shen, Fan, Li - *Self-Paced Clustering Ensemble*, IEEE TNNLS 32(4) | 2021 | Base clusterings/instances of unequal quality are all trusted equally in consensus learning | Curriculum-style self-paced learning: gradually includes harder samples/clusterings as training proceeds | Multiple benchmark datasets (per TNNLS venue norms) | Improved robustness vs. non-self-paced consensus baselines | Curriculum ("easy-to-hard") criterion is not the same construct as stability; no explicit dimensionality-robustness study |
| 3 | Zhou, Du, Li - *Self-Paced Consensus Clustering with Bipartite Graph*, IJCAI | 2020 | Scalability and robustness of consensus clustering | Bipartite graph formulation + self-paced sample selection | Benchmark datasets | Efficiency + robustness gains | Graph-based; different computational profile than co-association approaches |
| 4 | Strehl, Ghosh - *Cluster Ensembles: A Knowledge Reuse Framework*, JMLR 3 | 2002 | How to combine multiple partitions without access to original features/algorithms | Introduces consensus functions (CSPA, HGPA, MCLA) | Various | Establishes foundational framework | Predates stability-weighting and high-dimensional-noise focus entirely |
| 5 | Fred, Jain - *Combining Multiple Clusterings Using Evidence Accumulation*, IEEE TPAMI 27(6) | 2005 | Combining diverse clusterings into one robust partition | Evidence accumulation via co-association matrix, then re-cluster the matrix | Multiple datasets | Established the co-association matrix as a standard tool | No stability-based sample weighting; treats all evidence equally |
| 6 | Vega-Pons, Ruiz-Shulcloper - *A Survey of Clustering Ensemble Algorithms*, IJPRAI 25(3) | 2011 | Taxonomize the (by then) fragmented ensemble-clustering literature | Survey: co-occurrence-based vs. median-partition consensus functions | N/A (survey) | Standard reference taxonomy | Survey - no new method; now over a decade old, doesn't cover self-paced/deep-clustering-era work |
| 7 | Boongoen, Iam-On - *Cluster Ensembles: A Survey of Approaches with Recent Extensions and Applications*, Computer Science Review 28 | 2018 | Updated taxonomy including graph-based methods | Survey: direct, feature-based, pairwise-similarity, graph-based consensus functions | N/A (survey) | Broader four-category taxonomy | Survey - still pre-dates most stability-weighted and self-paced methods |
| 8 | Ben-David, von Luxburg, Pál - *A Sober Look at Clustering Stability*, COLT | 2006 | Whether stability is theoretically justified for model selection (choosing k) | Theoretical analysis of k-means stability vs. number of optimal solutions | Theoretical | Stability driven by data symmetries, not necessarily "true" k | Cautionary, not constructive - but essential for framing your stability claims honestly |
| 9 | von Luxburg - *Clustering Stability: An Overview*, Foundations and Trends in ML 2(3) | 2010 | Unify and explain the (technical) stability literature for practitioners | Survey connecting resampling-based and statistical-test-based stability estimation | N/A (survey) | Widely cited entry point to stability estimation methodology | Survey; notes the field lacks a thorough empirical comparison of stability estimators - an opening for your experimental section |
| 10 | Ben-Hur, Elisseeff, Guyon - *A Stability-Based Method for Discovering Structure in Clustered Data*, PSB | 2002 | Practical resampling-based stability estimation | Subsample repeatedly, compare pairwise cluster agreement | Gene-expression and other biological datasets | Established practical resampling protocol still used today | Predates ensemble/consensus integration - stability used only for model selection, not ensemble weighting |
| 11 | Parsons, Haque, Liu - *Subspace Clustering for High Dimensional Data: A Review*, SIGKDD Explorations 6(1) | 2004 | Distance concentration and irrelevance/redundancy in high-D clustering | Survey of subspace/projected clustering methods | N/A (survey) | Explains why conventional distance-based clustering fails in high-D | Survey; doesn't address ensemble or stability integration |
| 12 | Golalipour, Akbari, Hamidi, Lee, Enayatifar - *From Clustering to Clustering Ensemble Selection: A Review*, Engineering Applications of AI 104 | 2021 | Which base clusterings to *select* into an ensemble, not just how to combine them | Survey of ensemble selection strategies | N/A (survey) | Frames "selection" as distinct from "combination" - relevant if you frame stability as a *selection* criterion | Survey; doesn't test stability specifically as the selection criterion |
| 13 | Cheng, Li, Wang, Qian - *Deep Embedding Clustering Driven by Sample Stability*, IJCAI | 2024 | Extending sample-stability concept (from #1) into deep/embedding clustering | Deep clustering guided by pairwise co-association-derived stability | Image/embedding datasets | Shows the sample-stability concept generalizes beyond classic clustering | Deep-learning scope - heavier than an undergraduate project needs, but useful evidence the "stability" idea from paper #1 is still an active, extensible research direction |
| 14 | Mourer, Forest, Lebbah, Azzag, Lacaille - *Selecting the Number of Clusters K with a Stability Trade-off*, PAKDD | 2023 | Using stability jointly with internal validation to pick k | Internal validation criterion incorporating a stability trade-off | Benchmark datasets | New criterion combining validity + stability | Focused on model selection (choosing k), not ensemble construction |
| 15 | Golub et al. gene-expression clustering lineage / UCI high-dimensional benchmarks (background, not a single paper) | various | Real-world source of naturally high-dimensional, noisy, small-sample data (e.g., microarray) | - | Gene-expression / microarray datasets | - | Useful as a **candidate dataset family**, see Part F | - |

> This table is a starting scaffold, not exhaustive. Before Thursday, each team member should pull the actual PDF/abstract for at least 2–3 rows in their assigned area (Part I) and refine the Method/Result/Limitation columns from the primary source, not just this summary.

---

## PART D - RESEARCH GAP CANDIDATES

| Gap | Novelty | Feasibility (UG team, 1 semester) | Complexity | Research Value | Publication Potential | Score (1–5 each, sum) |
| --- | --- | --- | --- | --- | --- | --- |
| **G1. Joint sample-stability + dimensionality-robustness weighting for ensemble clustering** - extend Li et al. (2019)'s core/halo stability idea by testing and adapting it explicitly across controlled noise levels *and* dimensionality regimes, which the original paper does not systematically vary | 4 | 4 | 3 | 4 | 3 | **18/25** |
| G2. Stability-guided *feature selection* before ensemble clustering (use stability of clusterings under different feature subsets to select features, not just samples) | 4 | 3 | 4 | 4 | 3 | 18/25 |
| G3. PSO/GA-optimized ensemble weighting driven by a stability-based fitness function (instead of hand-crafted stability weights) | 3 | 3 | 4 | 3 | 3 | 16/25 |
| G4. Multi-level stability (sample-level *and* cluster-level *and* model-level, evaluated jointly rather than one level at a time) | 5 | 2 | 5 | 4 | 3 | 19/25 (highest novelty, but hardest to execute well in one semester) |
| G5. Reproduce Li et al. (2019) faithfully, then extend only with a systematic noise-injection experiment (0/5/10/20/30%) across low/medium/high-dimensional datasets, reporting where stability-based weighting helps vs. breaks down | 3 | 5 | 2 | 3 | 3 | 16/25 (lowest risk, high feasibility) |

**Recommendation: G1**, with **G5's experimental discipline** folded in as the evaluation protocol. Concretely: take the core/halo sample-stability mechanism from Li et al. (2019) as your base method, and contribute a systematic empirical (and where feasible, mechanistic) study of how sample-stability weighting behaves as you dial up (a) feature noise and (b) dimensionality - something the original paper's eight synthetic + sixteen real datasets don't explicitly parameterize. This is defensible (not a fake "first-ever" claim - it's "we extend and stress-test an existing mechanism under conditions the original paper didn't isolate"), technically feasible on student hardware, and gives you a natural ablation study (Part 13 of your mentor's brief) almost for free, since "with vs. without stability weighting, at each noise/dimensionality level" *is* the experiment.

G4 (multi-level stability) is the more ambitious, more novel option - flag it to your mentor as a stretch goal or future-work item rather than the core semester deliverable, since it's the kind of scope that risks displacing rigor for breadth.

---

## PART E - PROPOSED METHODOLOGIES

### Methodology 1 - Stability-Weighted Ensemble with Controlled Noise/Dimensionality Study (recommended)

1. Generate diverse base clusterings (K-Means, FCM, DBSCAN, Hierarchical) across bootstrap resamples, random seeds, and feature subsets.
2. Compute sample-level stability via a co-association matrix (fraction of base clusterings placing a pair of samples together), following Li et al.'s core/halo formulation.
3. Build the consensus clustering using core samples first, then assign halo samples - matching the original paper's mechanism as the *baseline* you extend.
4. **Your contribution:** systematically vary injected noise (0/5/10/20/30%) and dimensionality (low/medium/high, via natural datasets and/or synthetic feature padding) and measure how stability-weighting's advantage over unweighted ensembles changes across this grid. Report where the method helps, where it stops helping, and why (tie back to distance-concentration theory from Part B).
5. Optional downstream step: use the final consensus clusters as pseudo-labels or cluster-derived features for a classification stage (KNN/DT/RF/SVM), to demonstrate practical utility - but treat this as secondary validation, not the main contribution.

*Pros:* Directly buildable from a well-specified, peer-reviewed base paper; produces a genuine ablation almost automatically; realistic scope.
*Cons:* Novelty is "systematic extension," not a brand-new algorithm - needs to be argued carefully and honestly in the paper's contribution statement.

### Methodology 2 - Stability-Guided Feature Selection Before Ensemble Clustering

Use stability (how consistently a feature subset produces similar clusterings under resampling) as the *selection criterion* for features, before running the ensemble - i.e., stability drives dimensionality reduction rather than (or in addition to) sample weighting.
*Pros:* Attacks the "high-dimensional" part of the title more directly.
*Cons:* Feature-stability estimation is more computationally expensive (needs many reclustering runs per candidate feature subset) and has less direct precedent to build from - higher implementation risk for a one-semester team.

### Methodology 3 - Metaheuristic-Optimized Stability-Weighted Ensemble

Same as Methodology 1, but replace hand-crafted stability-weight formulas with a PSO- or GA-optimized weighting scheme, using a stability+validity composite fitness function.
*Pros:* Directly uses the GA/PSO material your mentor asked you to study; adds an optimization angle.
*Cons:* Adds a second, fairly heavy moving part (metaheuristic search) on top of an already nontrivial ensemble pipeline - real risk of the project sprawling past what four undergrads can rigorously evaluate in one semester. Per your mentor's own instruction ("do NOT force a metaheuristic algorithm into the project simply because it's on the prep list"), treat this as an optional stretch extension layered onto Methodology 1 *only if* time permits after the core noise/dimensionality study is done and evaluated.

### Recommendation

Start with **Methodology 1**. Keep Methodology 3's PSO-weighting idea in your back pocket as an ablation arm ("does optimized weighting beat our stability formula?") if the core system is solid with time to spare - don't commit to it up front.

---

## PART F - EXPERIMENTAL DESIGN

**Baselines:** individual K-Means, individual FCM, individual DBSCAN, individual Hierarchical clustering; unweighted ("vanilla") clustering ensemble (equal-weight consensus, Fred & Jain-style evidence accumulation); Li et al. (2019)'s original stability-weighted method (reimplemented as closely as feasible) as the direct comparator for your extension.

**Noise models:** Gaussian feature noise at controlled variance, random feature corruption, and injected outlier points, at 0/5/10/20/30% severity - but confirm with your mentor whether all three noise *types* are in scope, or whether one (e.g., Gaussian feature noise) is a more defensible, cleaner starting point than mixing types.

**Dimensionality regimes:** low-dimensional (e.g., Iris-scale, ~4–20 features), medium (~50–100 features), high (~500+ features or genuinely high-dimensional domains like gene-expression/microarray data, which are a natural, academically recognized fit for "noisy high-dimensional" - see dataset table below).

**Metrics:** internal - Silhouette, Davies-Bouldin, Calinski-Harabasz; external (when ground-truth labels exist, which they do for most UCI benchmark classification datasets repurposed for clustering) - Adjusted Rand Index, Normalized Mutual Information, Purity; classification-stage (if included) - Accuracy, Precision, Recall, F1, ROC-AUC.

**Statistical validation:** run each configuration ≥10–30 times with different seeds/resamples; report mean ± standard deviation; use a paired test (e.g., Wilcoxon signed-rank, which is standard practice in this exact sub-literature - see Taheri & Hesamian's work on the Wilcoxon signed-rank test cited in recent ensemble-clustering papers) across datasets/runs rather than eyeballing single-run numbers.

**Candidate datasets** (compare on samples/features/classes/noise-controllability before committing):

| Dataset family | Dimensionality | Notes |
| --- | --- | --- |
| Classic UCI sets (Iris, Wine, Breast Cancer Wisconsin, etc.) | Low | Good for sanity-checking pipeline correctness and low-D baseline |
| UCI mid-size sets (e.g., Ionosphere, Sonar, Madelon) | Medium–high | Madelon in particular is explicitly designed with irrelevant/noisy features - strong fit for your noise experiments |
| Gene-expression / microarray benchmarks (e.g., from OpenML or curated bioinformatics repositories) | High (often thousands of features, few hundred samples) | Naturally noisy and high-dimensional; academically standard for this exact research area (used repeatedly in the feature-selection/clustering literature you searched) |
| Document/text datasets (e.g., 20 Newsgroups subset, TF-IDF features) | High | Matches the "6 document datasets" precedent in Li et al. (2019) |
| Image-feature datasets (e.g., extracted CNN embeddings or classic image-segmentation benchmarks) | Medium–high | Matches the image-segmentation case study precedent in Li et al. (2019) |

Do not finalize dataset choices without checking real sample counts/feature counts/license terms directly on UCI/OpenML - the table above is a starting shortlist, not a final decision.

**Ablation studies:** with/without stability weighting; with/without feature selection or dimensionality reduction; single algorithm vs. multi-algorithm ensemble; equal weights vs. stability-based weights; across each noise level and each dimensionality regime independently, so you can attribute effects correctly instead of conflating them.

---

## PART G - THURSDAY MEETING PREPARATION

**2-minute explanation:** "Our project builds on prior work showing that some data samples are more reliably clustered than others across repeated runs - this is called sample stability. We're extending a specific published method that uses this stability to build a more robust consensus clustering, by systematically testing how well the approach holds up as we increase noise and dimensionality - two conditions where standard clustering is known to break down but that the original paper doesn't isolate directly. We'll validate with an ablation study across multiple clustering algorithms and multiple public datasets, and optionally add a classification stage on top of the final clusters."

**5-minute explanation:** Expand each of the above into: (1) motivation - why clustering results vary and why that matters, (2) the specific gap in Li et al. (2019) our project targets, (3) our planned pipeline (noise/feature preprocessing → multiple base clusterings → stability estimation → weighted consensus → optional classification), (4) our evaluation plan (baselines, ablations, statistical validation), (5) what we still need the mentor's guidance on (Part below).

**Likely mentor questions:**

- Why is stability a meaningful signal, given the known critique (Ben-David et al.) that stability can reflect data symmetry rather than "true" structure?
- Why these four clustering algorithms specifically, and is DBSCAN's parameter sensitivity going to be a problem in your noise experiments?
- How will you avoid data leakage if you use labels for external validation (ARI/NMI) while claiming an unsupervised method?
- Is the classification stage central to your contribution, or incidental?
- Which specific dataset(s) will you commit to, and why?
- What exactly is new versus what is reproduced from Li et al. (2019)?

**Questions your team should ask the mentor:**

- Should the classification stage (KNN/DT/RF/SVM) be a core contribution, or an optional downstream demonstration?
- Is reproducing Li et al. (2019) as a baseline, then extending it, an acceptable scope - or does he expect a more original mechanism?
- Any dataset restrictions (must it be gene-expression/bio data, given the original "AI-based disease prediction" allotment)?
- Is a metaheuristic (GA/PSO) component expected, or optional?
- Preferred venue/format for the eventual paper (conference-style vs. journal-style), which affects how much space you'll have for the literature review and ablations.

**Decisions NOT to finalize before the meeting:** final dataset(s); whether classification is core or optional; whether GA/PSO weighting is in scope; exact noise-injection protocol; final research-gap statement (present G1 as your leading option, but let the mentor confirm/redirect).

---

## PART H - LEARNING ROADMAP

**MUST KNOW (before Thursday):**

- K-Means, FCM, DBSCAN, Hierarchical clustering - intuition, procedure, key hyperparameters, sensitivity to noise/high-D
- Internal metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz) and external metrics (ARI, NMI, Purity) - what each measures and higher/lower-is-better
- What cluster stability means and how it's estimated (resampling/co-association)
- What consensus/ensemble clustering means and why it helps
- Curse of dimensionality - why it degrades distance-based clustering
- The core mechanism of Li et al. (2019): core/halo sample stability

**SHOULD KNOW (this week, not necessarily by Thursday):**

- GMM, Spectral clustering - enough to discuss why they weren't chosen as primary base clusterers, if asked
- GA/PSO/ACO - core intuition (search space, fitness function, exploration vs. exploitation) even if not yet in your methodology
- KNN, Decision Tree, Random Forest, SVM - core mechanics, for the optional classification stage
- Bagging/boosting/voting/stacking as general ensemble concepts, to contrast with cluster ensembles specifically

**OPTIONAL (background depth, pursue after the meeting once scope is confirmed):**

- Deep embedding clustering extensions of sample stability (Cheng et al., 2024)
- Self-paced clustering ensemble as an alternative weighting philosophy
- Formal stability theory (Ben-David/von Luxburg) beyond the practical takeaway

---

## PART I - TEAM WORK DISTRIBUTION (tentative - do not lock in before mentor confirms scope)

**Akash Kundu (Lead):** overall architecture, mentor coordination/documentation, integration of all modules, final consensus-clustering + core/halo implementation (the heart of Methodology 1), repo/version-control setup.

**Trinankur Guha:** clustering algorithms module - implement and characterize K-Means, FCM, DBSCAN, Hierarchical (hyperparameter behavior, noise/dimensionality sensitivity notes for the literature review), plus internal/external evaluation metrics module.

**Rupankar Ghatak:** noise-injection and dimensionality-regime experimental harness - build the controlled noise-level (0/5/10/20/30%) and dimensionality-regime (low/medium/high) experiment grid, dataset preprocessing, and statistical validation (mean/std, Wilcoxon tests) reporting pipeline.

**Anubhav Naskar:** literature review deep-dive (own the paper table in Part C, pull primary sources, keep it current) plus the optional classification stage (KNN/DT/RF/SVM) and its evaluation metrics, so the pipeline's downstream half has a clear owner.

*Revisit this division after the mentor meeting - some responsibilities (e.g., whether GA/PSO or feature-selection-driven stability get added) depend directly on what your mentor confirms as in-scope.*

---

## PART J - PROJECT ROADMAP

1. **Weeks 1–2:** Literature review deepened (primary sources for all 15 papers), research gap finalized with mentor sign-off after Thursday's meeting.
2. **Weeks 3–4:** Methodology finalized in detail (exact stability formula, exact consensus mechanism), dataset(s) finalized, architecture/repo scaffolding built.
3. **Weeks 5–7:** Baselines implemented (individual algorithms, unweighted ensemble, reimplemented Li et al. 2019 method) and sanity-checked on low-dimensional data.
4. **Weeks 8–10:** Core extension implemented (noise/dimensionality-controlled experiment grid), first full experimental runs.
5. **Weeks 11–12:** Ablation studies executed; statistical validation (repeated runs, significance tests).
6. **Weeks 13–14:** Optional classification stage (if confirmed in scope); robustness/explainability visualizations.
7. **Weeks 15–16:** Research paper drafting (Abstract → Conclusion), documentation, presentation prep, final polish and demo.

Do not begin Week 5 implementation before Weeks 1–4 (research gap + methodology) are mentor-approved - this is the single most important sequencing rule in your mentor's own brief, and it's worth protecting even under deadline pressure.

---

## References (as gathered - verify DOIs/links directly before citing in your paper)

1. Li, F., Qian, Y., Wang, J., Dang, C., & Jing, L. (2019). Clustering ensemble based on sample's stability. *Artificial Intelligence*, 273, 37–55. <https://doi.org/10.1016/j.artint.2018.12.007>
2. Zhou, P., Du, L., Liu, X., Shen, Y.-D., Fan, M., & Li, X. (2021). Self-paced clustering ensemble. *IEEE Transactions on Neural Networks and Learning Systems*, 32(4), 1497–1511. <https://doi.org/10.1109/TNNLS.2020.2984814>
3. Zhou, P., Du, L., & Li, X. (2020). Self-paced consensus clustering with bipartite graph. *IJCAI 2020*. <https://doi.org/10.24963/ijcai.2020/295>
4. Strehl, A., & Ghosh, J. (2002). Cluster ensembles - a knowledge reuse framework for combining multiple partitions. *Journal of Machine Learning Research*, 3, 583–617.
5. Fred, A. L., & Jain, A. K. (2005). Combining multiple clusterings using evidence accumulation. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 27(6), 835–850. <https://doi.org/10.1109/TPAMI.2005.113>
6. Vega-Pons, S., & Ruiz-Shulcloper, J. (2011). A survey of clustering ensemble algorithms. *International Journal of Pattern Recognition and Artificial Intelligence*, 25(3), 337–372.
7. Boongoen, T., & Iam-On, N. (2018). Cluster ensembles: a survey of approaches with recent extensions and applications. *Computer Science Review*, 28, 1–25.
8. Ben-David, S., von Luxburg, U., & Pál, D. (2006). A sober look at clustering stability. *COLT 2006*, LNCS 4005, 5–19.
9. von Luxburg, U. (2010). Clustering stability: an overview. *Foundations and Trends in Machine Learning*, 2(3). Also arXiv:1007.1075.
10. Ben-Hur, A., Elisseeff, A., & Guyon, I. (2002). A stability based method for discovering structure in clustered data. *Pacific Symposium on Biocomputing*, 7, 6–17.
11. Parsons, L., Haque, E., & Liu, H. (2004). Subspace clustering for high dimensional data: a review. *ACM SIGKDD Explorations*, 6(1).
12. Golalipour, K., Akbari, E., Hamidi, S. S., Lee, M., & Enayatifar, R. (2021). From clustering to clustering ensemble selection: a review. *Engineering Applications of Artificial Intelligence*, 104, 104388.
13. Cheng, Z., Li, F., Wang, J., & Qian, Y. (2024). Deep embedding clustering driven by sample stability. *IJCAI 2024*, 3854–3862.
14. Mourer, A., Forest, F., Lebbah, M., Azzag, H., & Lacaille, J. (2023). Selecting the number of clusters K with a stability trade-off: an internal validation criterion. *PAKDD 2023*, LNCS 13935.

*Note: this list was compiled via web search of Google Scholar-indexed sources and publisher pages; treat it as a verified starting bibliography, but re-confirm each DOI/venue against the primary source before final submission - citation accuracy is your responsibility, not something to take on faith from any secondary summary, including this one.*
