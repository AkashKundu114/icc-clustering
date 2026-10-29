"""
Patch paper/main.tex and springer_manuscript/main.tex to resolve:
1. 2,750 -> 3,000 model fits on line 303
2. BGSS candidate pool description
3. 'certified core' -> 'high-determinacy core' terminology
"""

import sys

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update 2,750 fit count
    old_str1 = r'This design yields $(6 \times 11 \times 30) + (7 \times 11 \times 10) = 2{,}750$ total benchmark model fits.'
    new_str1 = r'This design yields $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ total benchmark model fits across the 12 evaluated pipelines.'

    if old_str1 in content:
        content = content.replace(old_str1, new_str1)
        print(f"[{filepath}] Replaced 2,750 fit count -> 3,000.")

    # 2. Update BGSS candidate pool explanation
    old_str2 = r'selects the top candidate pool of size $\min(D, \max(K, \lfloor \alpha \cdot D \rfloor))$ with default $\alpha = 0.15$ and minimum cap $\min(100, D)$.'
    new_str2 = r'selects the top candidate pool of size $\min(D, \max(K, \max(100, \lfloor \alpha \cdot D \rfloor)))$ with default $\alpha = 0.15$. Setting a minimum floor of $\min(100, D)$ candidate features ensures sufficient subspace diversity across base clusterers.'

    if old_str2 in content:
        content = content.replace(old_str2, new_str2)
        print(f"[{filepath}] Updated BGSS candidate pool explanation.")

    # 3. Update 'certified core' in abstract
    old_str3 = r'while anchor certification provides no statistical benefit ($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$])'
    new_str3 = r'while determinacy-based anchor selection provides no statistical benefit ($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$])'
    if old_str3 in content:
        content = content.replace(old_str3, new_str3)
        print(f"[{filepath}] Updated abstract anchor certification phrasing.")

    # 4. Update 'certified core' in item 3
    old_str4 = r'Conversely, determinacy anchor certification yields an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$).'
    new_str4 = r'Conversely, determinacy-based anchor selection yields an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$).'
    if old_str4 in content:
        content = content.replace(old_str4, new_str4)
        print(f"[{filepath}] Updated contribution item 3 anchor certification phrasing.")

    # 5. Update 'certified core' in line 223
    old_str5 = r'sampling uniformly at random from within the certified core set $\mathcal{C} = \{i : \sigma_i \ge \tau_{\text{core}}\}$ (in contrast to variant V4, which draws anchors uniformly across the full dataset without determinacy screening). We sample uniformly within the core set rather than running $k$-means prototype clustering on the core points (as in FastMVC) or constructing hierarchical $k$-d trees because random subsampling executes in strictly $O(L)$ time with zero pairwise distance evaluations, avoiding the $O(|\mathcal{C}| \cdot D \cdot L)$ cost of preliminary clustering passes in high-dimensional noise regimes. Furthermore, empirical ablation (Section~\ref{sec:ablation}, Table~\ref{tab:component_contributions}) confirms that determinacy-ordered anchors achieve accuracy statistically indistinguishable from uniform random anchors ($V_5$ vs. $V_4$: $\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), establishing that bipartite graph compression rather than anchor certification is the primary operational driver.'
    new_str5 = r'sampling uniformly at random from within the high-determinacy core set $\mathcal{C} = \{i : \sigma_i \ge \tau_{\text{core}}\}$ (in contrast to variant V4, which draws anchors uniformly across the full dataset without determinacy screening). We sample uniformly within the high-determinacy core rather than running $k$-means prototype clustering on the core points (as in FastMVC) or constructing hierarchical $k$-d trees because random subsampling executes in strictly $O(L)$ time with zero pairwise distance evaluations, avoiding the $O(|\mathcal{C}| \cdot D \cdot L)$ cost of preliminary clustering passes in high-dimensional noise regimes. Furthermore, empirical ablation (Section~\ref{sec:ablation}, Table~\ref{tab:component_contributions}) confirms that determinacy-selected anchors achieve accuracy statistically indistinguishable from uniform random anchors ($V_5$ vs. $V_4$: $\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), establishing that bipartite graph compression rather than determinacy anchor selection is the primary operational driver.'
    if old_str5 in content:
        content = content.replace(old_str5, new_str5)
        print(f"[{filepath}] Updated Section 3 anchor selection phrasing.")

    # 6. Update 'certified core' in figure caption 382
    old_str6 = r'\caption{Inductive generalization performance on held-out test splits ($20\%$). (a) When trained on 50\% certified core points, downstream classifiers achieve parity with 100\% full-data training under low-to-moderate noise ($D_{\text{noise}} \le 50$), while under high noise ($D_{\text{noise}} \ge 1{,}000$), core-only training exhibits a 5--21 percentage point deficit due to reduced training sample size in noise-dominated regimes. (b) Under heavy noise corruption ($D_{\text{noise}} \ge 1{,}000$), training on unguided pseudo-labels (both full and core subsets) degrades toward random chance accuracy ($33.6\%$--$36.0\%$ vs. $33.3\%$ chance level for $K=3$), demonstrating that core filtering alone cannot rescue corrupted pseudo-labels without prior feature gating.}'
    new_str6 = r'\caption{Inductive generalization performance on held-out test splits ($20\%$). (a) When trained on 50\% high-determinacy core points, downstream classifiers achieve parity with 100\% full-data training under low-to-moderate noise ($D_{\text{noise}} \le 50$), while under high noise ($D_{\text{noise}} \ge 1{,}000$), core-only training exhibits a 5--21 percentage point deficit due to reduced training sample size in noise-dominated regimes. (b) Under heavy noise corruption ($D_{\text{noise}} \ge 1{,}000$), training on unguided pseudo-labels (both full and core subsets) degrades toward random chance accuracy ($33.6\%$--$36.0\%$ vs. $33.3\%$ chance level for $K=3$), demonstrating that high-determinacy filtering alone cannot rescue corrupted pseudo-labels without prior feature gating.}'
    if old_str6 in content:
        content = content.replace(old_str6, new_str6)
        print(f"[{filepath}] Updated figure caption core filtering phrasing.")

    # 7. Update 'certified core' in paragraph 387
    old_str7 = r'We evaluated the inductive utility of the certified core $\mathcal{C}_{\text{core}}$ when training downstream supervised classifiers on held-out test data (20\% split). As shown in Fig.~\ref{fig:exp1_oracle}, classifiers trained on 50\% certified core points attain performance comparable to training on 100\% of the data under low-to-moderate noise ($D_{\text{noise}} \le 50$).'
    new_str7 = r'We evaluated the inductive utility of the high-determinacy core $\mathcal{C}_{\text{core}}$ when training downstream supervised classifiers on held-out test data (20\% split). As shown in Fig.~\ref{fig:exp1_oracle}, classifiers trained on 50\% high-determinacy core points attain performance comparable to training on 100\% of the data under low-to-moderate noise ($D_{\text{noise}} \le 50$).'
    if old_str7 in content:
        content = content.replace(old_str7, new_str7)
        print(f"[{filepath}] Updated paragraph core evaluation phrasing.")

    # 8. Update 'certified core' in section 606 & 607
    old_str8 = r'\subsection{Anchor Certification Null Result}\label{sec:ablation_null}'
    new_str8 = r'\subsection{High-Determinacy Anchor Selection Null Result}\label{sec:ablation_null}'
    if old_str8 in content:
        content = content.replace(old_str8, new_str8)
        print(f"[{filepath}] Updated subsection heading.")

    old_str9 = r'A key empirical insight from Table~\ref{tab:component_contributions} is that determinacy-based anchor certification provides no statistically significant accuracy benefit over uniform random anchors. Full ICC-v2 (V5: certified core anchors) achieves a subgroup mean ARI of $\mathbf{\AblationHighDSubgroupFullIccVTwo}$ compared to $\AblationHighDSubgroupBgssRandomAnchor$ for V4 with uniform random anchors.'
    new_str9 = r'A key empirical insight from Table~\ref{tab:component_contributions} is that determinacy-based anchor selection provides no statistically significant accuracy benefit over uniform random anchors. Full ICC-v2 (V5: high-determinacy core anchors) achieves a subgroup mean ARI of $\mathbf{\AblationHighDSubgroupFullIccVTwo}$ compared to $\AblationHighDSubgroupBgssRandomAnchor$ for V4 with uniform random anchors.'
    if old_str9 in content:
        content = content.replace(old_str9, new_str9)
        print(f"[{filepath}] Updated ablation text.")

    # 9. Update 'certified core' in line 616
    old_str10 = r'significantly lower than both uniform random anchors (V4: $0.190 \pm 0.301$) and certified core anchors (V5: $0.225 \pm 0.318$). In extreme high-dimensional noise regimes ($D/N > 20$), Lloyd\'s algorithm converges to degraded centroids corrupted by ambient noise, demonstrating that landmark anchors should be selected directly from empirical observations (or certified core subsets) rather than synthesized via iterative distance optimization.'
    new_str10 = r'significantly lower than both uniform random anchors (V4: $0.190 \pm 0.301$) and high-determinacy core anchors (V5: $0.225 \pm 0.318$). In extreme high-dimensional noise regimes ($D/N > 20$), Lloyd\'s algorithm converges to degraded centroids corrupted by ambient noise, demonstrating that landmark anchors should be selected directly from empirical observations (or high-determinacy core subsets) rather than synthesized via iterative distance optimization.'
    if old_str10 in content:
        content = content.replace(old_str10, new_str10)
        print(f"[{filepath}] Updated alternative anchors text.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for p in ['paper/main.tex', 'springer_manuscript/main.tex']:
        print(f"Patching {p}...")
        patch_file(p)
