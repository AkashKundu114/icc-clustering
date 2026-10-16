# 02 — Mathematical Audit & Theorem Derivations

**Auditor:** Mathematical & Theoretical Auditor  
**Date:** October 13, 2026  
**Primary Target:** Equations, Propositions, Theorems, and Algorithmic Complexities in ICC-v2  

---

## 1. Proposition 1: Conditional Multimodality Separation Bound

### Original Statement in Manuscript
For a balanced two-component Gaussian mixture $0.5\mathcal{N}(-\Delta, \sigma^2) + 0.5\mathcal{N}(\Delta, \sigma^2)$, the bimodality coefficient satisfies $b_d > 5/9$ if and only if component separation satisfies $\Delta/\sigma > \sqrt{2}$.

### Independent Step-by-Step Derivation
Let $X \sim 0.5\mathcal{N}(-\Delta, \sigma^2) + 0.5\mathcal{N}(\Delta, \sigma^2)$. By symmetry about 0:
- Odd central moments vanish: $\mu_1 = 0$, $\mu_3 = 0 \implies \text{Skewness } \gamma = 0$.
- The second moment (variance) is:
  $$\mu_2 = \mathbb{E}[X^2] = 0.5(\sigma^2 + \Delta^2) + 0.5(\sigma^2 + \Delta^2) = \sigma^2 + \Delta^2$$
- The fourth central moment is:
  $$\mu_4 = \mathbb{E}[X^4] = 0.5(3\sigma^4 + 6\sigma^2\Delta^2 + \Delta^4) + 0.5(3\sigma^4 + 6\sigma^2\Delta^2 + \Delta^4) = 3\sigma^4 + 6\sigma^2\Delta^2 + \Delta^4$$
- Pearson's kurtosis $\beta_2$ is:
  $$\beta_2 = \frac{\mu_4}{\mu_2^2} = \frac{3\sigma^4 + 6\sigma^2\Delta^2 + \Delta^4}{(\sigma^2 + \Delta^2)^2}$$
- Let $r = \frac{\Delta^2}{\sigma^2}$. Then:
  $$\beta_2 = \frac{3 + 6r + r^2}{(1 + r)^2} = \frac{(1+r)^2 + 4r + 2}{(1+r)^2} = 1 + \frac{4r + 2}{(1+r)^2}$$
- Sarle's Bimodality Coefficient is defined as:
  $$b = \frac{\gamma^2 + 1}{\beta_2} = \frac{1}{\beta_2} = \frac{(1+r)^2}{r^2 + 6r + 3}$$
- Setting $b > \frac{5}{9}$:
  $$\frac{(1+r)^2}{r^2 + 6r + 3} > \frac{5}{9} \iff 9(r^2 + 2r + 1) > 5(r^2 + 6r + 3)$$
  $$9r^2 + 18r + 9 > 5r^2 + 30r + 15$$
  $$4r^2 - 12r - 6 > 0 \iff 2r^2 - 6r - 3 > 0$$
- Solving the quadratic $2r^2 - 6r - 3 = 0$:
  $$r = \frac{6 \pm \sqrt{36 - 4(2)(-3)}}{4} = \frac{6 \pm \sqrt{36 + 24}}{4} = \frac{6 \pm \sqrt{60}}{4} = \frac{3 \pm \sqrt{15}}{2}$$
- Since $r \ge 0$, the root is:
  $$r = \frac{3 + \sqrt{15}}{2} \approx \frac{3 + 3.87298}{2} \approx 3.43649$$
- Hence, the separation ratio $\frac{\Delta}{\sigma} = \sqrt{r}$ satisfies:
  $$\frac{\Delta}{\sigma} > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx \sqrt{3.43649} \approx 1.85377$$

### Audit Verdict
- **Original Claim ($\sqrt{2} \approx 1.414$):** FALSE / MATHEMATICALLY DEFECTIVE.
- **Corrected Claim ($\approx 1.854$):** TRUE & PROVEN.
- **Implementation Status:** Corrected in `springer_manuscript/main.tex` and `docs/THEORETICAL_FOUNDATIONS.md`.

---

