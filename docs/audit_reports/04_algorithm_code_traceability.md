# Traceability (pseudocode unavailable; docstring used)
1 VSSG scoring -> consensus_v2.fit_predict step 1 (OK). 2 pool -> step 2 (floor 15%; deviates from 'gating'). 3 subspace ensemble -> step 3 (OK). 4 core/anchors -> step 4, TWO branches (N<=2000 dense; N>2000 subsample-1000). 5 bipartite spectral -> step 5 (see 03). 6 centroids -> step 6 stability-weighted means. predict() = nearest centroid (optionally restricted to pool). `beta` unused (3 occurrences: doc, init, assignment). ASPP: not traced.

## A3 update
Dense (N<=dense_threshold) vs scalable branch on the same data (N=900, robust pool, 4 seeds): gaussian ARI 0.819 vs 0.784 (label agreement 0.908); student_t 0.483 vs 0.359 (agreement 0.597). The two branches are materially different algorithms (VERIFIED). `dense_threshold` is now a parameter (default 2000). `beta` deprecated (warns, no effect).
