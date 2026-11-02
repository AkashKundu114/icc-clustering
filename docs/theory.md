# Implementation notes and theoretical scope

This page does not state or claim general theorems for ICC, GAC, CICC, or the empirical clustering results. The implementation contains heuristic feature filters, consensus constructions, and optional inductive/conformal components. Their behavior depends on their assumptions, input representation, parameters, implementation details, and data distribution.

In particular, no universal guarantee of cluster recovery, biomedical validity, clinical utility, feature-selection correctness, or superiority over other methods is established by this repository. Any formal property of a specific component must be evaluated against its source implementation and the assumptions stated in the relevant method reference.

For the software's current modules, see [architecture](software-architecture.md) and the [API reference](api.md). For the limits of the available research evidence, see [limitations](limitations.md).
## Selected prior literature

These publications provide background for clustering stability, consensus clustering, modality testing, graph construction, single-cell consensus methods, and ensemble clustering. They do not establish theoretical guarantees for ICC or validate the repository's empirical claims.

- **[monti2003]** Monti, S., Tamayo, P., Mesirov, J. P., & Golub, T. R. (2003). Consensus clustering: A resampling-based method for class discovery and visualization of gene expression microarray data. *Machine Learning*, 52, 91–118. [doi:10.1023/A:1023949509487](https://doi.org/10.1023/A:1023949509487).
- **[wilkerson2010]** Wilkerson, M. D., & Hayes, D. N. (2010). ConsensusClusterPlus: A class discovery tool with confidence assessments and item tracking. *Bioinformatics*, 26(12), 1572–1573. [doi:10.1093/bioinformatics/btq170](https://doi.org/10.1093/bioinformatics/btq170).
- **[hartigan1985]** Hartigan, J. A., & Hartigan, P. M. (1985). The dip test of unimodality. *The Annals of Statistics*, 13(1), 70–84. [doi:10.1214/aos/1176346577](https://doi.org/10.1214/aos/1176346577).
- **[liu2010]** Liu, W., He, J., & Chang, S.-F. (2010). Large graph construction for scalable semi-supervised learning. In *Proceedings of the 27th International Conference on Machine Learning*, 679–686.
- **[kiselev2017]** Kiselev, V. Y., Kirschner, K., Schaub, M. T., et al. (2017). SC3: Consensus clustering of single-cell RNA-seq data. *Nature Methods*, 14, 483–486. [doi:10.1038/nmeth.4236](https://doi.org/10.1038/nmeth.4236).
- **[huang2023]** Huang, D., Wang, C.-D., & Lai, J.-H. (2023). Fast multi-view clustering via ensembles: Towards scalability, superiority, and simplicity. *IEEE Transactions on Knowledge and Data Engineering*. [doi:10.1109/TKDE.2023.3236698](https://doi.org/10.1109/TKDE.2023.3236698). The repository's FastMVC-labelled wrapper is a surrogate and must not be described as a faithful implementation of this method without a separate fidelity audit.

