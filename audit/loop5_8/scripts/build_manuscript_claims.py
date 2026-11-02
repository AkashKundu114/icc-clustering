"""Build a claim-level review of the local FYP candidate manuscript.

Input: D:/Final Year Project/paper/main.tex (read only; SHA documented in baseline_state.md).
Outputs: manuscript_claim_evidence_matrix.csv and remaining_claims_audit_plan.csv.
This script does not modify the manuscript and must not be applied to another version without updating the claim map.
"""
from pathlib import Path
import csv
import re

OUT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"D:\Final Year Project\paper\main.tex")

claims = [
 ("Abstract line 58", "Six cohorts; nine selected cells mean stability .684 and ARI -.003; all 18 cells .638/.046; cohort bootstrap gap .485 CI [.379,.662].", "Loop5.7 recomputed_cell_results.csv; nine_cell_final_verification.csv; bootstrap_reassessment.json", "Contradicted (interval pairing); conditional (other values)", "The nine are post-hoc. ‘All 18’ means recurrent methods × six cohorts, not Rule(i′)'s 18. The CI resamples equal cohort means, unlike the .485 cell-weighted point.", "Rewrite; omit CI and nine from abstract; disambiguate 18.", "Across 72 cells, mean stability was .517, mean external ARI .052, and mean cell-level gap .464 (median .448); these are descriptive for the six cohorts.", "No subset/CI"),
 ("Abstract line 58; methods 153", "Stability is mean of 435 pairwise overlap ARIs; accuracy is mean ARI across 30 subsamples.", "Loop5.7 independent_repeat_checks.csv; recomputed_cell_results.csv", "Verified with qualification", "Definitions match recovered calculations, but 435 pair values are dependent and reuse overlapping partitions.", "Clarify pair dependence and use external-label alignment rather than generic correctness.", "Stability summarizes 435 pairwise ARIs across overlapping subsample partitions; external ARI summarizes 30 comparisons with cohort reference labels.", "Yes"),
 ("Abstract 58; contributions 86; methods 203", "30 independent/stratified 80% subsamples characterize robustness.", "Recovered partitions, per-fit Parquet, PLAN_STAB.md", "Conditionally supported", "30 splits exist, but they are label-stratified, overlapping, shared across methods, and model seed is fixed.", "Describe label-informed sampling and fixed initialization seed; don't call seed robustness.", "We assessed subsampling sensitivity using 30 shared label-stratified 80% subsets and a fixed solver seed.", "Yes"),
 ("Abstract 58; methods 153; conclusion 800", "Reproducibility does not imply correctness.", "Loop5.7 six-cohort reconstruction", "Conditionally supported", "Observed discordance is bounded to reference-label alignment under this protocol; ‘correctness’ overstates ARI's meaning.", "Bound to these cohorts and labels.", "In these cohorts and under the examined protocol, reproducibility did not ensure alignment with available reference labels.", "Narrowed"),
 ("Contributions 86; results 221–225", "Three methods satisfy nondegenerate criterion; null comparison confirms data-driven structure.", "Loop5.7 cell and null results; Loop5.8 subset review", "Conditional; mechanism unsupported", "Selection was post-hoc. Null contrast is descriptive and doesn't identify meaningful structure.", "Report full population and explicitly exploratory subset; remove ‘confirms’.", "The post-hoc subset had higher observed stability than the specified column-permuted null; this is descriptive.", "No"),
 ("Abstract 58; intro 110; results 164/201; conclusion 762/800", "High dimensionality causes stability/accuracy collapse or observed discordance.", "Six-cohort evidence; synthetic experiment not re-run in Loop5.8", "Unsupported as empirical causal inference", "No controlled D intervention in cohorts; simulation can support only its exact synthetic data-generating setting.", "Remove causal bridge and separately verify simulation.", "The analyzed cohorts had D/N>20; the observational results do not establish dimensionality as the cause.", "No causal wording"),
 ("Abstract 60; contributions 90; methods 368/556", "13 datasets, 3,000 fits, 12 methods, Friedman p=.40.", "Loop5.7 benchmark_recalculation.json and raw local FYP rows", "Conditionally supported", "3,000 saved ARI rows and statistic recalculate; model executions are unauthenticated and seed schedules differ.", "Call them saved score observations; correct PassF versus CoHiRF schedules.", "A separate benchmark contains 3,000 saved ARI observations across 13 datasets and 12 methods; the Friedman statistic was recalculated from dataset–method means.", "Maybe"),
 ("Contributions 92; data/code declarations 816–828", "All data, seeds, code and raw logs publicly available; permanent Zenodo archive.", "Loop5.7 clean clone; Zenodo snapshot", "Contradicted", "Clone lacks caches, partitions, fit records and raw benchmark rows; DOI is restricted with zero files.", "Remove until actual archive passes access, hash and clean reproduction checks.", "Code and aggregate-only verification are public; complete inputs and experimental records are not currently available from a fresh clone.", "No"),
 ("Abstract 60; contribution 88; Section 6/7", "BGSS improves ARI by .169; Wilcoxon p=.031; confirmatory gains and domain trade-offs.", "FYP results unreviewed here; EXPERIMENTAL_RED_TEAM_REPORT.md identifies conflicting issues", "Not audited / conflicting", "Needs raw paired outcomes, multiplicity plan, baseline fidelity and cohort validity. Prior red-team review flags label-informed sampling, proxy baseline and contamination.", "Do not retain headline language until independent raw reanalysis.", "Omit pending separate evidence audit.", "No"),
 ("Abstract 94; lines 462–494", "99.6% memory compression; empirical runtime scaling exponent and million-sample performance.", "No independent trace audit in Loop5.8", "Not audited", "Requires hardware/config/raw timing and memory traces and repeatability check.", "Audit separately before claim retention.", "Omit pending audit.", "No"),
 ("Lines 150–164, 221–225, 762–804", "High-dimensional data cause consensus failure; permutation proves observed structure is meaningful.", "Loop5.7 evidence; null summary", "Unsupported mechanism", "Association/null contrast is not causal identification or biological validation.", "Replace mechanism with limited empirical wording.", "The null comparison distinguishes the observed statistic from this permutation control; the source of the partition structure remains undetermined.", "No"),
 ("Lines 159–160; 225; 429; 772", "Rule(i′) and dataset bootstrap were planned and provide confirmatory inference.", "Protocol history; Loop5.7 bootstrap reassessment", "Contradicted / conditional", "Rule(i′) is post-hoc; bootstrap point and interval estimands differ; six cohorts limit population inference.", "Label post-hoc, remove primary CI or re-estimate matching equal-cohort estimand as exploratory.", "The non-degeneracy subset is post-hoc; no cohort-population inference is claimed.", "No"),
 ("Methods 368/556", "All benchmark methods use same seed schedule.", "Raw PassF and CoHiRF CSVs; historical code commits", "Contradicted", "PassF seeds 0–29/0–9; CoHiRF 42–71/42–51; current source's general runner doesn't match the exact PassF file.", "State observed component-specific schedules and source uncertainty.", "Seed schedules differed across benchmark components and should not be treated as paired.", "No"),
 ("Methods 370", "Analysis criteria were pre-specified before execution.", "Protocol commit history and absence of authenticated execution identity", "Conditionally supported", "Commit chronology shows initial rule and later amendment, but doesn't establish runs occurred after protocol freeze.", "Distinguish protocol history from execution chronology.", "Protocol history records the initial criteria and later post-hoc change; execution timing relative to protocol could not be authenticated.", "No"),
 ("Sections 291–363", "GAC propositions/theoretical guarantees and complexity.", "No full proof/code correspondence audit", "Not audited", "Outside stability reconstruction; need independent formal review and boundary testing.", "Retain only after proof audit.", "Omit theorem strength pending review.", "No"),
 ("Lines 223, 751, 762, 787, 800", "Prostate partitions reflect PC1, outliers or total expression rather than tumor status.", "No independent PCA/sample-level mechanism reanalysis", "Unsupported in current evidence set", "Recovered fit files lack stable sample IDs and this audit did not reproduce diagnostics.", "Remove mechanism or provide audited covariate/loadings analysis.", "The available results do not identify what features or covariates drive the Prostate partitions.", "No"),
 ("Lines 634–671; tables 17–19", "Four-cohort preregistered independent confirmatory study; 1,440 runs; multiplicity conclusions.", "FYP claims and audit summaries; not independently run here", "Not audited", "Requires preregistration timestamp, quarantine/unseal chain, raw inputs/outputs and independent reproduction.", "Do not call confirmatory until full protocol and run chain authenticated.", "Omit pending evidence audit.", "No"),
 ("Lines 671–672; 544–566; 608–622", "GAC/Sparse K-Means superiority and biological lineage explanation.", "FYP red-team report; baseline raw-run audit absent", "Unsupported / contested", "Prior audit flags sparse-K parameter mismatch, baseline fallback and cohort concerns; no independent resolution.", "Remove superiority and mechanism language pending fair rerun.", "Omit pending audit.", "No"),
 ("Lines 723–749", "Factorial ablations, Wilcoxon, TOST equivalence and biomarker recovery.", "Not independently recomputed", "Not audited", "Requires per-seed paired records, prespecified family/multiplicity, gene universe and independent analysis.", "Recompute all contrasts and corrections.", "Omit pending audit.", "No"),
 ("Lines 816–828", "All datasets available at listed public sources; data can be reproduced / Zenodo release complete.", "Loop5.5 rights report; Loop5.7 clean clone; Loop5.8 package review", "Unsupported / contradicted as current release claim", "Source links don't establish redistribution rights; clone lacks evidence; DOI empty/restricted.", "Replace with source-specific access and frank unavailable artifacts statement.", "See proposed data_availability_revised.md.", "No"),
 ("Lines 780–789", "Limitations appropriately note exploratory cohorts, finite power, clinical disclaimer, label semantics.", "Manuscript text and evidence gaps", "Conditionally supported", "Caveats are appropriate but contradicted by stronger claims elsewhere; caveats alone don't correct them.", "Retain and align headline/conclusion claims with limitations.", "Use the narrow scope and limitations consistently throughout.", "No"),
]

