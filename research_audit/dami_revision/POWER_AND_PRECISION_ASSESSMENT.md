# Power and Precision Assessment: Confirmatory Cohort Expansion ($J=15$)

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Document Reference:** `ASSESSMENT-POWER-PRECISION-v2.1`  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Branch:** `research/dami-revision`  
**Date:** November 1, 2026  
**Status:** Post-Audit Reconciled Protocol Deliverable (Incorporating Independent Statistical Review)  

---

## 1. Executive Summary: The Sufficiency Fallacy

Prior project drafts asserted that expanding from $N=6$ exploratory cohorts to $J=15$ confirmatory cohorts would be "statistically sufficient" to resolve all inferential questions.

**This assessment formally refutes that assertion.** While expanding to $J=15$ (comprising $J_{\text{Tier A}} = 10$ pure tumor-subtype cohorts and $J_{\text{Tier B}} = 5$ secondary phenotype cohorts) substantially improves minimum attainable rank-sum $p$-values (from $p_{\min} = 0.03125$ at $N=6$ to $p_{\min} = 2^{-14} \approx 6.1 \times 10^{-5}$ at $J=15$), statistical power and estimation precision vary dramatically across hypotheses:

1. **Foundational Methodological Hypotheses (H1a, H1b):** **EXCELLENT POWER ($>95\%$).** Because the discordance gap is large ($\Delta_{\text{gap}} \approx 0.40\text{--}0.50$), $J=15$ provides overwhelming power to reject stability-accuracy coupling.
2. **Primary Comparative Baselines (Family 1, $M=8$):** **MODERATE TO LOW POWER.** Under Holm-Bonferroni correction ($\alpha_{(1)} = 0.00625$), $J=15$ achieves $80\%$ power only for very large effect sizes ($d_z \ge 1.07$). On the pure Tier A subset ($J=10$), $80\%$ power requires $d_z \ge 1.35$. Subtle differences ($d_z \le 0.50$) will remain undetectable.
3. **Bimodality Gating Advantage (H2a):** **HIGHLY CONTINGENT POWER ($35\%\text{--}70\%$).** If BGSS gain is concentrated in a subset of tumor types (as observed in the exploratory baseline where only 2 of 6 cohorts exhibited gains), cross-cohort dilution reduces effective power.
4. **Dense Attenuation Interaction (H2b):** **LOW POWER ($<30\%$).** As a difference-of-differences contrast involving four estimators, error propagation inflates variance, leaving $J=15$ underpowered unless the interaction effect is massive.
5. **Core Determinacy Equivalence via TOST (H3):** **SEVERE POWER DEFICIT ($<15\%$).** For an equivalence margin of $\delta = \pm 0.02$, $J=15$ requires $\sigma_D \le 0.025$ to attain $80\%$ power. If the cross-cohort standard deviation matches the exploratory baseline ($\sigma_D \approx 0.084$), the power of TOST is essentially $0\%$, making an **inconclusive outcome** the expected empirical result.

---

## 2. Mathematical Framework for Power and Precision

### 2.1 Paired Non-Parametric and Parametric Testing
For paired cohort evaluations (Full ICC-v2 vs. Baseline $m$), let $D_j = Y_{\text{ICC}, j} - Y_{m, j}$ denote the paired difference on cohort $j \in \{1, \dots, J\}$. Under the paired $t$-test (which serves as a tight lower bound on the asymptotic relative efficiency of the Wilcoxon signed-rank test, $\text{ARE} \ge 0.864$ and $\text{ARE} = 0.955$ for normal errors):
- Standardized effect size: $d_z = \frac{\mu_D}{\sigma_D}$.
- Non-centrality parameter: $\lambda = d_z \sqrt{J}$.
- Exact power under non-central $t$-distribution with $\nu = J - 1$ degrees of freedom:
  $$\text{Power} = 1 - T_{\nu, \lambda}\left(t_{1 - \alpha/2, \nu}\right) + T_{\nu, \lambda}\left(-t_{1 - \alpha/2, \nu}\right)$$

