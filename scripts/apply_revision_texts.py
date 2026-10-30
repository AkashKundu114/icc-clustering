"""
scripts/apply_revision_texts.py

Applies the correct Section 3.1, Section 5, and Section 9 texts to paper/main.tex
and ensures byte-for-byte synchronization with springer_manuscript/main.tex.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAIN_TEX = ROOT / "paper" / "main.tex"
SPRINGER_TEX = ROOT / "springer_manuscript" / "main.tex"

def main():
    text = MAIN_TEX.read_text(encoding="utf-8")

    # Fix the two stripped % spots:
    text = text.replace(r"The stratified \% subsampling protocol", r"The stratified 80\% subsampling protocol")
    text = text.replace(r"(\% CI: $[+0.379, +0.662]$", r"(95\% CI: $[+0.379, +0.662]$")

    # Write out to both files
    MAIN_TEX.write_text(text, encoding="utf-8")
    SPRINGER_TEX.write_text(text, encoding="utf-8")
    print(f"[+] Fixed percentages and synchronized to {MAIN_TEX} and {SPRINGER_TEX}")

if __name__ == "__main__":
    main()
