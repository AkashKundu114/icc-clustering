# Numerical consistency report

## Six-cohort reconstruction

Lead and independent Agent F directly recomputed the saved six-cohort arrays; Agent B independently implemented a separate reconstruction script and the lead reran it. All yield 72 cells, 2,160 external ARIs, 31,320 real and 31,320 null pairwise intersection ARIs, 4,320 partitions and 4,320 corresponding one-row records. No partition/Parquet key, status, or split-index mismatch was found. Maximum difference versus historical summary: stability 1.11e-16; external ARI 9.71e-17; null stability 9.92e-17. Mean stability 0.5165860621, mean external ARI 0.0523121822, mean cell difference 0.4642738799, median cell difference 0.4484068169, mean null stability 0.0066196808.

## Subsets and sensitivity

The raw selection calculations recover Rule(i)=20, Rule(i-prime)=18, recurrence Rule(iii)=9. Nine-cell summary is post-hoc. Sensitivity varies cluster threshold and 27/30 vs 30/30 repeat requirement; results remain exploratory. Leave-one-cohort-out mean gap ranges from 0.3983408 (omit Prostate) to 0.4972999 (omit Leukemia); direction remains positive in all six exclusions, while magnitude is cohort-influenced. This is descriptive influence analysis, not proof of generalization.

## Benchmark

Saved score recalculation from Pass F and CoHiRF source CSVs yields 3000 rows, 13 datasets, 12 methods, 156 complete cells, zero duplicate dataset-method-seed keys; Friedman Q=11.5562130178, df=11, p=0.3979076148; ICC-v2 average rank 5.6153846154. This is not proof of 3000 unique fit events.

## Caveats

All primary reconstructed values are arithmetic over local saved evidence, not fresh clustering fits. Reference labels informed sampling and K. Pairwise observations are dependent. The weighted wording correction in the candidate was made after Agent F's review and its static checker was rerun.
