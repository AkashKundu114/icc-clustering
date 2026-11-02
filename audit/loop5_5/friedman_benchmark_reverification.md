# 13-dataset Friedman benchmark reverification

Independently recalculated from local `results/evidence_recovery/recovered/results.json` by the Loop 5.5 script. Filtering `experiment == exp3_1` and `metric_name == ari` yields 1,430 observations, exactly 13 datasets × 11 methods × 10 distinct seeds. There are 143 dataset–method cells, 10 observations each, no duplicate dataset–method–seed keys, and ten config hashes corresponding to the ten seeds. Every row carries source commit `879fd96a282e88f5491826dd7355d24d9490661b`.

Within each dataset–method cell, the ten ARIs are averaged. Friedman is applied across the 13 dataset-level mean scores per method; rankings are descending ARI with average ranks for ties. Recomputed statistic 11.342657, df=10, p=0.331452. ICC_v2 average rank is 5.4615, fifth of 11. This independently supports the stated 11-method numerical result from raw run records, conditional on the validity/comparability of those underlying benchmark runs.

The rows contain no assignments, explicit labels, resampling configuration, or data hashes. Seed equality across methods is visible, but this does not establish paired initialization or identical preprocessing. The methods and datasets span different domains and K values. Friedman rank inference treats datasets as blocks; 13 heterogeneous benchmark datasets do not establish a general population law. Report as exploratory benchmark comparison.

The 12-method Table 6 statistic cannot be recomputed because raw observations for CoreHalo/CoHiRF across seven additional datasets are absent. Any stored summary statistic remains unverified. Keep this result separate from the 6×12 stability analysis.
