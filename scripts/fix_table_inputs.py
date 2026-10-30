# -*- coding: utf-8 -*-
from pathlib import Path

def main():
    for rel_path in ['paper/main.tex', 'springer_manuscript/main.tex']:
        p = Path(rel_path)
        text = p.read_text(encoding='utf-8')

        # 1. table03
        t1_old = r'Table~\ref{tab:inductive_direct} compares closed-form centroid assignment (Eq.~\eqref{eq:centroid_proj}) against alternative mapping methods across 10 random train/test splits (80\% fit, 20\% query). Centroid assignment'
        t1_new = r'Table~\ref{tab:inductive_direct} compares closed-form centroid assignment (Eq.~\eqref{eq:centroid_proj}) against alternative mapping methods across 10 random train/test splits (80\% fit, 20\% query).' + '\n\n' + r'\input{gen/table03_inductive_generalization.tex}' + '\n\n' + r'Centroid assignment'

        if t1_old in text:
            text = text.replace(t1_old, t1_new)
            print(f"[+] Added table03 in {rel_path}")
        elif r'\input{gen/table03_inductive_generalization.tex}' in text:
            print(f"[=] table03 already present in {rel_path}")
        else:
            print(f"[-] Could not find insertion point for table03 in {rel_path}")

        # 2. table12
        t2_old = r'Table~\ref{tab:factorial} reports a $2 \times 2$ factorial decomposition of subgroup mean ARI across the six high-$D$ cohorts. Without gating'
        t2_new = r'Table~\ref{tab:factorial} reports a $2 \times 2$ factorial decomposition of subgroup mean ARI across the six high-$D$ cohorts.' + '\n\n' + r'\input{gen/table12_factorial_decomposition.tex}' + '\n\n' + r'Without gating'

        if t2_old in text:
            text = text.replace(t2_old, t2_new)
            print(f"[+] Added table12 in {rel_path}")
        elif r'\input{gen/table12_factorial_decomposition.tex}' in text:
            print(f"[=] table12 already present in {rel_path}")
        else:
            print(f"[-] Could not find insertion point for table12 in {rel_path}")

        p.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
