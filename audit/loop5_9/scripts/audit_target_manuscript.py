"""Inventory target-local canonical manuscript claims and inputs.

Reads ignored local paper/manuscript/main.tex, numbers.tex, gen tables and
figures. Writes only audit/loop5_9/manuscript. It does not edit manuscript.
"""
from pathlib import Path
import csv, hashlib, re

ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'paper'
OUT=ROOT/'audit'/'loop5_9'/'manuscript'
MAIN=PAPER/'manuscript'/'main.tex'

def write(name,rows,fields=None):
    p=OUT/name
    if fields is None: fields=list(rows[0]) if rows else []
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    if not MAIN.exists(): raise SystemExit(f'Missing canonical local manuscript: {MAIN}')
    text=MAIN.read_text(encoding='utf-8')
    sha=hashlib.sha256(MAIN.read_bytes()).hexdigest()
    claims=[
      ('Abstract, line 58','Six cohorts; non-degenerate nine-cell stability/ARI; CI +.485 [.379,.662]; all-18 cell values.','Loop5.9 statistics/cell_reconstruction.csv; selection_reconstruction.csv; bootstrap_reanalysis.csv','CONTRADICTED / EXPLORATORY','Nine is post-hoc; CI estimand mismatch; “all 18” ambiguous; stability/ARI are distinct summaries.','Rewrite abstract to report full 72-cell descriptive result; omit subset and CI.'),
      ('Abstract, line 60','GAC/BGSS ablation gains, p=.031, 13-dataset p=.40, memory reduction, marginal multimodality conclusion.','Loop5.9 benchmark/method_implementation_audit.md; remaining claims not independently reconstructed','NOT AUDITED / QUALIFY','Ablation, multiplicity, scaling and data mechanism claims lack raw independent verification here; saved benchmark p is descriptive and rows include copies/imports.','Remove abstract claims pending raw evidence audit; keep separate verified saved-score result narrowly.'),
      ('Introduction, line 68','High dimensionality/noise causes repeated arbitrary partitions and no correctness; prior work gap.','Six-cohort artifacts; literature not comprehensively searched','UNSUPPORTED MECHANISM / NOT AUDITED NOVELTY','Empirical cohorts are observational; simulation evidence not rerun. Novelty claim needs systematic literature review.','Avoid causal wording; substantiate novelty with full related-work review.'),
      ('Contributions, lines 77-94','GAC as method, systematic stability finding, controlled decomposition, 13 benchmark, guidance/reproducibility.','Statistics and benchmark audits; public state','MIXED; SEE SUBCLAIMS','Several results are unaudited, and code/data availability is overstated.','Keep central contribution bounded; remove unsupported GAC/reproducibility assertions.'),
      ('Methods, line 153 and stability section','Stability = mean 435 pairwise overlap ARIs; Accuracy = mean ARI over 30 subsamples.','Loop5.9 statistics/reconstruct_stats.py and cell_reconstruction.csv','VERIFIED WITH LIMITATIONS','Pair values dependent; overlapping data and same partitions; labels stratify subset selection; fixed model seed.','Use “subsampling sensitivity” and state label-informed sampling and fixed seed.'),
      ('Methods, lines 159-160','Rule i / i-prime / ii / iii; rules pre-specified except i-prime.','Git history and statistics/selection_reconstruction.csv','PARTIALLY CONTRADICTED','Rule i-prime explicitly added post hoc; timing of execution relative protocol is unauthenticated; subset used exploratorily.','Label all post-hoc criteria and nine-cell selection as exploratory.'),
      ('Results, six-cohort summary/table 2','Mean stability, ARI, gap/null and nondegenerate results.','Loop5.9 statistics/cell_reconstruction.csv','VERIFIED DESCRIPTIVELY','Cell-level means not independent; no population-level inferential support.','Report as cell/cohort descriptive summaries and show cohort heterogeneity.'),
      ('Results, nine-cell and “all 18” discussion','Nine selected cells and all-18 mean values.','Loop5.9 statistics/selection_reconstruction.csv','EXPLORATORY; WORDING AMBIGUOUS','Two distinct 18-cell populations; post-hoc selection.','Define populations explicitly; do not call an independent confirmation.'),
      ('Results, bootstrap CI','Cohort bootstrap interval for gap.','Loop5.9 statistics/bootstrap_reanalysis.csv','CONTRADICTED AS CURRENTLY PAIRED','Point .485376 cell-weighted; manuscript interval from equal-cohort distribution. Six clusters and aggregate-level bootstrap.','Remove primary CI; optional supplement only with correct estimand and limits.'),
      ('13-dataset benchmark, lines 90 and related tables','3,000 model fits; Friedman p=.40; twelve methods.','Loop5.9 statistics/benchmark_reanalysis.json; benchmark/benchmark_claim_verdict.md','CONDITIONAL / FIT COUNT UNVERIFIED','3,000 saved rows, but Ward rows copied and ICCv2 rows imported; no 3,000 authenticated fits; seed families differ.','Call 3,000 saved score rows; do not imply independent fit count or paired seeds.'),
      ('GAC/BGSS comparative claims, sections 5-6 and conclusion','BGSS improves; ICC/GAC components recover signal.','benchmark/fairness_matrix.csv; raw ablation evidence not independently rerun','NOT AUDITED / HIGH RISK','Method budgets differ; baseline/surrogate implementation questions; tests/multiplicity not recalculated.','Remove headline performance claim pending direct matched reanalysis.'),
      ('Theoretical propositions, methods sections 3-4','Complexity and determinacy guarantees.','No proof/code correspondence audit in Loop5.9','NOT AUDITED','No independent formal review or boundary-case verification.','Do not imply broad guarantees until formal audit.'),
      ('Prostate interpretation, results/discussion/conclusion','PC1/outlier/total-expression mechanism explains partition.','No audited sample-level covariate/PCA linkage in saved fit evidence','NOT AUDITED','Stable sample IDs and producer inputs not linked; mechanism not reconstructed.','Remove or explicitly state origin is unknown.'),
      ('Clinical/biological relevance and implications','Structure relates to tumour classes or discovery/clinical utility.','ARI to external labels only; no clinical validation','UNSUPPORTED AS CLINICAL CLAIM','Reference-label alignment is not clinical utility; no prospective decision study.','Avoid diagnostic/clinical implication.'),
      ('Availability, line 767','All 13 datasets publicly accessible from upstream repositories.','Loop5.9/reproducibility/data_rights_matrix.csv','PARTIALLY SUPPORTED ACCESS; RIGHTS NOT CLEARED','Upstream accessibility does not imply license/redistribution right or exact dataset version.','List exact sources/accessions and terms; release no uncleared files.'),
      ('Code availability, line 777','Complete pipelines/raw logs on GitHub and permanently archived on Zenodo.','Fresh clone log; Zenodo check; GitHub release check','CONTRADICTED','Fresh clone lacks raw evidence; Zenodo record restricted with no files; releases have no assets.','Replace with truthful Tier1-only availability statement.'),
      ('Limitations, line 738 onward','Labels partial standard; alternatives and technical causes noted.','Manuscript text plus missing provenance/rights','PARTIALLY SUPPORTED','Caveat is appropriate, but technical/biological origin cannot be asserted without IDs and covariates.','State source of clusters is unknown.'),
      ('Conclusion, lines 751-755','Discordance; nondegenerate mean CI; Prostate mechanism; GAC ablation; benchmark; scaling.','Multiple Loop5.9 registers','MIXED / OVERCLAIMED','Contains contradicted CI and unaudited/unsupported mechanisms/performance claims.','Narrow to 6-cohort descriptive observation and explicitly separate saved-score benchmark.'),
    ]
    line_map={
      'Abstract, line 58':58,'Abstract, line 60':60,'Introduction, line 68':68,
      'Contributions, lines 77-94':86,'Methods, line 153 and stability section':151,
      'Methods, lines 159-160':153,'Results, six-cohort summary/table 2':210,
      'Results, nine-cell and “all 18” discussion':221,'Results, bootstrap CI':158,
      '13-dataset benchmark, lines 90 and related tables':499,
      'GAC/BGSS comparative claims, sections 5-6 and conclusion':60,
      'Theoretical propositions, methods sections 3-4':231,
      'Prostate interpretation, results/discussion/conclusion':751,
      'Clinical/biological relevance and implications':738,
      'Availability, line 767':767,'Code availability, line 777':777,
      'Limitations, line 738 onward':738,'Conclusion, lines 751-755':751,
    }
    phys=text.splitlines()
    rows=[]
    for loc,claim,evidence,status,reason,action in claims:
        lineno=line_map[loc]
        exact=phys[lineno-1] if len(phys)>=lineno else ''
        rows.append({'manuscript_path':'paper/manuscript/main.tex (local ignored, canonical per paper/README.md)','manuscript_sha256':sha,'location':loc,'source_line':lineno,'exact_source_line':exact,'claim_summary':claim,'evidence':evidence,'status':status,'reason':reason,'recommended_action':action,'abstract_candidate':'No' if any(x in loc for x in ['GAC','Theoretical','Prostate','Clinical','Availability','Conclusion','bootstrap','nine-cell']) else 'Conditional'})
    write('manuscript_claim_matrix.csv',rows)
    tables=[]; figs=[]
    for match in re.finditer(r'\\input\{([^}]+)\}',text):
        raw=match.group(1); path=PAPER/'manuscript'/(raw if raw.endswith('.tex') else raw+'.tex')
        if raw=='numbers.tex': continue
        tables.append({'kind':'table/input','reference':raw,'resolved_path':str(path),'exists':path.exists(),'bytes':path.stat().st_size if path.exists() else '', 'sha256':hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else '', 'scientific_value_audit':'Not independently reconciled to raw experiments in Loop 5.9; see claim register','source_line':text.count('\n',0,match.start())+1})
    for match in re.finditer(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',text):
        raw=match.group(1); path=PAPER/'manuscript'/raw
        candidates=[path,path.with_suffix('.png'),path.with_suffix('.pdf'),path.with_suffix('.jpg')]
        found=next((p for p in candidates if p.exists()),None)
        figs.append({'kind':'figure','reference':raw,'resolved_path':str(found) if found else str(path),'exists':found is not None,'bytes':found.stat().st_size if found else '', 'sha256':hashlib.sha256(found.read_bytes()).hexdigest() if found else '', 'visual_and_numeric_provenance':'Not independently re-generated/validated in Loop 5.9','source_line':text.count('\n',0,match.start())+1})
    write('table_figure_audit.csv',tables+figs,['kind','reference','resolved_path','exists','bytes','sha256','scientific_value_audit','visual_and_numeric_provenance','source_line'])
    return len(rows),len(tables),len(figs)

if __name__=='__main__': print('claim rows, tables, figures:',*main())
