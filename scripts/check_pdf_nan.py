import pypdf

reader = pypdf.PdfReader('paper/main.pdf')
full_text = ''
for i, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    full_text += f'\n--- PAGE {i+1} ---\n' + txt

nan_count = 0
for line in full_text.split('\n'):
    if '± nan' in line or 'nan ' in line or '±nan' in line:
        print('Found NaN:', line)
        nan_count += 1

print(f'Total NaN occurrences in PDF: {nan_count}')
assert nan_count == 0, 'Found NaN in PDF!'
print('PDF NaN check PASSED!')
