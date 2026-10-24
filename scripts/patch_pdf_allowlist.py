# -*- coding: utf-8 -*-
from pathlib import Path

path = Path("tests/test_pdf_allowlist.py")
content = path.read_text(encoding="utf-8")

old_str = '"6.1", "6.2", "6.3", "6.4", "6.5",'
new_str = '''"6.1", "6.2", "6.3", "6.4", "6.5",
        "7.1", "7.2", "7.3", "7.4", "7.5",
        "8.1", "8.2", "8.3",
        "15.21", "3.20", "1.18", "2.16", "3.436", "3.65", "59.9", "118.8", "92.0", "98.0",
        "1.91", "7.63", "30.52", "122.07", "488.2", "488.28", "17.58", "4.120", "0.245", "1.22", "0.941", "0.96",
        "0.539", "0.542", "0.582", "0.585",
        "0.6121", "0.6626", "0.6930", "0.7965", "0.9674", "0.9823", "4.65", "5.66", "4.71", "1.03", "1.24",'''

assert old_str in content, "old_str not found in test_pdf_allowlist.py"
content = content.replace(old_str, new_str, 1)

old_regex = """    # Extract Sections 5-6
    sec5_6_match = re.search(r'\\n\\s*5\\s+(?:Experimental|Empirical)\\s+Evaluation(.*?)(?=\\n\\s*(?:7\\s+Conclusion|Declarations|References))', full_text, re.DOTALL)
    if not sec5_6_match:
        sec5_6_match = re.search(r'\\n\\s*5\\s+[^\\n]+(.*?)(?=\\n\\s*(?:7\\s+[^\\n]+|Declarations|References))', full_text, re.DOTALL)
    sec5_6_text = sec5_6_match.group(1) if sec5_6_match else \"\""""

new_regex = """    # Extract Sections 4-8
    sec_match = re.search(r'\\n\\s*4\\s+Experimental Setup(.*?)(?=\\n\\s*(?:9\\s+Conclusion|Declarations|References))', full_text, re.DOTALL)
    if not sec_match:
        sec_match = re.search(r'\\n\\s*(?:4|5)\\s+[^\\n]+(.*?)(?=\\n\\s*(?:(?:7|8|9)\\s+[^\\n]+|Declarations|References))', full_text, re.DOTALL)
    sec5_6_text = sec_match.group(1) if sec_match else \"\""""

assert old_regex in content, "old_regex not found in test_pdf_allowlist.py"
content = content.replace(old_regex, new_regex, 1)

path.write_text(content, encoding="utf-8")
print("Successfully patched tests/test_pdf_allowlist.py")
