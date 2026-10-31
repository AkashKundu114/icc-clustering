import pandas as pd

df = pd.read_csv('results/stability_degeneracy_audit.csv')
non_control = df[~df['is_control']].copy()

print(f'Total non-control cells: {len(non_control)}')

degen = non_control[non_control['degen_rate'] > 0.10]
print(f'Degenerate cells (degen_rate > 0.10): {len(degen)}')
for idx, r in degen.iterrows():
    m = r['model']
    d = r['dataset']
    dr = r['degen_rate'] * 100
    mf = r['mean_min_frac'] * 100
    s = r['stab']
    a = r['acc']
    print(f'  {m:12s} on {d:10s}: degen_rate={dr:5.1f}%, min_frac={mf:5.1f}%, stab={s:6.3f}, acc={a:6.3f}')

non_degen = non_control[non_control['degen_rate'] <= 0.10]
print(f'Non-degenerate cells: {len(non_degen)}')

# Check Table 4 dagger cells in LaTeX
with open('paper/gen/table16_degeneracy_audit.tex', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print('\nCounting daggers in table16_degeneracy_audit.tex:')
for line in text.splitlines():
    if r'^\dagger' in line:
        # count occurrences of ^\dagger in this line
        c = line.count(r'^\dagger')
        m_name = line.split('&')[0].strip()
        print(f'  {m_name:25s}: {c} daggers')
