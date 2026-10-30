# -*- coding: utf-8 -*-
from pathlib import Path

def main():
    for rel_path in ['paper/main.tex', 'springer_manuscript/main.tex']:
        p = Path(rel_path)
        text = p.read_text(encoding='utf-8')
        old = 'is especially severe in graph-based methods'
        new = 'is especially pronounced in graph-based methods'
        assert old in text, f'{old} not in {rel_path}'
        text = text.replace(old, new)
        p.write_text(text, encoding='utf-8')
        print(f'Replaced in {rel_path}')

if __name__ == '__main__':
    main()
