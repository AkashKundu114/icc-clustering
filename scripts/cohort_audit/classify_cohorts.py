"""
Step 7: Formal Cohort Classification & Independence Quantification.
Categorizes every dataset into Category A, B, C, D, or E based on provenance and profile audits.

Outputs:
- results/cohort_independence/cohort_classification.csv
"""

from pathlib import Path
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
OUT_CSV = _ROOT / "results" / "cohort_independence" / "cohort_classification.csv"
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

CLASSIFICATIONS = [
    # -------------------------------------------------------------------------
    # Category A: Confirmed Independent Biological Cohorts
    # -------------------------------------------------------------------------
    {
        "dataset_key": "colon",
        "intended_name": "Colon Cancer Gene Expression",
        "primary_citation": "Alon et al. PNAS 1999",
        "samples_n": 62, "features_d": 2000, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct clinical recruitment (Princeton Hospital); Affymetrix Hum60K array.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent oncology cohort."
    },
    {
        "dataset_key": "srbct",
        "intended_name": "Small Round Blue Cell Tumors",
        "primary_citation": "Khan et al. Nat Med 2001",
        "samples_n": 83, "features_d": 2308, "clusters_k": 4,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct pediatric patient cohort (NCI/NIH); Custom cDNA microarrays.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent oncology cohort."
    },
    {
        "dataset_key": "leukemia",
        "intended_name": "Golub Acute Leukemia (ALL vs AML)",
        "primary_citation": "Golub et al. Science 1999",
        "samples_n": 72, "features_d": 7129, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct clinical recruitment (St. Jude / CALGB); Affymetrix Hu6800 array.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "GCM (reused in GCM), Leukemia-3 (alternative labeling)",
        "recommended_benchmark_treatment": "Retain as primary independent oncology cohort."
    },
    {
        "dataset_key": "cns",
        "intended_name": "CNS Embryonal Tumors",
        "primary_citation": "Pomeroy et al. Nature 2002",
        "samples_n": 60, "features_d": 7129, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct pediatric medulloblastoma cohort (Dana-Farber / Mass General); Affymetrix Hu6800.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "glioma_e1 (100% duplicate copy in e1), GCM (reused in GCM)",
        "recommended_benchmark_treatment": "Retain as primary independent oncology cohort."
    },
    {
        "dataset_key": "prostate",
        "intended_name": "Prostate Cancer Microarray",
        "primary_citation": "Singh et al. Cancer Cell 2002",
        "samples_n": 102, "features_d": 12600, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct radical prostatectomy clinical recruitment (Brigham and Women's); Affymetrix U95Av2.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent oncology cohort."
    },
    {
        "dataset_key": "ovarian",
        "intended_name": "Ovarian Cancer Proteomics (SELDI)",
        "primary_citation": "Petricoin et al. Lancet 2002",
        "samples_n": 253, "features_d": 15154, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct patient serum cohort (NCI-FDA Clinical Proteomics); SELDI-TOF Mass Spectrometry.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent proteomics cohort."
    },
    {
        "dataset_key": "dlbcl",
        "intended_name": "Diffuse Large B-Cell Lymphoma vs FL",
        "primary_citation": "Shipp et al. Nat Med 2002",
        "samples_n": 77, "features_d": 5469, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct lymphoma clinical biopsies (Dana-Farber); Affymetrix Hu6800.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent expanded cohort."
    },
    {
        "dataset_key": "breast",
        "intended_name": "Breast Cancer 5-Year Metastasis",
        "primary_citation": "van 't Veer et al. Nature 2002",
        "samples_n": 97, "features_d": 24481, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct breast carcinoma surgical cohort (Netherlands Cancer Institute NKI); Agilent Hu25k.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as primary independent expanded cohort."
    },
    {
        "dataset_key": "su2001",
        "intended_name": "11 Human Solid Tumors",
        "primary_citation": "Su et al. Cancer Res 2001",
        "samples_n": 174, "features_d": 12533, "clusters_k": 11,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Multi-center solid tumor surgical biopsies; Affymetrix GeneChip U95A.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "Novartis 2002 (shares author laboratory GNF)",
        "recommended_benchmark_treatment": "Retain as primary independent expanded cohort."
    },
    {
        "dataset_key": "endometrium",
        "intended_name": "Endometrium vs Kidney Adenocarcinoma",
        "primary_citation": "Risinger et al. Cancer Res 2003",
        "samples_n": 321, "features_d": 10936, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct surgical resection cohort (Armstrong / Risinger); Affymetrix HG-U95Av2.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "lymphoma_e1 (mislabeled alias in e1)",
        "recommended_benchmark_treatment": "Retain as primary independent expanded cohort."
    },
    {
        "dataset_key": "gli",
        "intended_name": "Gliomas (High-grade vs Low-grade)",
        "primary_citation": "Nutt et al. Cancer Res 2003",
        "samples_n": 85, "features_d": 22283, "clusters_k": 2,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort",
        "evidence_summary": "Distinct brain tumor clinical biopsies (Mass General / Harvard); Affymetrix U95Av2.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "OpenML 45089 GLI. Distinct from OpenML 1107 tumors_C duplicate.",
        "recommended_benchmark_treatment": "Include as verified true glioma cohort."
    },
    {
        "dataset_key": "zheng68k",
        "intended_name": "PBMC 68k Single-Cell RNA-seq",
        "primary_citation": "Zheng et al. Nat Commun 2017",
        "samples_n": 700, "features_d": 765, "clusters_k": 10,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort (Single-Cell Stratum)",
        "evidence_summary": "Primary 10x Genomics microfluidics droplet scRNA-seq from healthy blood donor.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "pbmc68k_reduced (identical subsample)",
        "recommended_benchmark_treatment": "Retain in separate scRNA-seq benchmark stratum."
    },
    {
        "dataset_key": "arrhythmia",
        "intended_name": "Cardiac Arrhythmia 12-Lead ECG",
        "primary_citation": "Guvenir et al. Comp in Cardiology 1997",
        "samples_n": 452, "features_d": 279, "clusters_k": 16,
        "classification_category": "Category A",
        "category_description": "Confirmed Independent Cohort (Clinical Electrophysiology)",
        "evidence_summary": "Clinical cardiology ECG patient recordings; Bilkent University.",
        "confidence_level": "High (Confirmed)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Retain as clinical non-genomic tabular benchmark."
    },

    # -------------------------------------------------------------------------
    # Category B: Independent Study, Potential Lab Overlap or Renamed Alias
    # -------------------------------------------------------------------------
    {
        "dataset_key": "novartis",
        "intended_name": "9 Human Carcinomas (Novartis)",
        "primary_citation": "Su et al. PNAS 2002",
        "samples_n": 60, "features_d": 5726, "clusters_k": 9,
        "classification_category": "Category B",
        "category_description": "Independent Study, Shared Author Lab",
        "evidence_summary": "Shares senior author laboratory (GNF / Novartis) with Su 2001, though measured on distinct 60-tissue panel.",
        "confidence_level": "Medium-High",
        "related_datasets": "Su 2001",
        "recommended_benchmark_treatment": "Include in expanded benchmark with sensitivity check for Su 2001."
    },
    {
        "dataset_key": "lymphoma_e1",
        "intended_name": "Lymphoma in e1 cache (OpenML 1157)",
        "primary_citation": "Risinger et al. / Armstrong (AP Endometrium Kidney)",
        "samples_n": 321, "features_d": 10935, "clusters_k": 2,
        "classification_category": "Category B",
        "category_description": "Independent Clinical Cohort, Mislabeled in Code",
        "evidence_summary": "OpenML ID 1157 is actually AP_Endometrium_Kidney. It is an independent cohort, but was misattributed as lymphoma.",
        "confidence_level": "High (Mislabeled Alias)",
        "related_datasets": "endometrium",
        "recommended_benchmark_treatment": "Rename to Endometrium; deduplicate against endometrium."
    },

    # -------------------------------------------------------------------------
    # Category C: Shared Cohort / Composite Compilation (Overlapping Patients)
    # -------------------------------------------------------------------------
    {
        "dataset_key": "gcm",
        "intended_name": "Global Cancer Map (Ramaswamy 2001)",
        "primary_citation": "Ramaswamy et al. PNAS 2001",
        "samples_n": 190, "features_d": 16063, "clusters_k": 14,
        "classification_category": "Category C",
        "category_description": "Composite Multi-Study Compilation with Confirmed Patient Overlap",
        "evidence_summary": "Ingests 61/72 Golub Leukemia patients (r >= 0.99) and 8/60 Pomeroy CNS patients (r > 0.90).",
        "confidence_level": "High (Confirmed Overlap)",
        "related_datasets": "leukemia, cns, lung_cancer_e1",
        "recommended_benchmark_treatment": "EXCLUDE from cross-cohort validation if Leukemia or CNS is evaluated."
    },
    {
        "dataset_key": "lung_cancer_e1",
        "intended_name": "Lung Cancer in e1 cache (OpenML 1106)",
        "primary_citation": "Ramaswamy et al. PNAS 2001 (Actually GCM)",
        "samples_n": 190, "features_d": 16063, "clusters_k": 14,
        "classification_category": "Category C",
        "category_description": "Composite Compilation (Mislabeled Alias of GCM)",
        "evidence_summary": "OpenML ID 1106 is GCM ($N=190, K=14$). Ingests Golub Leukemia and Pomeroy CNS samples.",
        "confidence_level": "High (Confirmed Overlap)",
        "related_datasets": "gcm, leukemia, cns",
        "recommended_benchmark_treatment": "EXCLUDE from benchmark due to patient contamination and mislabeling."
    },

    # -------------------------------------------------------------------------
    # Category D: Derived Dataset / 100% Bit-for-Bit Duplicate
    # -------------------------------------------------------------------------
    {
        "dataset_key": "glioma_e1",
        "intended_name": "Glioma in e1 cache (OpenML 1107)",
        "primary_citation": "Pomeroy et al. Nature 2002 (tumors_C)",
        "samples_n": 60, "features_d": 7129, "clusters_k": 2,
        "classification_category": "Category D",
        "category_description": "100% Bit-for-Bit Exact Duplicate of CNS",
        "evidence_summary": "Identical SHA-256 (0e449bf...). OpenML ID 1107 is tumors_C (CNS), not Glioma.",
        "confidence_level": "High (100% Duplicate)",
        "related_datasets": "cns",
        "recommended_benchmark_treatment": "EXCLUDE immediately. Do not double-count."
    },
    {
        "dataset_key": "pbmc68k_reduced",
        "intended_name": "PBMC 68k Reduced Subsample",
        "primary_citation": "Zheng et al. Nat Commun 2017",
        "samples_n": 700, "features_d": 765, "clusters_k": 10,
        "classification_category": "Category D",
        "category_description": "Exact Duplicate Representation of zheng68k",
        "evidence_summary": "Refers to the identical 700-cell subsample from Scanpy.",
        "confidence_level": "High (100% Duplicate)",
        "related_datasets": "zheng68k",
        "recommended_benchmark_treatment": "Collapse into single zheng68k entry."
    },
    {
        "dataset_key": "leukemia3",
        "intended_name": "Leukemia-3 (OpenML 45091)",
        "primary_citation": "Golub et al. 1999 / Armstrong et al. 2002",
        "samples_n": 72, "features_d": 7129, "clusters_k": 3,
        "classification_category": "Category D",
        "category_description": "Alternative Label Partition of Golub Leukemia",
        "evidence_summary": "Exact same 72 patient microarrays as Golub Leukemia, partitioned into 3 classes (AML, ALL-B, ALL-T).",
        "confidence_level": "High (Same Cohort)",
        "related_datasets": "leukemia",
        "recommended_benchmark_treatment": "Do not count as independent cohort; use only as subtype sensitivity check."
    },

    # -------------------------------------------------------------------------
    # Category E: Disqualified Non-Biological Mislabeled Datasets & Controls
    # -------------------------------------------------------------------------
    {
        "dataset_key": "breast_cancer_genomic_e1",
        "intended_name": "Breast Cancer Genomic in e1 cache (OpenML 1120)",
        "primary_citation": "Bock et al. (MagicTelescope)",
        "samples_n": 19020, "features_d": 10, "clusters_k": 2,
        "classification_category": "Category E",
        "category_description": "Disqualified Non-Biological Mislabeled File (MagicTelescope)",
        "evidence_summary": "OpenML ID 1120 is an astrophysics Cherenkov gamma-ray telescope simulation ($D=10$), not genomics.",
        "confidence_level": "High (Disqualified)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "PURGE from biological benchmarks."
    },
    {
        "dataset_key": "gisette_e1",
        "intended_name": "Gisette in e1 cache (OpenML 41027)",
        "primary_citation": "Jungle Chess Game Endgame (OpenML 41027)",
        "samples_n": 1000, "features_d": 6, "clusters_k": 3,
        "classification_category": "Category E",
        "category_description": "Disqualified Non-Biological Mislabeled File (Jungle Chess)",
        "evidence_summary": "OpenML ID 41027 is a board game endgame dataset ($D=6$), not the NIPS 2003 Gisette handwriting challenge.",
        "confidence_level": "High (Disqualified)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "PURGE from benchmark."
    },
    {
        "dataset_key": "usps_e1",
        "intended_name": "USPS in e1 cache (OpenML 554)",
        "primary_citation": "LeCun et al. MNIST (OpenML 554)",
        "samples_n": 2000, "features_d": 784, "clusters_k": 10,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (MNIST Digits)",
        "evidence_summary": "Handwritten digits. Mislabeled as USPS, but is actually MNIST 784.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Treat strictly as vision control, not biological."
    },
    {
        "dataset_key": "sonar",
        "intended_name": "Sonar Acoustic Returns",
        "primary_citation": "Gorman & Sejnowski 1988",
        "samples_n": 208, "features_d": 60, "clusters_k": 2,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Acoustic Sonar)",
        "evidence_summary": "Naval acoustic sonar returns from metal cylinders vs rock cylinders.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Non-biological control stratum only."
    },
    {
        "dataset_key": "madelon",
        "intended_name": "Madelon Synthetic XOR",
        "primary_citation": "Guyon et al. NIPS 2003",
        "samples_n": 500, "features_d": 500, "clusters_k": 2,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Synthetic XOR Simulation)",
        "evidence_summary": "Purely synthetic non-linear XOR data generator with 480 Gaussian distractor dimensions.",
        "confidence_level": "High (Synthetic)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Synthetic control stratum only."
    },
    {
        "dataset_key": "isolet",
        "intended_name": "Isolet Spoken Letter Recognition",
        "primary_citation": "Fanty & Cole 1991",
        "samples_n": 7797, "features_d": 617, "clusters_k": 26,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Speech Audio)",
        "evidence_summary": "Spoken letter acoustic signals from 150 human speakers.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Speech control stratum only."
    },
    {
        "dataset_key": "newsgroups20",
        "intended_name": "20 Newsgroups Topic Postings",
        "primary_citation": "Lang 1995",
        "samples_n": 18846, "features_d": 10000, "clusters_k": 20,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Text Corpus)",
        "evidence_summary": "Usenet newsgroup text document postings.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Text control stratum only."
    },
    {
        "dataset_key": "indian_pines",
        "intended_name": "Indian Pines Hyperspectral Radiance",
        "primary_citation": "Purcell et al. 1992",
        "samples_n": 10249, "features_d": 200, "clusters_k": 16,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Remote Sensing Hyperspectral)",
        "evidence_summary": "Airborne AVIRIS hyperspectral sensor image of agricultural field crops.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Hyperspectral control stratum only."
    },
    {
        "dataset_key": "yale_b",
        "intended_name": "Extended Yale Face Database B",
        "primary_citation": "Georghiades et al. 2001",
        "samples_n": 2414, "features_d": 1024, "clusters_k": 38,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Facial Photography)",
        "evidence_summary": "Grayscale photograph pixel luminance arrays.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Vision control stratum only."
    },
    {
        "dataset_key": "waveform",
        "intended_name": "Waveform Database Generator",
        "primary_citation": "Breiman et al. 1984",
        "samples_n": 2000, "features_d": 40, "clusters_k": 3,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Synthetic Waveform)",
        "evidence_summary": "Mathematical combination of triangular wave bases with random noise.",
        "confidence_level": "High (Synthetic)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Synthetic control stratum only."
    },
    {
        "dataset_key": "har",
        "intended_name": "Human Activity Recognition Sensors",
        "primary_citation": "Anguita et al. 2013",
        "samples_n": 2000, "features_d": 561, "clusters_k": 6,
        "classification_category": "Category E",
        "category_description": "Non-Biological Control (Inertial Smartphone Sensors)",
        "evidence_summary": "Tri-axial accelerometer and angular velocity gyroscope sensors.",
        "confidence_level": "High (Non-Biological)",
        "related_datasets": "None",
        "recommended_benchmark_treatment": "Sensor control stratum only."
    },
]


