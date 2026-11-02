from pathlib import Path
import re, sys
root=Path(__file__).resolve().parent
tex=(root/'main.tex').read_text(encoding='utf-8')
errs=[]
for env in re.findall(r'\\begin\{([^}]+)\}',tex):
 if tex.count('\\begin{'+env+'}')!=tex.count('\\end{'+env+'}'):
  errs.append(f'unbalanced environment {env}')
for path in re.findall(r'\\input\{([^}]+)\}',tex):
 if not (root/path).is_file():errs.append(f'missing input {path}')
keys=set(re.findall(r'\\bibitem\{([^}]+)\}',tex))
cites=set()
for m in re.findall(r'\\cite\{([^}]+)\}',tex):cites.update(x.strip() for x in m.split(','))
for k in sorted(cites-keys):errs.append(f'undefined citation {k}')
for k in sorted(keys-cites): print('uncited_reference='+k)
# Require linked results file and dynamically regenerated values.
import json
obj=json.loads((root/'aggregate_results.json').read_text(encoding='utf-8'))
if obj['results']['n_cells']!=72 or obj['results']['n_datasets']!=6 or obj['results']['n_methods']!=12:errs.append('unexpected reconstructed design counts')
for macro,val in [('AggStability','0.516586'),('AggARI','0.052312'),('AggGap','0.464274'),('AggMedianGap','0.448407'),('AggNull','0.006620')]:
 if f'\\newcommand{{\\{macro}}}{{{val}}}' not in (root/'aggregate_macros.tex').read_text(encoding='utf-8'):errs.append(f'metric macro mismatch {macro}')
print('citation_keys='+','.join(sorted(cites)))
print('reference_keys='+','.join(sorted(keys)))
print(f'cell_count={obj["results"]["n_cells"]} datasets={obj["results"]["n_datasets"]} methods={obj["results"]["n_methods"]}')
if errs:
 print('FAIL');print('\n'.join(errs));sys.exit(1)
print('PASS static structure, inputs, citations, and aggregate linkage')
