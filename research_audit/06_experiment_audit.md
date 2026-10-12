# Experiment audit
Exp3: see 02. Run-level seeds, deterministic baselines have 0 variance; unit of analysis must be dataset (n=13). True K given to all methods.
A2 results (research_audit/results, scripts/): synthetic N=240,D=2000,5 seeds: legacy ICC ARI~0.00 (gauss/scaled/corr), robust-MAD pool ICC 0.57-0.86, but BC-filter+KMeans on same pool = 1.000 (consensus HURTS here); student_t: ICC_robust 0.735 vs KM_pool 0.149 (ensemble helps); sparse noise: all ~0 (gate fails).
Real cached (5 seeds): legacy mean ARI 0.167, robust 0.031, gauss 0.121; tightening the pool destroys Leukemia/SRBCT gains.
Controls (10 seeds): Leukemia KM_all 0.210, ICC_legacy 0.709+-0.267, random-pool ICC 0.198, BC-top15%+KM -0.040, var-top15%+KM 0.231. SRBCT: KM_all 0.053, ICC_legacy 0.566+-0.084, random pool 0.085, BC-filter+KM 0.422. Colon ICC 0.083 vs ~0; CNS ~0.
Reading: BC ranking is the operative ingredient on SRBCT (filter alone gets 0.42); on Leukemia the subspace-consensus step adds beyond the filter. Mechanism is NOT 'isolating informative dims' (tight pools fail). n=2 winning datasets: needs more datasets and strong FS baselines before any claim.
