# Comprehensive Metric Definitions and Mathematical Formulations

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent C — Comprehensive Evaluation Design  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. External Clustering Quality Metrics

External validation metrics evaluate agreement between predicted cluster assignments $\hat{\mathbf{y}} = (\hat{y}_1, \dots, \hat{y}_N)$ and ground-truth biological annotations $\mathbf{y}^* = (y^*_1, \dots, y^*_N)$.

### 1.1 Adjusted Rand Index (ARI; Hubert & Arabie, 1985)
- **Mathematical Definition:**
  Let $n_{ij} = |C_i \cap C^*_j|$ denote the contingency overlap between predicted cluster $C_i$ and ground-truth class $C^*_j$.
  $$\text{ARI} = \frac{\sum_{ij} \binom{n_{ij}}{2} - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{N}{2}}{\frac{1}{2} \left[ \sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2} \right] - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{N}{2}}$$
  where $a_i = \sum_j n_{ij}$ and $b_j = \sum_i n_{ij}$.
- **Range:** $[-0.5, 1.0]$. $1.0$ indicates identical clusterings; $0.0$ denotes expected chance agreement under the generalized hypergeometric model.
- **Scientific Role:** Primary external validation metric. Adjusted for chance grouping regardless of cluster count $K$.

### 1.2 Normalized Mutual Information (NMI; Strehl & Ghosh, 2002)
- **Mathematical Definition:**
  $$\text{NMI}(\mathbf{y}^*, \hat{\mathbf{y}}) = \frac{2 \cdot I(\mathbf{y}^*; \hat{\mathbf{y}})}{H(\mathbf{y}^*) + H(\hat{\mathbf{y}})}$$
  where $I(U; V) = \sum_{ij} P(u_i, v_j) \log \frac{P(u_i, v_j)}{P(u_i)P(v_j)}$ and $H(U) = -\sum_i P(u_i) \log P(u_i)$.
- **Range:** $[0.0, 1.0]$. $1.0$ denotes perfect mutual information concordance; $0.0$ indicates statistical independence.
- **Scientific Role:** Measures information-theoretic shared entropy.

### 1.3 Adjusted Mutual Information (AMI; Vinh et al., 2010)
- **Mathematical Definition:**
  $$\text{AMI}(\mathbf{y}^*, \hat{\mathbf{y}}) = \frac{I(\mathbf{y}^*; \hat{\mathbf{y}}) - \mathbb{E}[I(\mathbf{y}^*; \hat{\mathbf{y}})]}{\frac{1}{2}(H(\mathbf{y}^*) + H(\hat{\mathbf{y}})) - \mathbb{E}[I(\mathbf{y}^*; \hat{\mathbf{y}})]}$$
  where $\mathbb{E}[I]$ is calculated analytically using the multivariate hypergeometric distribution for fixed marginals.
- **Range:** $[-0.5, 1.0]$. Expected value is $0.0$ under random chance partitions.
- **Scientific Role:** Recommended over NMI when comparing clusterings with varying numbers of clusters or unbalanced class sizes.

### 1.4 Homogeneity, Completeness, and V-Measure (Rosenberg & Hirschberg, 2007)
- **Homogeneity ($h$):** $h = 1 - \frac{H(\mathbf{y}^* | \hat{\mathbf{y}})}{H(\mathbf{y}^*)}$. Measures whether each cluster contains only members of a single class.
- **Completeness ($c$):** $c = 1 - \frac{H(\hat{\mathbf{y}} | \mathbf{y}^*)}{H(\hat{\mathbf{y}})}$. Measures whether all members of a given class are assigned to the same cluster.
- **V-Measure ($V_\beta$ with $\beta=1$):**
  $$V_1 = \frac{2 \cdot h \cdot c}{h + c}$$
- **Range:** $[0.0, 1.0]$. Harmonic mean balancing cluster purity against class fragmentation.

### 1.5 Silhouette Coefficient (Rousseeuw, 1987)
- **Mathematical Definition:**
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
  where $a(i)$ is mean intra-cluster distance of sample $i$, and $b(i) = \min_{C_k \neq C(i)} \text{mean}_{j \in C_k} d(i, j)$ is mean nearest-cluster distance.
