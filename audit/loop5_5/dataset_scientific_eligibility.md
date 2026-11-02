# Scientific eligibility decisions

Decisions concern whether a dataset can support the primary biological stability–accuracy analysis with current evidence. No additional dataset qualifies because matched resampling stability is absent. A numerical class label does not make a dataset biological ground truth.

| Dataset | Decision | Reason |
|---|---|---|
| CNS | ELIGIBLE FOR PRIMARY ANALYSIS | Biomedical diagnostic reference; already in six-cohort aggregate analysis. Raw repeats/IDs remain unavailable. |
| Colon | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor/normal biomedical reference; already included. |
| Leukemia | ELIGIBLE FOR PRIMARY ANALYSIS | ALL/AML diagnostic reference; already included. |
| Ovarian | ELIGIBLE FOR PRIMARY ANALYSIS | Case/control biomedical reference; already included, with proteomic rather than microarray features. |
| Prostate | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor/normal biomedical reference; already included. |
| SRBCT | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor-subtype biomedical reference; already included. |
| Indian Pines | DESCRIPTIVE ONLY | Land-cover labels are meaningful external classes, but spatially adjacent pixels violate simple exchangeability and no stability runs exist. |
| Isolet | DESCRIPTIVE ONLY | Spoken-letter recognition labels are meaningful semantic classes; no matched stability runs; 26-class objective differs. |
| Madelon | DESCRIPTIVE ONLY | Synthetic challenge labels are constructed task labels, not biological categories; no paired stability. |
| Newsgroups20 | DESCRIPTIVE ONLY | Human topic categories are meaningful semantic labels but may contain topic overlap and no paired stability. |
| Sonar | DESCRIPTIVE ONLY | Mine/rock domain labels are meaningful, but non-biomedical and no paired stability. |
| Yale B | DESCRIPTIVE ONLY | Subject IDs are identity categories, while illumination is nuisance structure; no paired stability and licensing is restricted/unclear. |
| Zheng68K | INELIGIBLE | Registry, README, loader and runs disagree on variant/dimensions; full loader labels are all zero; reduced-mode label source needs provenance and exact array recovery. |

“Primary eligible” for the existing six means the label concept is suitable, not that the local summary is fully reproducible or confirms all processing steps.
