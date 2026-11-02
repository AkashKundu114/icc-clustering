# Benchmark scope consistency

The 13-dataset benchmark evaluates external ARI performance and is distinct from the six-cohort resampling stability analysis. The manuscript's stability section generally names six cohorts, but abstract/conclusion juxtaposition with the broad benchmark risks readers inferring that discordance was tested across 13 datasets. State explicitly that only six biomedical cohorts enter the stability–accuracy analysis.

Loop 5.5/previous source inspection reports 13×11=143 benchmark cells and 10 observations each (1,430 core fits), Friedman statistic 11.3427, df=10, p=0.33145, ICC-v2 rank 5/11. Those raw observations were not recovered in the FYP stability package and are outside this recomputation. The manuscript's 3,000-fit statement and 12-method Friedman p≈0.40 remain unverified; raw CoreHalo and CoHiRF observations are missing. Do not call the 11-method result a reproduction of the 12-method table. The stability analysis has 12 methods × 6 cohorts ×30 repeats and evaluates another estimand.

No verified evidence supports “stability across all 13 datasets” or an ICC superiority claim. Keep table/figure labels and conclusions distinct by dataset set, method set, and outcome.
