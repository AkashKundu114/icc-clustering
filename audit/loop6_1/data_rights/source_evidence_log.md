# Dataset rights source evidence log

Checked for Loop 6.1 on 2026-11-02. This log records observed source claims, not legal advice and not an authorization to redistribute.

| Source | Evidence observed | Limit |
|---|---|---|
| UCI ISOLET, https://archive.ics.uci.edu/dataset/54/isolet | Canonical UCI page reports CC BY 4.0, 7,797 instances, 617 features; Cole and Fanty citation; DOI 10.24432/C51G69. | Project registry uses OpenML 300. Same dataset family does not prove exact file/version identity. |
| UCI Twenty Newsgroups, https://archive.ics.uci.edu/dataset/113/twenty+newsgroups | UCI record reports CC BY 4.0, 20,000 messages; Tom Mitchell citation; DOI 10.24432/C5C323. | Project uses scikit-learn fetched/filtered documents; exact variant and underlying post attribution/content restrictions need review. |
| UCI Sonar, https://archive.ics.uci.edu/dataset/151/connectionist+bench+(sonar,+mines+vs.+rocks) | Canonical UCI page reports CC BY 4.0; 208 instances, 60 features; Sejnowski and Gorman citation; DOI 10.24432/C5T01Q. | Project uses OpenML 40; byte-level variant mapping not established. |
| UCI Madelon, https://archive.ics.uci.edu/dataset/171/madelon | Canonical UCI page reports CC BY 4.0; Guyon challenge citation; DOI 10.24432/C5602H. | Project uses OpenML 1485 and the registry says it selects 500 rows. Exact file/split/selection identity is not established. |
| Purdue PURR Indian Pines, https://purr.purdue.edu/publications/1947/1 | PURR record describes 220-band AVIRIS Indian Pine Test Site 3 and declares CC0 1.0; DOI 10.4231/R7RX991C. | Registry points to EHU corrected 200-band MAT and ground truth, which is a different variant. PURR rights do not automatically cover it. |
| Yale Face Database B, https://cvc.cs.yale.edu/cvc/projects/yalefacesB/yalefacesB.html | Yale page allows research use with acknowledgment and says images may not be incorporated into a larger publicly distributed database without Yale permission. | Applies conservatively to image-derived caches/partitions until Yale grants permission; sample-level derived data need explicit review. |
| OpenML REST dataset records, https://www.openml.org/api/v1/json/data/45086 (and IDs 45087, 1104, 45098, 45099, 45101, 300, 1485, 40) | Retrieved metadata contains version and `licence: Public` for these dataset records. | “Public” is not a named standard license and does not by itself establish redistribution rights. OpenML docs say dataset resources carry license metadata; uploader must have rights. |
| 10x Genomics historical PBMC source, https://github.com/10XGenomics/single-cell-3prime-paper | Source repository contains historical 68k PBMC data/source references. No applicable license for the exact historical data file was verified in this review. | Current availability or later 10x dataset licenses cannot be projected backward to this source or Scanpy's reduced example. |
| OpenML terms, https://www.openml.org/terms | General platform terms and dataset-level metadata are available. | Platform terms are not a substitute for rights-holder permissions or exact data-level license. |

## Repository-derived warnings

The FYP registry calls several OpenML cohorts “Public Domain / Open Access.” The inspected OpenML API metadata instead returned the generic string `Public`, which does not establish public-domain status. The registry's broad `license_policy` (“Public academic benchmark datasets under CC-BY / OpenML / Public Domain”) should not be treated as proof of rights.

The local PBMC registry entry names `scanpy.datasets.pbmc68k_reduced()` and gives 700 samples by 765 features. This is not the full 68,579-cell Zheng PBMC matrix. “PBMC68k” and “Zheng68K” therefore should not be treated as identical experimental matrices; the reduced object derives from the same broad source family, but exact lineage, content, and rights need version-specific verification.