- **Global Score:** $\bar{s} = \frac{1}{N}\sum_{i=1}^N s(i)$.
- **Distance & Sampling Specification:** Euclidean metric computed on standardized feature matrix $\mathbf{X}$; for $N > 2000$, sub-sampled over 2,000 points.

---

## 2. Stability and Consensus-Specific Metrics

### 2.1 Proportion of Ambiguous Clustering (PAC; Senbabaoglu et al., Sci Rep 2014)
- **Mathematical Definition:**
  Let $\mathbf{S} \in [0, 1]^{N \times N}$ be the consensus co-association matrix, and $F(x) = \frac{2}{N(N-1)}\sum_{i < j} \mathbf{1}(S_{ij} \le x)$ denote the empirical cumulative distribution function (CDF) of consensus values.
  $$\text{PAC}(u_1, u_2) = F(u_2) - F(u_1)$$
  with canonical ambiguity boundaries:
  $$u_1 = 0.10, \quad u_2 = 0.90$$
- **Bipartite Linear Approximation:** In bipartite consensus with sample-to-anchor matrix $\mathbf{B} \in \mathbb{R}^{N \times L}$, $S_{ij} = \sum_{l=1}^L B_{il} B_{jl}$. PAC is evaluated over $P = 10{,}000$ randomly sampled sample pairs in $\mathcal{O}(P \cdot L)$ time.
- **Interpretation:** $\text{PAC} \to 0$ indicates a bimodal consensus matrix where sample pairs either always cluster together ($S_{ij} \ge 0.90$) or never cluster together ($S_{ij} \le 0.10$). Optimal $K^* = \arg\min_K \text{PAC}(K)$.

### 2.2 Subsample Stability Agreement ($\text{Stab}_{\text{sub}}$)
- **Mathematical Definition:**
  Draw two independent random subsamples $\mathcal{X}_1, \mathcal{X}_2 \subset \mathcal{X}$ of proportion $\gamma = 0.80$. Fit clusterer $f$ to obtain partitions $\mathcal{P}_1, \mathcal{P}_2$. Restrict both to the intersection $\mathcal{X}_{12} = \mathcal{X}_1 \cap \mathcal{X}_2$.
  $$\text{Stab} = \text{ARI}(\mathcal{P}_1 |_{\mathcal{X}_{12}}, \mathcal{P}_2 |_{\mathcal{X}_{12}})$$
  Evaluated across $B=30$ independent subsampling draws.

### 2.3 Stability–Accuracy Discordance Metrics
- **Fisher $z$-Transformed Spearman Correlation ($z(\hat{\rho}_j)$):**
  $$\hat{\rho}_j = \text{SpearmanCorr}(\{\text{Stab}_{m, j}\}_{m=1}^M, \{\text{ARI}_{m, j}\}_{m=1}^M), \quad z(\hat{\rho}_j) = \frac{1}{2}\ln\left(\frac{1 + \hat{\rho}_j}{1 - \hat{\rho}_j}\right)$$
- **Stability-Minus-Accuracy False Confidence Gap ($\Delta_{\text{gap}}$):**
  $$\Delta_{m, j} = \text{Stab}_{m, j} - \text{ARI}_{m, j}, \quad \bar{\Delta}_j = \frac{1}{M}\sum_{m=1}^M \Delta_{m, j}$$

---

## 3. Computational and Operational Metrics

### 3.1 Wall-Clock Latency ($t_{\text{sec}}$)
- Evaluated using `time.perf_counter()` strictly wrapping model execution (`model.fit_predict(X)`), excluding disk I/O and evaluation metric calculation.

### 3.2 Peak Resident Set Size (RSS Memory; $\text{RAM}_{\text{MB}}$)
- Evaluated via `tracemalloc` or `psutil.Process().memory_info().rss / 1024 / 1024`. Measures peak physical memory allocated during model execution.

### 3.3 Convergence and Attrition Rate ($R_{\text{fail}}$)
- Ratio of runs terminating with `FAILURE_ABORT`, singular matrix exceptions, or degenerate single-cluster outputs:
  $$R_{\text{fail}} = \frac{N_{\text{failed}}}{N_{\text{total}}}$$
