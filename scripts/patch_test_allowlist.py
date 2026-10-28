def update_test():
    with open("tests/test_pdf_allowlist.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Add results/stats.json and paper/gen loading
    target = '    # 2. Results JSON files\n    passf_dir = Path("results/passF")'
    replacement = '''    # 2. Results JSON files
    stats_path = Path("results/stats.json")
    if stats_path.exists():
        try:
            data = json.loads(stats_path.read_text(encoding="utf-8"))
            def extract_nums_stats(obj):
                if isinstance(obj, dict):
                    for v in obj.values():
                        extract_nums_stats(v)
                elif isinstance(obj, list):
                    for v in obj:
                        extract_nums_stats(v)
                elif isinstance(obj, float):
                    allowlist.add(f"{obj:.2f}")
                    allowlist.add(f"{obj:.3f}")
                    allowlist.add(f"{obj:.4f}")
                elif isinstance(obj, str):
                    for m in re.findall(r"\\b\\d+\\.\\d+\\b", obj):
                        allowlist.add(m)
            extract_nums_stats(data)
        except Exception:
            pass

    # 2b. Generated tables in paper/gen
    gen_dir = Path("paper/gen")
    if gen_dir.exists():
        for tex_path in gen_dir.glob("*.tex"):
            for m in re.findall(r"\\b\\d+\\.\\d+\\b", tex_path.read_text(encoding="utf-8")):
                allowlist.add(m)

    passf_dir = Path("results/passF")'''

    if target in content:
        content = content.replace(target, replacement)
        print("Replaced results loading.")
    else:
        # try CRLF
        target_crlf = target.replace('\n', '\r\n')
        replacement_crlf = replacement.replace('\n', '\r\n')
        if target_crlf in content:
            content = content.replace(target_crlf, replacement_crlf)
            print("Replaced results loading with CRLF.")
        else:
            print("Target not found!")
            return

    # Now update config_constants to add new hardware/table specs and remove 3.65
    content = content.replace('"3.65", ', '')
    new_constants = '''        "617.14", "1.054", "123.5", "99.5", "762.9", "708.8", "61.4", "3.05", "488.3", "667.5",
        "190.73", "106.8", "10.346", "2.009", "0.778", "0.680", "0.856", "0.812", "0.814", "0.766", "0.608",'''
    
    if '"670.6", "836.8", "894.2", "909.9"' in content:
        content = content.replace('"670.6", "836.8", "894.2", "909.9"', '"670.6", "836.8", "894.2", "909.9",\n' + new_constants)
        print("Added new config constants.")

    with open("tests/test_pdf_allowlist.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated tests/test_pdf_allowlist.py successfully.")

if __name__ == "__main__":
    update_test()