def run_classification():
    print("=== Formal Cohort Independence Classification ===")
    df = pd.DataFrame(CLASSIFICATIONS)
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved cohort classifications to: {OUT_CSV} ({len(df)} entries)")

    # Print summary counts
    print("\n--- Summary Independence Breakdown ---")
    counts = df["classification_category"].value_counts()
    for cat in ["Category A", "Category B", "Category C", "Category D", "Category E"]:
        cnt = counts.get(cat, 0)
        print(f"  {cat:12s}: {cnt:2d} datasets")

    # Filter to biological oncology microarrays only
    bio_df = df[df["dataset_key"].isin([
        "colon", "srbct", "leukemia", "cns", "prostate", "ovarian",
        "dlbcl", "breast", "su2001", "novartis", "gcm", "endometrium",
        "gli", "glioma_e1", "lung_cancer_e1", "lymphoma_e1"
    ])]
    print(f"\nTotal Biological Oncology Datasets Examined: {len(bio_df)}")
    cat_a = len(bio_df[bio_df["classification_category"] == "Category A"])
    cat_b = len(bio_df[bio_df["classification_category"] == "Category B"])
    cat_c = len(bio_df[bio_df["classification_category"] == "Category C"])
    cat_d = len(bio_df[bio_df["classification_category"] == "Category D"])
    print(f"  Category A (Confirmed Independent Cohorts): {cat_a}")
    print(f"  Category B (Likely Independent / Shared Lab): {cat_b}")
    print(f"  Category C (Composite Overlap with Golub/Pomeroy): {cat_c}")
    print(f"  Category D (100% Bit-for-Bit Duplicate of CNS): {cat_d}")
    print(f"--> MAXIMUM TRUE INDEPENDENT HIGH-D ONCOLOGY COHORTS: {cat_a + cat_b} (NOT 21!)")


if __name__ == "__main__":
    run_classification()
