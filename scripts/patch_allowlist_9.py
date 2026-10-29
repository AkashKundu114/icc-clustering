def patch():
    with open("tests/test_pdf_allowlist.py", "r", encoding="utf-8") as f:
        text = f.read()

    target = '"8.1", "8.2", "8.3",'
    replacement = '"8.1", "8.2", "8.3",\n        "9.1", "9.2", "9.3", "10.1",'

    if target in text:
        text = text.replace(target, replacement, 1)
        print("Patched section headings in tests/test_pdf_allowlist.py")
    else:
        print("Target not found!")
        return

    with open("tests/test_pdf_allowlist.py", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    patch()
