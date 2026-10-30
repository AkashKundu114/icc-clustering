# -*- coding: utf-8 -*-
import re
from pathlib import Path

terms = [
    'Stable but Wrong',
    'stability trap',
    'trap',
    'entrap',
    'lock onto',
    'pathology',
    'massive',
    'firmly',
    'proving',
    'severe'
]

def main():
    p = Path('paper/main.tex')
    text = p.read_text(encoding='utf-8')
    print('=== Prohibited Informal Terms Audit ===')
    found_any = False
    for t in terms:
        matches = list(re.finditer(r'\b' + re.escape(t) + r'\b', text, re.IGNORECASE))
        if matches:
            found_any = True
            print(f"Found {len(matches)} occurrences of '{t}':")
            for m in matches[:5]:
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                print("   ...", text[start:end].replace('\n', ' '), "...")
    if not found_any:
        print("ALL CLEAN! Zero prohibited informal terms found in paper/main.tex!")

if __name__ == '__main__':
    main()