### 2.2 Minimum Detectable Effect Size (MDES) for $J = 15$ and $J = 10$
Table 1 summarizes the Minimum Detectable Effect Size ($d_z$) required to achieve $80\%$ and $90\%$ statistical power across relevant significance thresholds.

#### Table 1: Minimum Detectable Effect Size ($d_z$) for Confirmatory Cohorts
| Inferential Context | Nominal / Adjusted $\alpha$ | Directionality | Critical $t$ ($J=15, \nu=14$) | MDES $J=15$ ($80\%$ Power) | Critical $t$ ($J=10, \nu=9$) | MDES $J=10$ ($80\%$ Power) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Unadjusted Paired Test** | $\alpha = 0.05000$ | Two-sided | $2.145$ | **$0.778$** | $2.262$ | **$0.999$** |
| **Unadjusted One-Sided Test** | $\alpha = 0.05000$ | One-sided | $1.761$ | **$0.648$** | $1.833$ | **$0.817$** |
| **Family 2 Holm Step 1 ($M=3$)** | $\alpha = 0.01667$ | One-sided | $2.378$ | **$0.812$** | $2.569$ | **$1.045$** |
| **Family 2 Holm Step 2 ($M=3$)** | $\alpha = 0.02500$ | One-sided | $2.145$ | **$0.751$** | $2.262$ | **$0.955$** |
| **Family 1 Holm Step 1 ($M=8$)** | $\alpha = 0.00625$ | Two-sided | $3.160$ | **$1.068$** | $3.581$ | **$1.350$** |
| **Family 1 Holm Step 4 ($M=8$)** | $\alpha = 0.01000$ | Two-sided | $2.977$ | **$1.018$** | $3.250$ | **$1.258$** |
| **Family 1 Holm Step 8 ($M=8$)** | $\alpha = 0.05000$ | Two-sided | $2.145$ | **$0.778$** | $2.262$ | **$0.999$** |

**Key Takeaway:** In the primary Tier A suite ($J=10$), an effect must exceed $d_z = 1.35$ to survive Holm step-down correction. Even in the pooled $J=15$ suite, any baseline difference smaller than $d_z = 1.07$ will fail Holm-adjusted significance.

---

## 3. Power Analysis of Individual Confirmatory Hypotheses

### 3.1 Hypothesis 1: Stability–Accuracy Decoupling and False Confidence Gap

#### H1a: Rank Correlation Decoupling ($\rho < 0.30$ vs. $\rho \ge 0.50$)
- Null value: $z(\rho_0) = z(0.50) \approx 0.5493$.
- Expected true correlation based on exploratory audit: Across high-dimensional biomedical cohorts, $\hat{\rho} \in [-0.15, +0.10]$, yielding true mean $z(\rho_1) \approx 0.00$.
- Standardized gap: $\Delta z = 0.5493 - 0.00 = 0.5493$.
- Across $J = 15$ independent cohort estimates: $\text{SE}_{\bar{z}} = \frac{\sigma_z}{\sqrt{15}} \approx \frac{0.35}{\sqrt{15}} \approx 0.090$.
- Non-centrality parameter: $\lambda = \frac{0.5493}{0.090} \approx 6.10$.
- **Statistical Power:** **$> 99.9\%$**. Rejecting $H_{0,1\text{a}}$ is virtually guaranteed under realistic high-dimensional conditions.

#### H1b: Discordance Gap ($\Delta_{\text{gap}} > 0.20$ vs. $\Delta_0 = 0.05$)
- Null threshold: $\Delta_0 = 0.05$. Target alternative: $\Delta_1 = 0.20$.
- Observed gap in exploratory baseline: $\bar{\Delta} = 0.485$ across non-degenerate partitions, with cross-cohort $\sigma_D \approx 0.15$.
- Standardized effect size: $d_z = \frac{0.485 - 0.05}{0.15} = \frac{0.435}{0.15} = 2.90$.
- **Statistical Power:** **$> 99.9\%$**. Decisive power to confirm the discordance gap.

