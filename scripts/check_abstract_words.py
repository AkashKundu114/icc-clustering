# -*- coding: utf-8 -*-
import re
from pathlib import Path

def main():
    text = Path('paper/main.tex').read_text(encoding='utf-8')
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.DOTALL)
    if m:
        raw_abstract = m.group(1).strip()
        # Count words in abstract
        words = raw_abstract.split()
        print(f"Raw word count: {len(words)}")
        # Check if 'stable clustering' is claimed as a property of GAC
        print("Contains 'stable clustering':", "stable clustering" in raw_abstract.lower())
        print("\n--- Abstract Text ---")
        print(raw_abstract)

if __name__ == '__main__':
    main()