remaining = [
 ("P0","Exact manuscript version and submission package","whole manuscript","Committed exact manuscript, tables, figures, bibliography, supplements","Hash and compare all package files to evidence sources","Target repo contains no manuscript; separate FYP candidate is not confirmed submission version","Abstract and all claims"),
 ("P0","Confirmatory biobank and preregistration","58,60,92,634-671,780-783,823","Timestamped protocol, cohort inputs/labels, run outputs, quarantine logs, unsealing history, code commit","Independently rerun 1,440 fits; verify identity, splits, multiplicity and chronology","No independent verification in Loop5.8","Abstract/conclusion"),
 ("P0","GAC/BGSS superiority and baseline comparisons","60,88,90,231,544-566,608-671,723-749","Raw matched per-seed scores, faithful baseline code, same K/budget/preprocessing and leakage checks","Recompute effects/tests with multiplicity and audit implementations","Prior red-team flags FastMVC proxy, Sparse K mismatch, fallback, uneven comparisons","Abstract/contributions"),
 ("P0","Benchmark fit provenance and seeds","90,368,556; tables 6-10","Raw rows, generator/config/source commits, execution logs/environment","Verify 3000/156, reconcile schedules, regenerate Friedman and post-hoc tests","Saved values verified, run event not authenticated; schedules inconsistent","Abstract/results"),
 ("P1","Synthetic causal statements","58,110,164,181,201,762,800","Generator/configs, seeds and raw outputs","Reproduce controlled noise intervention and limit inference to synthetic domain","Not rerun; empirical cohorts observational","Abstract/conclusion"),
 ("P1","Scaling, runtime and memory","94,462-494,804","Hardware, commands, raw timing/memory traces and repetitions","Rerun with controls and report variability","No execution evidence reviewed here","Abstract/conclusion"),
 ("P1","Prostate PCA/outlier mechanism","223,751,762,787,800","Sample mapping, exact features, loadings/scores, covariates and batch controls","Recompute diagnostic analyses and uncertainty","No sample IDs / causal mechanism not established","Conclusion"),
 ("P1","Leukemia biomarker/pathway claims","749-750","Gene rankings, reference list/version, background universe and multiple-testing plan","Recompute overlap/enrichment independently","Not checked; circular interpretation risk","Abstract/conclusion"),
 ("P1","Theoretical propositions and complexity","291-363,803","Formal assumptions/proofs and code correspondence","Independent proof review and boundary tests","Outside empirical audit","Abstract/conclusion"),
 ("P1","Clinical implications","58,86,783-804","Clinical validation and prospective governance","Remove diagnostic claims or conduct clinical study","No clinical validation evidence","Abstract/conclusion"),
 ("P2","Novelty/related work","68-114,247-280","Current systematic literature search and closest-method comparisons","Update citations and differentiate empirical/methodological novelty","Not exhaustive","Abstract/introduction"),
 ("P2","Dataset identity/licensing","518-533,816-823","Upstream versions, labels, licenses, attribution and exact transformations","Verify each source and document legal access","Public download is not redistribution authorization","Data availability"),
 ("P2","Figures and supplementary tables","all figures; tables 1-19 and supplement","Source data/scripts and generated versions","Regenerate in supported clean environment and compare outputs","No complete figure/table audit","All displayed claims"),
]