---

### 3.2 Hypothesis 2: Bimodality Gating Advantage and Dense Attenuation

#### 3.2.1 H2a: BGSS Gating Heterogeneity and Biological Dilution
In the exploratory audit of six cohorts, BGSS gain over matched random gating was not uniform:
- Responsive cohorts ($2/6 = 33.3\%$): Leukemia ($\Delta = +0.398$) and SRBCT ($\Delta = +0.447$).
- Non-responsive cohorts ($4/6 = 66.7\%$): Colon ($+0.078$), CNS ($+0.007$), Prostate ($+0.004$), Ovarian ($-0.012$).

Let $\pi_{\text{resp}}$ denote the true prevalence of biologically responsive cancer cohorts in the universe of Tier A/B candidates.
- If a cohort is responsive: $\mu_{\text{resp}} \approx +0.40, \sigma_{\text{resp}} \approx 0.10$.
- If a cohort is non-responsive: $\mu_{\text{null}} \approx +0.02, \sigma_{\text{null}} \approx 0.04$.

#### Table 2: Projected Statistical Power for H2a ($J = 15$, Holm $\alpha = 0.01667$ One-Sided)
| Responsive Prevalence ($\pi_{\text{resp}}$) | Expected Responsive Cohorts ($k$) | Population Mean $\mu_D$ | Population SD $\sigma_D$ | Standardized Effect $d_z$ | Projected Power ($J=15$) | Projected Power ($J=10$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$10\%$** | $1.5$ | $+0.058$ | $0.118$ | $0.492$ | **$26.4\%$** | **$16.2\%$** |
| **$20\%$** | $3.0$ | $+0.096$ | $0.154$ | $0.623$ | **$45.1\%$** | **$28.5\%$** |
| **$30\%$ (Baseline)** | $4.5$ | $+0.134$ | $0.177$ | $0.757$ | **$65.8\%$** | **$46.3\%$** |
| **$40\%$** | $6.0$ | $+0.172$ | $0.188$ | $0.915$ | **$82.6\%$** | **$64.9\%$** |
| **$50\%$** | $7.5$ | $+0.210$ | $0.191$ | $1.099$ | **$93.1\%$** | **$80.5\%$** |

**Conclusion on H2a:** If bimodal lineage markers exist in only $20\text{--}30\%$ of tumor types, power drops below $66\%$ for $J=15$ and below $47\%$ for $J=10$. A failure to reject does not disprove BGSS efficacy; it demonstrates cross-cancer biological heterogeneity.

#### 3.2.2 H2b: Dense-Consensus Attenuation Interaction Power Derivation
Hypothesis 2b evaluates the difference-of-differences contrast:
$$D_{2\text{b}, j} = \left(\text{ARI}_{\text{BGSS, Bip}, j} - \text{ARI}_{\text{Random, Bip}, j}\right) - \left(\text{ARI}_{\text{BGSS, Dense}, j} - \text{ARI}_{\text{Random, Dense}, j}\right)$$

Because $D_{2\text{b}}$ compounds the estimation errors of four separate algorithmic configurations across cohorts:
$$\text{Var}(D_{2\text{b}}) = \text{Var}(D_{\text{Bip}}) + \text{Var}(D_{\text{Dense}}) - 2\text{Cov}(D_{\text{Bip}}, D_{\text{Dense}})$$
Assuming comparable variance ($\sigma_{D, \text{Bip}} \approx \sigma_{D, \text{Dense}} \approx \sigma_D$) and moderate cross-topology correlation ($\rho \approx 0.35$):
$$\sigma_{D2\text{b}} = \sqrt{2\sigma_D^2(1 - \rho)} = \sigma_D \sqrt{2(0.65)} \approx 1.14 \, \sigma_D$$

With $\sigma_D \approx 0.177$, the interaction standard deviation is $\sigma_{D2\text{b}} \approx 0.202$.
In the exploratory baseline, the observed interaction gain was $\mu_{D2\text{b}} \approx +0.139 - (+0.031) \approx +0.108$.
- Resulting standardized effect size: $d_z = \frac{0.108}{0.202} \approx 0.535$.
- At Holm-adjusted one-sided $\alpha = 0.025$ ($t_{\text{crit}} = 2.145$ for $\nu = 14$):
  $$\lambda = 0.535 \sqrt{15} \approx 2.072 \implies \mathbf{\text{Power} \approx 36.5\%} \quad (J=15)$$
- On the pure Tier A subset ($J=10, \nu = 9$):
  $$\lambda = 0.535 \sqrt{10} \approx 1.692 \implies \mathbf{\text{Power} \approx 21.8\%} \quad (J=10)$$

**Auditor Warning on H2b:** Hypothesis 2b is **severely underpowered ($22\%\text{--}37\%$)**. Testing this interaction contrast carries a high risk of a Type II error (false negative). The protocol must openly disclose this limitation and treat H2b as an exploratory mechanistic contrast.

---

### 3.3 Hypothesis 3: Core Determinacy Equivalence via TOST (The Precision Bottleneck)

#### Mathematical Formulation of Equivalence Power
Under the Two One-Sided Tests (TOST) procedure with equivalence bounds $[-\delta, +\delta] = [-0.02, +0.02]$ and significance level $\alpha = 0.05$:
Equivalence is established if the $(1 - 2\alpha) = 90\%$ confidence interval for the paired difference lies entirely within $[-0.02, +0.02]$.
The half-width of the $90\%$ confidence interval is:
$$W_{0.90} = t_{0.95, \nu} \frac{\sigma_D}{\sqrt{J}} = 1.761 \frac{\sigma_D}{\sqrt{15}} \approx 0.4548 \, \sigma_D$$

For the confidence interval to fit inside $[-0.02, +0.02]$ when the true mean difference is $\mu_D = 0$:
$$W_{0.90} < 0.02 \implies \sigma_D < \frac{0.02}{0.4548} \approx \mathbf{0.0440}$$
If $\sigma_D \ge 0.044$, the interval width exceeds the equivalence corridor, and equivalence can **NEVER** be established, even if the observed sample mean is exactly zero!

#### Table 3: Exact TOST Equivalence Power for $J = 15$ ($\delta = \pm 0.02, \alpha = 0.05$)
| Paired Difference SD ($\sigma_D$) | Standard Error ($\text{SE} = \sigma_D/\sqrt{15}$) | $90\%$ CI Half-Width ($W_{0.90}$) | Maximum Allowable $|\bar{D}|$ for Equivalence | Exact TOST Power ($\mu_D = 0$) |
| :---: | :---: | :---: | :---: | :---: |
| **$0.010$** | $0.00258$ | $\pm 0.00455$ | $0.0154$ | **$>99.9\%$** |
| **$0.015$** | $0.00387$ | $\pm 0.00682$ | $0.0132$ | **$99.6\%$** |
| **$0.020$** | $0.00516$ | $\pm 0.00909$ | $0.0109$ | **$94.7\%$** |
| **$0.025$** | $0.00645$ | $\pm 0.01137$ | $0.0086$ | **$79.8\%$** |
| **$0.030$** | $0.00775$ | $\pm 0.01364$ | $0.0064$ | **$57.4\%$** |
| **$0.035$** | $0.00904$ | $\pm 0.01591$ | $0.0041$ | **$34.2\%$** |
| **$0.040$** | $0.01033$ | $\pm 0.01819$ | $0.0018$ | **$13.7\%$** |
| **$0.045$** | $0.01162$ | $\pm 0.02046$ | None (Interval $> 0.04$) | **$0.0\%$** |
| **$0.084$ (Baseline)**| **$0.02169$** | **$\pm 0.03820$** | **None (Interval $= 0.076$)**| **$0.0\%$** |

#### The Impossibility of Declaring Equivalence under High Empirical Variance
In the exploratory Pass F audit, the empirical paired differences between certified core anchors and uniform random landmarks exhibited:
$$\bar{D}_{\text{exploratory}} = +0.0188, \quad \sigma_{D, \text{exploratory}} = \mathbf{0.0839}$$
If the confirmatory cohorts exhibit comparable inter-cohort variance ($\sigma_D \approx 0.08$):
- Standard error on $J = 15$ cohorts: $\text{SE} \approx 0.0217$.
- $90\%$ Confidence Interval: $[+0.0188 - 1.761(0.0217), +0.0188 + 1.761(0.0217)] = [-0.0194, +0.0570]$.
- This interval spans a width of $0.0764$, completely overflowing the $\pm 0.02$ corridor.

#### Sample Size Required to Achieve $80\%$ Equivalence Power at Margin $\delta = \pm 0.02$:
- If $\sigma_D = 0.025$: $J_{\text{required}} = 15$ cohorts.
- If $\sigma_D = 0.035$: $J_{\text{required}} = 29$ cohorts.
- If $\sigma_D = 0.050$: $J_{\text{required}} = 58$ cohorts.
- If $\sigma_D = 0.084$: $J_{\text{required}} \approx 162$ cohorts.

**Definitive Scientific Mandate:** Claiming that $J=15$ is "sufficient" to certify Proposition 2 core anchors as an empirical null is mathematically unsupportable. Unless within-cohort averaging across 30 seeds drastically dampens variance to $\sigma_D < 0.025$, **the outcome of TOST will be INCONCLUSIVE.**

The protocol explicitly mandates:
1. Permitting an **inconclusive** verdict.
2. Forbidding the authors from reporting an inconclusive test as evidence of an empirical null.
3. Explicitly stating in the final manuscript that while core anchors provide no statistically detectable gain, equivalence at the $\pm 0.02$ resolution cannot be formally proven with $J=15$ cohorts.

---

## 4. Synthesis and Protocol Risk Matrix

Table 4 summarizes the statistical risks and pre-specified protocol remediations for all planned tests.

#### Table 4: Risk and Resolution Ledger across Confirmatory Families
| Test / Hypothesis | Nominal Sample Size | Primary Statistical Risk | Risk Severity | Protocol Remediation & Decision Rule |
| :--- | :---: | :--- | :---: | :--- |
| **H1a (Correlation Decoupling)** | $J = 15$ | Conflating method and cohort variance via pseudoreplication | **CRITICAL** | Compute Spearman $\hat{\rho}_j$ per cohort; test Fisher $z$ across cohorts; fit linear mixed model. |
| **H1b (Discordance Gap)** | $J = 15$ | Small sample distortion; extreme outliers | **LOW** | Paired Wilcoxon against $\Delta_0 = 0.05$; $95\%$ cohort-clustered bootstrap intervals. |
| **H2a (BGSS vs. Random)** | $J = 15$ (Tier A: $10$) | Dilution from non-responsive cancer types | **HIGH** | Primary test on pure Tier A ($J=10$); report forest plots and response fraction. |
| **H2b (Dense Attenuation)** | $J = 15$ (Tier A: $10$) | Error propagation across 4 estimators (power $<35\%$) | **HIGH** | Document severe power deficit; treat as secondary mechanistic exploration. |
| **H3 (Core Equivalence)** | $J = 15$ | Severe underpowering at $\pm 0.02$ margin | **FATAL IF UNMANAGED** | Replace failure-to-reject with TOST; mandate reporting confidence intervals; explicitly permit and document inconclusive verdict. |
| **Family 1 (Baselines)** | $J = 15$ (Tier A: $10$) | False negatives on moderate effect sizes ($d_z < 0.80$) | **HIGH** | Require both $p_{\text{adj}} < 0.05$ AND $\text{Median}(D) > 0$; disclose raw and adjusted $p$-values. |