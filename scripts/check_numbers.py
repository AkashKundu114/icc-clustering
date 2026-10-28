import os
import re
import subprocess
import json

def run_checks():
    pdf_path = "paper/main.pdf"
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} does not exist!")
        return False

    # Extract text using pdftotext
    txt_path = "paper/main_extracted.txt"
    res = subprocess.run(["pdftotext", pdf_path, txt_path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR running pdftotext: {res.stderr}")
        return False

    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        pdf_text = f.read()

    print(f"Extracted {len(pdf_text)} characters from {pdf_path}.")

    # 1. Check for unresolved references
    unresolved_refs = re.findall(r'\?\?|\[\?', pdf_text)
    if unresolved_refs:
        print(f"ERROR: Found unresolved references in PDF: {len(unresolved_refs)} matches!")
        for m in re.finditer(r'(\S+\s+){0,3}(\?\?|\[\?)(\s+\S+){0,3}', pdf_text):
            print("  Context:", m.group(0).strip())
        return False
    else:
        print("PASS: Zero unresolved references (?? or [?) found in PDF.")

    # 2. Check that deprecated CD 3.65 is NOT present
    if "3.65" in pdf_text:
        # Check context
        matches = list(re.finditer(r'(\S+\s+){0,3}3\.65(\s+\S+){0,3}', pdf_text))
        print(f"WARNING: Found 3.65 in text ({len(matches)} matches):")
        for m in matches:
            print("  Context:", m.group(0).strip())
        return False
    else:
        print("PASS: Deprecated CD 3.65 is completely absent.")

    # 3. Load stats.json
    with open("results/stats.json", "r", encoding="utf-8") as f:
        stats = json.load(f)

    # 4. Verify core statistical values appear in PDF text
    checks = [
        ("Friedman p-value (0.48)", "0.48", True),
        ("Nemenyi CD (4.19)", "4.19", True),
        ("Standard Consensus rank (4.85)", "4.85", True),
        ("ICC-v2 rank (5.23)", "5.23", True),
        ("Grand Mean ARI (0.152)", "0.152", True),
        ("Grand Median ARI (0.055)", "0.055", True),
        ("Mean Excl Leu/SRB (0.076)", "0.076", True),
        ("Model fits count (2,750)", "2,750", True),
        ("Memory reduction 99.6%", "99.6%", True),
        ("Peak RAM reduction 97.4%", "97.4%", True),
        ("Leukemia active features 1,069", "1,069", True),
        ("Leukemia ARI 0.600", "0.600", True),
        ("SRBCT ARI 0.546", "0.546", True),
        ("Ablation interaction +0.140", "+0.140", True),
        ("Anchor cert null delta +0.019", "+0.019", True),
        ("Sarle uniform BC 5/9 or 0.556", "0.556", True),
    ]

    all_passed = True
    for desc, val, req in checks:
        if val in pdf_text:
            print(f"PASS: {desc} present in PDF.")
        else:
            print(f"FAIL: {desc} ('{val}') NOT found in PDF text!")
            all_passed = False

    # Clean up temporary extracted text
    if os.path.exists(txt_path):
        os.remove(txt_path)

    return all_passed

if __name__ == "__main__":
    success = run_checks()
    if not success:
        exit(1)
    print("\nALL VERIFICATIONS PASSED CLEANLY!")
