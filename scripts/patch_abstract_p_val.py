for path in ['springer_manuscript/main.tex', 'paper/main.tex']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    old_str = 'Wilcoxon  = 0.031$ uncorrected,  = 6$)'
    new_str = 'Wilcoxon $p = 0.031$ uncorrected, $n = 6$)'
    assert old_str in text, f'{old_str} not in {path}'
    text = text.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Fixed {path} successfully!')
