# -*- coding: utf-8 -*-
"""
scripts/remove_internal_labels.py

Removes internal development labels:
- 'Exp 8a--8f', 'Exp 8a', 'Exp 8b', etc.
- 'Experiment 8d', 'Experiment 8e'
- 'Canonical seeds', 'canonical seeds', 'canonical random seeds'
- 'Phase 3 sub-experiments'
across paper/main.tex, springer_manuscript/main.tex, and all gen/*.tex files.
"""

from pathlib import Path
import re

def clean_text_content(text: str) -> str:
    # 1. Main text Exp 8 replacements
    text = text.replace(r'(Exp~8d, Table~\ref{tab:exp8d_distance})', r'(Table~\ref{tab:exp8d_distance})')
    text = text.replace(r'($L \in [160, 380]$, Exp~8e)', r'($L \in [160, 380]$, Table~\ref{tab:exp8e_large_k})')
    text = text.replace(r'\paragraph{Experimental Protocol and Seed Specifications (Exp 8a--8f):}', r'\paragraph{Experimental Protocol and Evaluation Modules:}')
    text = text.replace(r'all Phase 3 sub-experiments follow pre-specified deterministic seed schedules:', r'all targeted evaluation modules follow pre-specified deterministic seed schedules:')
    text = text.replace(r'\item \textbf{Exp 8a (CoHiRF Benchmark):}', r'\item \textbf{CoHiRF Comparative Evaluation:}')
    text = text.replace(r'\item \textbf{Exp 8b (Anchor Selection):}', r'\item \textbf{Anchor Landmark Selection:}')
    text = text.replace(r'\item \textbf{Exp 8c (Feature Gating):}', r'\item \textbf{Feature Gating Evaluation:}')
    text = text.replace(r'\item \textbf{Exp 8d (Distance Metrics and Geometry Simulation):}', r'\item \textbf{Distance Metrics and Geometry Simulation:}')
    text = text.replace(r'\item \textbf{Exp 8e (Large-$K$ Anchor Budget Scaling):}', r'\item \textbf{Large-$K$ Anchor Budget Scaling:}')
    text = text.replace(r'\item \textbf{Exp 8f (Hyperparameter Sensitivity Grid):}', r'\item \textbf{Hyperparameter Sensitivity Grid:}')
    
    text = text.replace(r'\lfloor \alpha D \rfloor$, Exp~8c, evaluated on the 30 benchmark seeds', r'\lfloor \alpha D \rfloor$, evaluated on the 30 benchmark seeds')
    text = text.replace(r'over 10 seeds ($\{42, \dots, 51\}$, Exp~8f)', r'over 10 seeds ($\{42, \dots, 51\}$)')
    text = text.replace(r'across $L \in \{20, 40, 60, 80\}$ (Exp~8f) yields flat surfaces', r'across $L \in \{20, 40, 60, 80\}$ yields flat surfaces')
    text = text.replace(r'balanced determinacy anchors (Exp~8b) across all 30 canonical benchmark seeds', r'balanced determinacy anchors across all 30 benchmark seeds')
    text = text.replace(r'on the canonical 30 benchmark seeds', r'on the 30 benchmark seeds')
    text = text.replace(r'30 independent canonical random seeds', r'30 independent random seeds')
    text = text.replace(r'10 stratified canonical train/test splits', r'10 stratified random train/test splits')
    text = text.replace(r'across canonical seeds', r'across independent random seeds')
    text = text.replace(r'canonical random seeds', r'independent random seeds')
    text = text.replace(r'canonical seeds', r'random seeds')

    # 2. Table captions
    text = text.replace(r'Experiment 8d: ', '')
    text = text.replace(r'Experiment 8e: ', '')
    text = text.replace(r'Canonical Seeds', 'Random Seeds')
    text = text.replace(r'Canonical Random Seeds', 'Random Seeds')
    text = text.replace(r'Across Canonical Seeds:', 'Across Random Seeds:')
    
    return text

def main():
    # Process main.tex
    for main_path in ['paper/main.tex', 'springer_manuscript/main.tex']:
        p = Path(main_path)
        content = p.read_text(encoding='utf-8')
        cleaned = clean_text_content(content)
        p.write_text(cleaned, encoding='utf-8')
        print(f"[+] Cleaned {main_path}")

    # Process all gen/*.tex files
    for folder in ['paper/gen', 'springer_manuscript/gen']:
        p_folder = Path(folder)
        for tex_file in p_folder.glob('*.tex'):
            content = tex_file.read_text(encoding='utf-8', errors='ignore')
            cleaned = clean_text_content(content)
            tex_file.write_text(cleaned, encoding='utf-8')
            print(f"[+] Cleaned {tex_file}")

if __name__ == '__main__':
    main()