## 2. Proposition 2: Exact Linear-Memory Sample Determinacy Identity

### Claim in Manuscript
Let $S \in [0, 1]^{N \times N}$ be the ensemble co-association matrix defined by $S_{ij} = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\pi_m(i) = \pi_m(j)\}$. Then:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2}\sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
where $C_{m_1, m_2} \in \mathbb{N}^{K \times K}$ is the contingency matrix between base partitions $m_1$ and $m_2$.

### Independent Step-by-Step Derivation
By definition of $S_{ij}$:
$$S_{ij}^2 = \left(\frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\pi_m(i) = \pi_m(j)\}\right)^2 = \frac{1}{M^2}\sum_{m_1=1}^M \sum_{m_2=1}^M \mathbf{1}\{\pi_{m_1}(i) = \pi_{m_1}(j)\} \cdot \mathbf{1}\{\pi_{m_2}(i) = \pi_{m_2}(j)\}$$
Summing over all $j \in \{1, \dots, N\}$:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2}\sum_{m_1=1}^M \sum_{m_2=1}^M \sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(j) = \pi_{m_1}(i) \wedge \pi_{m_2}(j) = \pi_{m_2}(i)\}$$
Observe that the inner sum $\sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(j) = c_1 \wedge \pi_{m_2}(j) = c_2\}$ is precisely the definition of the entry $C_{m_1, m_2}(c_1, c_2)$ of the contingency matrix between partition $m_1$ and $m_2$.  
Setting $c_1 = \pi_{m_1}(i)$ and $c_2 = \pi_{m_2}(i)$, we obtain the exact identity:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2}\sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
Since the diagonal elements satisfy $S_{ii} = 1$, the off-diagonal quadratic determinacy is:
$$\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2 = \frac{1}{N-1}\left(\sum_{j=1}^N S_{ij}^2 - 1\right)$$

### Complexity Verification
- Computing $M(M-1)/2$ contingency matrices of size $K \times K$: For each pair $(m_1, m_2)$, a single pass over $N$ samples takes $O(N)$. Across all $M^2$ pairs: $O(M^2 N)$.
- Evaluating $\sigma_i$ for all $N$ samples: Each sample queries $M^2$ table lookups: $O(M^2 N)$.
- Storage: $O(M^2 K^2)$ or $O(K^2)$ if streaming pairs sequentially. No $N \times N$ matrix is ever constructed or stored!
- **Audit Verdict:** MATHEMATICALLY EXACT AND VALID. Matches implementation in `src/icc/consensus_v2.py`.

---

## 3. Theorem 1: Asymptotic Complexity & Transfer-Cut Equivalence

### Claim in Manuscript
ICC-v2 auxiliary memory complexity is $O(NL + L^2)$ and time complexity is $O(ND + M I_{\text{km}} N |\mathcal{F}_{\text{sub}}| K + MNL + NL^2 + L^3 + NLK + I_{\text{km}}NK^2)$.

### Audit Verification
1. **Feature Gating:** First 4 moments computed column-wise: $D$ loops of length $N \implies O(ND)$ time, $O(D)$ memory.
2. **Base Clusterings:** $M$ fits of K-Means on $|\mathcal{F}_{\text{sub}}|$ dimensions $\implies O(M \cdot I_{\text{km}} N |\mathcal{F}_{\text{sub}}| K)$.
3. **Anchor Graph $B \in [0, 1]^{N \times L}$:** $N \times L$ entries, each computed by comparing $M$ partition indicators $\implies O(MNL)$ time, $O(NL)$ memory words.
4. **Spectral Projection:** $W_{\text{anchor}} = B_{\text{norm}}^T B_{\text{norm}}$ takes $O(NL^2)$ time. Eigendecomposition of $L \times L$ matrix takes $O(L^3)$ time. Projection $U = B_{\text{norm}} V$ takes $O(NLK)$ time.
5. **Final K-Means on Embedding:** $N \times K$ space takes $O(I_{\text{km}} N K^2)$.
- **Audit Verdict:** The theoretical complexity bounds are ASYMPTOTICALLY SOUND under bounded anchor budget $L \ll N$.
