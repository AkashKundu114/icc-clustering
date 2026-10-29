import os
import re
import json

def extract_text_from_pdf(pdf_path):
    try:
        import pymupdf  # PyMuPDF
        doc = pymupdf.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text
    except Exception:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text

def run_checks():
    pdf_path = "paper/main.pdf"
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} does not exist!")
        return False

    pdf_text = extract_text_from_pdf(pdf_path)
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

    # 2. Check that deprecated CDs 3.65 and 4.19 are NOT present
    for dep_cd in ["3.65", "4.19"]:
        if dep_cd in pdf_text:
            matches = list(re.finditer(rf'(\S+\s+){{0,3}}{re.escape(dep_cd)}(\s+\S+){{0,3}}', pdf_text))
            print(f"WARNING: Found deprecated CD {dep_cd} in text ({len(matches)} matches):")
            for m in matches:
                print("  Context:", m.group(0).strip())
            return False
    print("PASS: Deprecated CD values (3.65, 4.19) are completely absent.")

    # 3. Load stats.json
    with open("results/stats.json", "r", encoding="utf-8") as f:
        stats = json.load(f)

    # 4. Verify core statistical values appear in PDF text
    checks = [
        ("Friedman p-value (0.40)", "0.40", True),
        ("Nemenyi CD (4.62)", "4.62", True),
        ("K-Means rank (5.15)", "5.15", True),
        ("DEC rank (5.23)", "5.23", True),
        ("Standard Consensus rank (5.23)", "5.23", True),
        ("ICC-v2 rank (5.62)", "5.62", True),
        ("High-D ICC-v2 rank (2.17)", "2.17", True),
        ("Grand Mean ARI (0.152)", "0.152", True),
        ("Grand Median ARI (0.055)", "0.055", True),
        ("Mean Excl Leu/SRB (0.076)", "0.076", True),
        ("Model fits count (3,000)", "3,000", True),
        ("Memory reduction 99.6%", "99.6%", True),
        ("Peak RAM reduction 97.4%", "97.4%", True),
        ("Leukemia active features 1,069", "1,069", True),
        ("Leukemia ARI 0.600", "0.600", True),
        ("SRBCT ARI 0.546", "0.546", True),
        ("Sarle uniform BC 5/9 or 0.556", "0.556", True),
    ]

    all_passed = True
    for desc, val, req in checks:
        if val in pdf_text:
            print(f"PASS: {desc} present in PDF.")
        else:
            print(f"FAIL: {desc} ('{val}') NOT found in PDF text!")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    success = run_checks()
    if not success:
        exit(1)
    print("\nALL VERIFICATIONS PASSED CLEANLY!")
