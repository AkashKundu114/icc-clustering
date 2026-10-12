import os
import re

pattern = re.compile(r'[\'\"](Figure\s+\d+|Fig\.\s*\d+)', re.IGNORECASE)

for folder in ['experiments', 'scripts']:
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.py'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for i, line in enumerate(fp, 1):
                        if pattern.search(line):
                            print(f"{p}:{i} -> {line.strip()[:100]}")
