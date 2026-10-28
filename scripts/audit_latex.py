import os
import re

def audit_latex():
    main_path = "paper/main.tex"
    with open(main_path, "r", encoding="utf-8") as f:
        main_content = f.read()

    # Find all included files
    included_files = re.findall(r'\\input\{([^}]+)\}', main_content)
    print("Found included files:", included_files)

    all_content = main_content
    for inc in included_files:
        inc_path = os.path.join("paper", inc)
        if not inc_path.endswith(".tex"):
            inc_path += ".tex"
        if os.path.exists(inc_path):
            with open(inc_path, "r", encoding="utf-8") as f:
                all_content += "\n" + f.read()
        else:
            print(f"WARNING: Included file {inc_path} does not exist!")

    # Collect labels
    labels = set(re.findall(r'\\label\{([^}]+)\}', all_content))
    print(f"Total labels defined: {len(labels)}")

    # Collect refs
    refs = set(re.findall(r'\\ref\{([^}]+)\}', all_content))
    eqrefs = set(re.findall(r'\\eqref\{([^}]+)\}', all_content))
    all_refs = refs.union(eqrefs)
    print(f"Total refs referenced: {len(all_refs)}")

    missing_refs = all_refs - labels
    if missing_refs:
        print("ERROR: Missing labels for refs:")
        for r in missing_refs:
            print(f"  - {r}")
    else:
        print("SUCCESS: All \\ref and \\eqref targets resolve cleanly!")

    # Check citations
    bib_path = "paper/references.bib"
    with open(bib_path, "r", encoding="utf-8") as f:
        bib_content = f.read()
    bib_keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+),', bib_content))
    print(f"Total bib keys defined: {len(bib_keys)}")

    cites = set()
    for cite_match in re.findall(r'\\cite\{([^}]+)\}', all_content):
        for c in cite_match.split(','):
            cites.add(c.strip())
    print(f"Total citations referenced: {len(cites)}")

    missing_cites = cites - bib_keys
    if missing_cites:
        print("ERROR: Missing bibliography entries for citations:")
        for c in missing_cites:
            print(f"  - {c}")
    else:
        print("SUCCESS: All \\cite keys exist in references.bib!")

    # Check for placeholder strings
    bad_patterns = [r'\?\?', r'\[\?', r'TODO', r'FIXME', r'XXX']
    for p in bad_patterns:
        matches = re.findall(p, all_content)
        if matches:
            print(f"WARNING: Found {len(matches)} occurrences of '{p}' in LaTeX source!")

if __name__ == "__main__":
    audit_latex()
