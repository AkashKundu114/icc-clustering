import re

def parse_bib(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    entries = []
    curr = None
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('@'):
            m = re.match(r'@(\w+)\s*\{\s*([^,]+),', line_s)
            if m:
                if curr:
                    entries.append(curr)
                curr = {'type': m.group(1).lower(), 'key': m.group(2).strip()}
        elif curr and '=' in line:
            parts = line.split('=', 1)
            k = parts[0].strip().lower()
            v = parts[1].strip().strip('{},').strip('"')
            curr[k] = v
    if curr:
        entries.append(curr)
    return entries

if __name__ == '__main__':
    entries = parse_bib('springer_manuscript/references.bib')
    print(f'Parsed {len(entries)} entries successfully!')
    for e in entries[:5]:
        print(' ', e['key'], '--> DOI:', e.get('doi'))