# The hand-coded adjudications above target high-priority claims. To prevent
# those rows from being mistaken for exhaustive coverage, also enumerate every
# section/subsection lead paragraph and every in-manuscript figure/table
# caption, quoting exact source text. These broad rows remain Not audited unless
# explicitly covered by a high-priority adjudication above.
def extract_balanced_brace(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{": depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0: return text[start + 1:i]
    return text[start + 1:]

def short_exact(text, limit=1000):
    # Keep exact source excerpt (including TeX) but avoid a multi-page claim row.
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + (" […]" if len(text) > limit else "")

source_text = SOURCE.read_text(encoding="utf-8")
section_markers = list(re.finditer(r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}(?:\\label\{[^}]*\})?", source_text))
coverage = []
for idx, marker in enumerate(section_markers):
    end = section_markers[idx + 1].start() if idx + 1 < len(section_markers) else len(source_text)
    chunk = source_text[marker.end():end].strip()
    # The first substantive paragraph/claim precedes the first float or list.
    chunk = re.sub(r"^\\label\{[^}]*\}\s*", "", chunk)
    para_end = min([p for p in [chunk.find("\n\n"), chunk.find("\\begin{figure"), chunk.find("\\begin{table"), chunk.find("\\begin{itemize"), chunk.find("\\input{")] if p >= 0] or [len(chunk)])
    excerpt = short_exact(chunk[:para_end])
    if excerpt:
        coverage.append((f"{marker.group(1).title()}: {marker.group(2)}; source offset {marker.start()}", excerpt,
                         "Loop5.7 evidence where applicable; FYP source/results not comprehensively audited", "Not audited (section coverage row)",
                         "This row captures the exact lead paragraph for coverage; individual claims and supporting artifacts still require item-level adjudication.",
                         "Refer to the priority claim adjudications and remaining_claims_audit_plan.csv; do not infer support from inclusion in manuscript.",
                         "Not proposed.", "No"))

# Exact table and figure captions are claims as presented to readers. Inline
# captions only; separately-input generated tables are inventoried below.
for env in ("figure", "figure*", "table", "table*"):
    for m in re.finditer(r"\\begin\{" + re.escape(env) + r"\}.*?\\caption\*?\{", source_text, re.S):
        cap = extract_balanced_brace(source_text, m.end() - 1)
        label_match = re.search(r"\\label\{([^}]*)\}", source_text[m.end():m.end()+1800])
        loc = ("Figure" if env.startswith("figure") else "Table") + (f" {label_match.group(1)}" if label_match else "") + f"; source offset {m.start()}"
        coverage.append((loc, short_exact(cap), "Corresponding result artifacts not all audited in Loop5.8", "Not audited (caption claim)",
                         "Caption-level result or interpretation has not been independently verified unless separately adjudicated above.",
                         "Trace caption to raw inputs, generation script and results before retaining.", "Not proposed.", "No"))

# Generated table inputs are exact manuscript dependencies even when their
# contents are separate files. Their scientific results were not broadly
# re-audited; the six-cohort and benchmark tables have specific adjudications.
for table_file in re.findall(r"\\input\{(gen/table[^}]+\.tex)\}", source_text):
    p = SOURCE.parent / table_file
    excerpt = short_exact(p.read_text(encoding="utf-8")) if p.exists() else "[input file missing]"
    status = "Conditionally supported (core table)" if any(k in table_file for k in ("table02_real_data_stability", "table16_degeneracy_audit", "table06_omnibus_benchmark_ari")) else "Not audited (generated table)"
    coverage.append((f"Generated table input {table_file}", excerpt, str(p) if p.exists() else "Missing input", status,
                     "Generated table content is not fully verified by the core stability reconstruction.",
                     "Recompute from versioned raw inputs and record the generating script.", "Not proposed.", "No"))

def write(name, header, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

if not SOURCE.exists():
    raise SystemExit(f"Manuscript input missing: {SOURCE}")
header = ["manuscript_version","location","exact_claim_or_quote","evidence_source","status","reason","required_correction","proposed_replacement","abstract_candidate"]
write("manuscript_claim_evidence_matrix.csv", header, [("FYP paper/main.tex; SHA BB09E87B...", *r) for r in claims] + [("FYP paper/main.tex; SHA BB09E87B...", *r) for r in coverage])
write("remaining_claims_audit_plan.csv", ["priority","claim_family","manuscript_locations","required_evidence","minimum_reanalysis","blocker_reason","abstract_or_conclusion"], remaining)
print(f"Reviewed input bytes={SOURCE.stat().st_size}; priority claim rows={len(claims)}; coverage rows={len(coverage)}; remaining families={len(remaining)}")
